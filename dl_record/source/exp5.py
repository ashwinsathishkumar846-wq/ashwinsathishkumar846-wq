import sys; sys.path.insert(0,'/tmp/claude-0/dl/run')
from nbrun import run_notebook
CELLS=[
("Download the dataset",'''!wget -q https://github.com/sayakpaul/Action-Recognition-in-TensorFlow/releases/download/v1.0.0/ucf101_top5.tar.gz
!tar xf ucf101_top5.tar.gz'''),
("Import libraries and define hyperparameters",'''import os
import cv2
import keras
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 10

MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048

print("TensorFlow version :", tf.__version__)
print("Keras version      :", keras.__version__)
print("OpenCV version     :", cv2.__version__)
print("IMG_SIZE =", IMG_SIZE, "| MAX_SEQ_LENGTH =", MAX_SEQ_LENGTH, "| NUM_FEATURES =", NUM_FEATURES)'''),
("Load the train / test video lists",'''train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

print(f"Total videos for training: {len(train_df)}")
print(f"Total videos for testing: {len(test_df)}")

train_df.sample(10)'''),
("Frame-extraction utilities",'''def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x + min_dim]


def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]      # BGR -> RGB
            frames.append(frame)
            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)'''),
("Read frames from one video",'''sample_video = os.path.join("train", train_df["video_name"].iloc[0])
frames = load_video(sample_video)
print("Video path    :", sample_video)
print("Total frames  :", len(frames))
print("Frame shape   :", frames[0].shape)

idx = np.linspace(0, len(frames) - 1, 5, dtype=int)
fig, axes = plt.subplots(1, 5, figsize=(12, 3.1))
for ax, i in zip(axes, idx):
    ax.imshow(frames[i])
    ax.set_title(f"Frame {i}")
    ax.axis("off")
plt.suptitle(f"Frames extracted from {os.path.basename(sample_video)}", fontsize=13)
plt.show()'''),
("Basic CNN operations: convolution, ReLU, max pooling, flatten",'''frame = frames[idx[2]].astype("float32") / 255.0
gray = frame.mean(axis=-1)[None, ..., None]                      # (1, 224, 224, 1)

kernels = {
    "Sobel-X (vertical edges)":   [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
    "Sobel-Y (horizontal edges)": [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
    "Laplacian (blobs)":          [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
    "Gaussian blur":              [[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]],
}
W = np.stack([np.array(k, dtype="float32") for k in kernels.values()], axis=-1)[:, :, None, :]  # (3,3,1,4)

conv = tf.nn.conv2d(gray, W, strides=1, padding="SAME")           # convolution
relu = tf.nn.relu(conv)                                           # ReLU activation
pool = tf.nn.max_pool2d(relu, ksize=2, strides=2, padding="VALID")# 2x2 max pooling
flat = tf.reshape(pool, (1, -1))                                  # flatten

print("Input  (grayscale frame) :", gray.shape)
print("Convolution (4 filters)  :", conv.shape)
print("ReLU                     :", relu.shape)
print("Max pooling (2x2)        :", pool.shape)
print("Flatten                  :", flat.shape)

fig, ax = plt.subplots(3, 5, figsize=(12, 7.6))
ax[0, 0].imshow(frame); ax[0, 0].set_title("Input frame")
for r, (T, name) in enumerate([(conv, "Convolution"), (relu, "ReLU"), (pool, "Max-pool")]):
    for c, k in enumerate(kernels):
        ax[r, c + 1].imshow(T[0, :, :, c], cmap="magma")
        ax[r, c + 1].set_title(f"{name}\\n{k.split(' (')[0]}", fontsize=9)
ax[1, 0].imshow(gray[0, :, :, 0], cmap="gray"); ax[1, 0].set_title("Grayscale input")
ax[2, 0].text(0.5, 0.5, f"Flatten\\n{tuple(flat.shape)}", ha="center", va="center", fontsize=14); ax[2, 0].set_xlim(0, 1); ax[2, 0].set_ylim(0, 1)
for a in ax.ravel(): a.set_xticks([]); a.set_yticks([])
plt.tight_layout()
plt.show()'''),
("Pre-trained CNN (InceptionV3) as feature extractor",'''def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    preprocess_input = keras.applications.inception_v3.preprocess_input

    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)

    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")


feature_extractor = build_feature_extractor()
feature_extractor.summary()'''),
("Encode the class labels",'''label_processor = keras.layers.StringLookup(
    num_oov_indices=0, vocabulary=np.unique(train_df["tag"])
)
print(label_processor.get_vocabulary())
print()
print(train_df["tag"].value_counts().to_string())'''),
("Video-to-feature utility",'''def prepare_all_videos(df, root_dir):
    num_samples = len(df)
    video_paths = df["video_name"].values.tolist()
    labels = df["tag"].values
    labels = keras.ops.convert_to_numpy(label_processor(labels[..., None]))

    # frame_masks marks which of the MAX_SEQ_LENGTH time-steps hold real frames (1) or padding (0)
    frame_masks = np.zeros(shape=(num_samples, MAX_SEQ_LENGTH), dtype="bool")
    frame_features = np.zeros(shape=(num_samples, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    for idx, path in enumerate(video_paths):
        frames = load_video(os.path.join(root_dir, path), max_frames=MAX_SEQ_LENGTH)
        length = min(MAX_SEQ_LENGTH, frames.shape[0])
        frame_features[idx, :length] = feature_extractor.predict(frames[:length], verbose=0)
        frame_masks[idx, :length] = 1

    return (frame_features, frame_masks), labels'''),
("Extract CNN features for every video",'''train_data, train_labels = prepare_all_videos(train_df, "train")
test_data, test_labels = prepare_all_videos(test_df, "test")

print(f"Frame features in train set: {train_data[0].shape}")
print(f"Frame masks in train set: {train_data[1].shape}")
print(f"Frame features in test set : {test_data[0].shape}")
print(f"Frame masks in test set : {test_data[1].shape}")

np.savez_compressed("ucf101_features.npz",
                    train_features=train_data[0], train_masks=train_data[1], train_labels=train_labels,
                    test_features=test_data[0], test_masks=test_data[1], test_labels=test_labels)
print("Features saved to ucf101_features.npz")'''),
("Visualise the extracted feature sequence",'''fig, ax = plt.subplots(1, 2, figsize=(12, 3.8), gridspec_kw={"width_ratios": [2.2, 1]})
im = ax[0].imshow(train_data[0][0][:, :256], aspect="auto", cmap="viridis")
ax[0].set_title("CNN feature matrix of video 0  (20 frames x first 256 of 2048 features)")
ax[0].set_xlabel("Feature index"); ax[0].set_ylabel("Frame (time-step)")
plt.colorbar(im, ax=ax[0], fraction=0.025)
ax[1].plot(np.linalg.norm(train_data[0][0], axis=1), marker="o", color="#1f77b4")
ax[1].set_title("L2 norm of each frame vector"); ax[1].set_xlabel("Frame"); ax[1].set_ylabel("||f||"); ax[1].grid(alpha=.3)
plt.tight_layout()
plt.show()
print("Mean activation :", round(float(train_data[0][train_data[1] == 1].mean()), 4))
print("Feature vector per frame :", NUM_FEATURES, "-> sequence per video :", MAX_SEQ_LENGTH, "x", NUM_FEATURES)'''),
]
if __name__=='__main__':
    run_notebook('exp5',CELLS,'/tmp/claude-0/dl/out','/tmp/claude-0/dl/data')
