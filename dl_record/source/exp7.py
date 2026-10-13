import sys,os; sys.path.insert(0,'/tmp/claude-0/dl/run')
import tensorflow as tf; tf.config.threading.set_intra_op_parallelism_threads(int(os.environ.get('NT','2'))); tf.config.threading.set_inter_op_parallelism_threads(2)
from nbrun import run_notebook
CELLS=[
("Import libraries and hyperparameters",'''import os
import cv2
import keras
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

IMG_SIZE = 224
MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048
keras.utils.set_random_seed(42)

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")
class_vocab = sorted(train_df["tag"].unique())
print("Classes :", class_vocab)
print("Train videos :", len(train_df), "| Test videos :", len(test_df))'''),
("Video loading utilities (spatial part)",'''def crop_center_square(frame):
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
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)
            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)


def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(
        weights="imagenet", include_top=False, pooling="avg", input_shape=(IMG_SIZE, IMG_SIZE, 3))
    preprocess_input = keras.applications.inception_v3.preprocess_input
    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)
    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")


feature_extractor = build_feature_extractor()
print("CNN feature extractor ready  :", feature_extractor.name, "->", feature_extractor.output_shape)'''),
("Sequence model (temporal part) and the best checkpoint",'''def get_sequence_model():
    frame_features_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
    mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")
    x = keras.layers.GRU(16, return_sequences=True)(frame_features_input, mask=mask_input)
    x = keras.layers.GRU(8)(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(8, activation="relu")(x)
    output = keras.layers.Dense(len(class_vocab), activation="softmax")(x)
    rnn_model = keras.Model([frame_features_input, mask_input], output)
    rnn_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return rnn_model


data = np.load("ucf101_features.npz")
test_data, test_labels = (data["test_features"], data["test_masks"]), data["test_labels"]

sequence_model = get_sequence_model()
sequence_model.load_weights("/tmp/video_classifier/ckpt.weights.h5")      # best weights saved in Exp. 6
_, accuracy = sequence_model.evaluate([test_data[0], test_data[1]], test_labels)
print(f"Test accuracy: {round(accuracy * 100, 2)}%")'''),
("Classification report and confusion matrix",'''probs = sequence_model.predict([test_data[0], test_data[1]], verbose=0)
y_pred = probs.argmax(axis=1)
y_true = test_labels.ravel()

print(classification_report(y_true, y_pred, target_names=class_vocab, digits=4))

cm = confusion_matrix(y_true, y_pred)
fig, ax = plt.subplots(figsize=(6.6, 5.6))
ConfusionMatrixDisplay(cm, display_labels=class_vocab).plot(ax=ax, cmap="Blues", xticks_rotation=30, colorbar=False)
ax.set_title("Confusion matrix - CNN + RNN on 224 test videos")
plt.tight_layout()
plt.show()'''),
("Single-video inference utilities",'''def prepare_single_video(frames):
    frames = frames[None, ...]
    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH), dtype="bool")
    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")
    for i, batch in enumerate(frames):
        video_length = batch.shape[0]
        length = min(MAX_SEQ_LENGTH, video_length)
        for j in range(length):
            frame_features[i, j, :] = feature_extractor.predict(batch[None, j, :], verbose=0)
        frame_mask[i, :length] = 1          # 1 = not masked, 0 = masked
    return frame_features, frame_mask


def sequence_prediction(path):
    frames = load_video(os.path.join("test", path))
    frame_features, frame_mask = prepare_single_video(frames)
    probabilities = sequence_model.predict([frame_features, frame_mask], verbose=0)[0]
    for i in np.argsort(probabilities)[::-1]:
        print(f"  {class_vocab[i]}: {probabilities[i] * 100:5.2f}%")
    return frames, probabilities'''),
("Classify test videos end-to-end",'''np.random.seed(11)
picked = []
for tag in class_vocab:                                    # one random test video of every class
    picked.append(np.random.choice(test_df[test_df["tag"] == tag]["video_name"].values))

results = []
for test_video in picked:
    print(f"Test video path: {test_video}")
    frames, probabilities = sequence_prediction(test_video)
    results.append((test_video, frames, probabilities))
    print()'''),
("Visualise the predictions",'''fig, axes = plt.subplots(len(results), 7, figsize=(13, 2.5 * len(results)),
                         gridspec_kw={"width_ratios": [1, 1, 1, 1, 1, 0.95, 2.4]})
for r, (name, frames, prob) in enumerate(results):
    for c, f in enumerate(np.linspace(0, min(len(frames), MAX_SEQ_LENGTH) - 1, 5, dtype=int)):
        axes[r, c].imshow(frames[f]); axes[r, c].axis("off")
        if r == 0: axes[r, c].set_title(f"frame {f + 1}")
    axes[r, 5].axis("off")
    order = np.argsort(prob)
    colors = ["#2ca02c" if class_vocab[i] == name.split("_")[1] else "#9aa5b1" for i in order]
    axes[r, 6].barh([class_vocab[i] for i in order], prob[order] * 100, color=colors)
    axes[r, 6].set_xlim(0, 100); axes[r, 6].set_xlabel("Probability (%)")
    pred = class_vocab[int(prob.argmax())]
    axes[r, 6].set_title(f"{name}\\nPredicted: {pred}  ({prob.max() * 100:.1f} %)", fontsize=11, loc="left")
fig.subplots_adjust(left=0.01, right=0.985, top=0.93, bottom=0.07, wspace=0.05, hspace=0.95)
plt.show()'''),
("Per-class accuracy summary",'''print(f"{'Class':<16}{'Videos':>8}{'Correct':>9}{'Accuracy':>11}")
for k, tag in enumerate(class_vocab):
    m = y_true == k
    print(f"{tag:<16}{m.sum():>8}{(y_pred[m] == k).sum():>9}{100 * (y_pred[m] == k).mean():>10.2f}%")
print("-" * 44)
print(f"{'Overall':<16}{len(y_true):>8}{(y_pred == y_true).sum():>9}{100 * (y_pred == y_true).mean():>10.2f}%")'''),
]
if __name__=='__main__':
    run_notebook('exp7',CELLS,'/tmp/claude-0/dl/out','/tmp/claude-0/dl/data')
