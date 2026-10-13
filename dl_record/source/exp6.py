import sys,os; sys.path.insert(0,'/tmp/claude-0/dl/run')
import tensorflow as tf; tf.config.threading.set_intra_op_parallelism_threads(int(os.environ.get('NT','2'))); tf.config.threading.set_inter_op_parallelism_threads(2)
from nbrun import run_notebook
CELLS=[
("Import libraries and load the CNN feature sequences",'''import os
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

keras.utils.set_random_seed(42)

data = np.load("ucf101_features.npz")
train_data, train_labels = (data["train_features"], data["train_masks"]), data["train_labels"]
test_data, test_labels = (data["test_features"], data["test_masks"]), data["test_labels"]
class_vocab = sorted(pd.read_csv("train.csv")["tag"].unique())

# train.csv is sorted class-by-class, but validation_split takes the LAST 30 % of the data.
# Shuffle once so that the validation set contains videos of every class.
perm = np.random.RandomState(42).permutation(len(train_labels))
train_data = (train_data[0][perm], train_data[1][perm])
train_labels = train_labels[perm]

print("Class vocabulary           :", class_vocab)
print("Frame features (train)     :", train_data[0].shape)
print("Frame masks    (train)     :", train_data[1].shape)
print("Labels         (train)     :", train_labels.shape)
print("Frame features (test)      :", test_data[0].shape)'''),
("Sequence model with GRU layers",'''def get_sequence_model():
    frame_features_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
    mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")

    # the mask hides the zero-padded time-steps from the recurrent layers
    x = keras.layers.GRU(16, return_sequences=True)(frame_features_input, mask=mask_input)
    x = keras.layers.GRU(8)(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(8, activation="relu")(x)
    output = keras.layers.Dense(len(class_vocab), activation="softmax")(x)

    rnn_model = keras.Model([frame_features_input, mask_input], output)
    rnn_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return rnn_model

get_sequence_model().summary()'''),
("Train the RNN (GRU) model",'''def run_experiment():
    os.makedirs("/tmp/video_classifier", exist_ok=True)
    filepath = "/tmp/video_classifier/ckpt.weights.h5"
    checkpoint = keras.callbacks.ModelCheckpoint(filepath, save_weights_only=True, save_best_only=True, verbose=1)

    seq_model = get_sequence_model()
    history = seq_model.fit(
        [train_data[0], train_data[1]],
        train_labels,
        validation_split=0.3,
        epochs=EPOCHS,
        callbacks=[checkpoint],
    )

    seq_model.load_weights(filepath)
    _, accuracy = seq_model.evaluate([test_data[0], test_data[1]], test_labels)
    print(f"Test accuracy: {round(accuracy * 100, 2)}%")
    return history, seq_model

history, sequence_model = run_experiment()'''),
("Accuracy and loss curves",'''fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].plot(history.history["accuracy"], marker="o", label="Training accuracy", color="#1f77b4")
ax[0].plot(history.history["val_accuracy"], marker="s", label="Validation accuracy", color="#ff7f0e")
ax[0].set_title("GRU model - accuracy"); ax[0].set_xlabel("Epoch"); ax[0].set_ylabel("Accuracy"); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].plot(history.history["loss"], marker="o", label="Training loss", color="#1f77b4")
ax[1].plot(history.history["val_loss"], marker="s", label="Validation loss", color="#ff7f0e")
ax[1].set_title("GRU model - loss"); ax[1].set_xlabel("Epoch"); ax[1].set_ylabel("Loss"); ax[1].legend(); ax[1].grid(alpha=.3)
plt.tight_layout()
plt.show()'''),
("LSTM variant of the temporal model",'''def get_lstm_model():
    frame_features_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
    mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")
    x = keras.layers.LSTM(16, return_sequences=True)(frame_features_input, mask=mask_input)
    x = keras.layers.LSTM(8)(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(8, activation="relu")(x)
    output = keras.layers.Dense(len(class_vocab), activation="softmax")(x)
    model = keras.Model([frame_features_input, mask_input], output)
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

lstm_model = get_lstm_model()
lstm_model.summary()
lstm_history = lstm_model.fit([train_data[0], train_data[1]], train_labels,
                              validation_split=0.3, epochs=EPOCHS, verbose=2)
_, lstm_acc = lstm_model.evaluate([test_data[0], test_data[1]], test_labels, verbose=0)
print(f"LSTM test accuracy: {round(lstm_acc * 100, 2)}%")'''),
("Compare GRU and LSTM",'''_, gru_acc = sequence_model.evaluate([test_data[0], test_data[1]], test_labels, verbose=0)
names = ["GRU (16-8)", "LSTM (16-8)"]
accs = [gru_acc * 100, lstm_acc * 100]
params = [sequence_model.count_params(), lstm_model.count_params()]

print(f"{'Model':<14}{'Parameters':>12}{'Test accuracy':>16}")
for n, p, a in zip(names, params, accs):
    print(f"{n:<14}{p:>12,}{a:>15.2f}%")

plt.figure(figsize=(6, 4.2))
bars = plt.bar(names, accs, color=["#1f77b4", "#ff7f0e"], width=0.5)
for b, a in zip(bars, accs):
    plt.text(b.get_x() + b.get_width() / 2, a + 1, f"{a:.2f}%", ha="center", fontweight="bold")
plt.ylim(0, 105); plt.ylabel("Test accuracy (%)"); plt.title("Temporal models on UCF101 (5 classes)")
plt.show()'''),
]
if __name__=='__main__':
    run_notebook('exp6',CELLS,'/tmp/claude-0/dl/out','/tmp/claude-0/dl/data')
