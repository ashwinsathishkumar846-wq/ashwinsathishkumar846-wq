import sys,os; sys.path.insert(0,'/tmp/claude-0/dl/run')
import tensorflow as tf; tf.config.threading.set_intra_op_parallelism_threads(int(os.environ.get('NT','2'))); tf.config.threading.set_inter_op_parallelism_threads(2)
from nbrun import run_notebook
CELLS=[
("Import libraries",'''import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(42)
tf.random.set_seed(42)
print("TensorFlow version :", tf.__version__)
print("Keras version      :", keras.__version__)'''),
("Load and pre-process the MNIST images",'''(x_train, _), (_, _) = keras.datasets.mnist.load_data()

# scale pixels to [-1, 1] to match the tanh output of the generator
x_train = (x_train.astype("float32") - 127.5) / 127.5
x_train = x_train.reshape(-1, 784)

BATCH_SIZE = 128
dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(60000).batch(BATCH_SIZE, drop_remainder=True)

print("Training images   :", x_train.shape)
print("Pixel range       :", x_train.min(), "to", x_train.max())
print("Batches per epoch :", len(dataset), "( batch size =", BATCH_SIZE, ")")

fig, axes = plt.subplots(2, 8, figsize=(10, 3.1))
for ax, img in zip(axes.ravel(), x_train[:16]):
    ax.imshow(img.reshape(28, 28), cmap="gray"); ax.axis("off")
plt.suptitle("Real MNIST images", fontsize=13)
plt.show()'''),
("Generator network",'''LATENT_DIM = 100

def build_generator():
    model = keras.Sequential(name="generator")
    model.add(keras.Input(shape=(LATENT_DIM,)))
    model.add(layers.Dense(256))
    model.add(layers.LeakyReLU(negative_slope=0.2))
    model.add(layers.BatchNormalization(momentum=0.8))
    model.add(layers.Dense(512))
    model.add(layers.LeakyReLU(negative_slope=0.2))
    model.add(layers.BatchNormalization(momentum=0.8))
    model.add(layers.Dense(1024))
    model.add(layers.LeakyReLU(negative_slope=0.2))
    model.add(layers.BatchNormalization(momentum=0.8))
    model.add(layers.Dense(784, activation="tanh"))
    return model

generator = build_generator()
generator.summary()'''),
("Discriminator network",'''def build_discriminator():
    model = keras.Sequential(name="discriminator")
    model.add(keras.Input(shape=(784,)))
    model.add(layers.Dense(512))
    model.add(layers.LeakyReLU(negative_slope=0.2))
    model.add(layers.Dense(256))
    model.add(layers.LeakyReLU(negative_slope=0.2))
    model.add(layers.Dense(1, activation="sigmoid"))
    return model

discriminator = build_discriminator()
discriminator.summary()'''),
("Loss function and optimizers",'''cross_entropy = keras.losses.BinaryCrossentropy()

generator_optimizer = keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5)
discriminator_optimizer = keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5)
print("Loss      : Binary cross-entropy")
print("Optimizer : Adam (learning rate = 0.0002, beta_1 = 0.5) for the generator and the discriminator")'''),
("Training step",'''@tf.function
def train_step(real_imgs):
    noise = tf.random.normal((tf.shape(real_imgs)[0], LATENT_DIM))
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        fake_imgs = generator(noise, training=True)
        real_output = discriminator(real_imgs, training=True)
        fake_output = discriminator(fake_imgs, training=True)
        # discriminator: real -> 1, fake -> 0        generator: fake -> 1
        d_loss = 0.5 * (cross_entropy(tf.ones_like(real_output), real_output)
                        + cross_entropy(tf.zeros_like(fake_output), fake_output))
        g_loss = cross_entropy(tf.ones_like(fake_output), fake_output)
    d_grads = disc_tape.gradient(d_loss, discriminator.trainable_variables)
    g_grads = gen_tape.gradient(g_loss, generator.trainable_variables)
    discriminator_optimizer.apply_gradients(zip(d_grads, discriminator.trainable_variables))
    generator_optimizer.apply_gradients(zip(g_grads, generator.trainable_variables))
    d_acc = 0.5 * (tf.reduce_mean(tf.cast(real_output > 0.5, tf.float32))
                   + tf.reduce_mean(tf.cast(fake_output < 0.5, tf.float32)))
    return d_loss, d_acc, g_loss

print("Training step defined: the discriminator and the generator are updated with their own gradients.")'''),
("Train the Vanilla GAN",'''EPOCHS = 50
fixed_noise = tf.random.normal((16, LATENT_DIM))
history = {"d_loss": [], "d_acc": [], "g_loss": []}
snapshots = {}

for epoch in range(1, EPOCHS + 1):
    d_l, d_a, g_l = [], [], []
    for real_batch in dataset:
        d_loss, d_acc, g_loss = train_step(real_batch)
        d_l.append(float(d_loss)); d_a.append(float(d_acc)); g_l.append(float(g_loss))
    history["d_loss"].append(np.mean(d_l)); history["d_acc"].append(np.mean(d_a)); history["g_loss"].append(np.mean(g_l))
    if epoch in (1, 10, 25, 50):
        snapshots[epoch] = generator(fixed_noise, training=False).numpy()
    if epoch == 1 or epoch % 5 == 0:
        print(f"Epoch {epoch:>2}/{EPOCHS}  [D loss: {history['d_loss'][-1]:.4f}, acc: {100 * history['d_acc'][-1]:.2f}%]  [G loss: {history['g_loss'][-1]:.4f}]")
print("Vanilla GAN training completed.")'''),
("Training curves",'''fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].plot(history["d_loss"], label="Discriminator loss", color="#d62728")
ax[0].plot(history["g_loss"], label="Generator loss", color="#1f77b4")
ax[0].set_title("Vanilla GAN - loss"); ax[0].set_xlabel("Epoch"); ax[0].set_ylabel("Binary cross-entropy"); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].plot(np.array(history["d_acc"]) * 100, color="#2ca02c")
ax[1].axhline(50, ls="--", color="grey", lw=1)
ax[1].set_title("Discriminator accuracy (50 % = fully fooled)"); ax[1].set_xlabel("Epoch"); ax[1].set_ylabel("Accuracy (%)"); ax[1].set_ylim(0, 100); ax[1].grid(alpha=.3)
plt.tight_layout()
plt.show()'''),
("Images generated during training",'''fig, axes = plt.subplots(1, 4, figsize=(12, 3.7))
for ax, ep in zip(axes, snapshots):
    grid = snapshots[ep].reshape(4, 4, 28, 28).transpose(0, 2, 1, 3).reshape(4 * 28, 4 * 28)
    ax.imshow(grid, cmap="gray"); ax.set_title(f"Epoch {ep}"); ax.axis("off")
plt.suptitle("Vanilla GAN - generated digits from the same 16 noise vectors", fontsize=13)
plt.show()'''),
("Generate new images from random noise",'''noise = tf.random.normal((25, LATENT_DIM))
gen_imgs = generator(noise, training=False).numpy().reshape(-1, 28, 28)
gen_imgs = 0.5 * gen_imgs + 0.5                       # back to [0, 1]

print("Noise vector shape     :", tuple(noise.shape))
print("Generated image batch  :", gen_imgs.shape)
print("Generated pixel range  : %.3f to %.3f" % (gen_imgs.min(), gen_imgs.max()))
print("Discriminator score on generated images (mean) : %.4f" % discriminator(gen_imgs.reshape(-1, 784) * 2 - 1, training=False).numpy().mean())

fig, axes = plt.subplots(5, 5, figsize=(6.5, 6.5))
for ax, img in zip(axes.ravel(), gen_imgs):
    ax.imshow(img, cmap="gray"); ax.axis("off")
plt.suptitle("Images generated by the trained Vanilla GAN", fontsize=12)
plt.show()'''),
]
if __name__=='__main__':
    run_notebook('exp8',CELLS,'/tmp/claude-0/dl/out','/tmp/claude-0/dl/data')
