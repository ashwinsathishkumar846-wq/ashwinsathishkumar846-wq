import sys,os; sys.path.insert(0,'/tmp/claude-0/dl/run')
import tensorflow as tf; tf.config.threading.set_intra_op_parallelism_threads(int(os.environ.get('NT','2'))); tf.config.threading.set_inter_op_parallelism_threads(2)
from nbrun import run_notebook
EP=int(os.environ.get('DC_EPOCHS','30'))
CELLS=[
("Import libraries",'''import time
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

tf.random.set_seed(42)
np.random.seed(42)
print("TensorFlow version :", tf.__version__)'''),
("Load and prepare the MNIST dataset",'''(train_images, _), (_, _) = keras.datasets.mnist.load_data()
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype("float32")
train_images = (train_images - 127.5) / 127.5          # normalise the images to [-1, 1]

BUFFER_SIZE = 60000
BATCH_SIZE = 128
train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)

print("Training images :", train_images.shape)
print("Batches per epoch :", len(train_dataset), "( batch size =", BATCH_SIZE, ")")'''),
("Generator model",'''def make_generator_model():
    model = keras.Sequential(name="generator")
    model.add(keras.Input(shape=(100,)))
    model.add(layers.Dense(7 * 7 * 256, use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Reshape((7, 7, 256)))

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding="same", use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding="same", use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding="same", use_bias=False, activation="tanh"))
    return model

generator = make_generator_model()
generator.summary()'''),
("Untrained generator output",'''noise = tf.random.normal([1, 100])
generated_image = generator(noise, training=False)
print("Generated image shape :", generated_image.shape)

plt.figure(figsize=(3.2, 3.2))
plt.imshow(generated_image[0, :, :, 0], cmap="gray")
plt.title("Image from the untrained generator"); plt.axis("off")
plt.show()'''),
("Discriminator model",'''def make_discriminator_model():
    model = keras.Sequential(name="discriminator")
    model.add(keras.Input(shape=(28, 28, 1)))
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding="same"))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding="same"))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))
    return model

discriminator = make_discriminator_model()
decision = discriminator(generated_image)
print("Discriminator decision on the untrained fake image :", decision.numpy())
discriminator.summary()'''),
("Loss functions and optimizers",'''cross_entropy = keras.losses.BinaryCrossentropy(from_logits=True)

def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    return real_loss + fake_loss

def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)

generator_optimizer = keras.optimizers.Adam(learning_rate=2e-4, beta_1=0.5)
discriminator_optimizer = keras.optimizers.Adam(learning_rate=2e-4, beta_1=0.5)
print("Loss  : Binary cross-entropy (from logits)")
print("Optim : Adam, learning rate = 2e-4, beta_1 = 0.5 (generator and discriminator)")'''),
("Training step and training loop",f'''EPOCHS = {EP}
noise_dim = 100
num_examples_to_generate = 16
seed = tf.random.normal([num_examples_to_generate, noise_dim])

@tf.function
def train_step(images):
    noise = tf.random.normal([tf.shape(images)[0], noise_dim])
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)
        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)
        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)
    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)
    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))
    return gen_loss, disc_loss

history = {{"gen": [], "disc": []}}
snapshots = {{}}
SNAP_EPOCHS = sorted({{1, EPOCHS // 6, EPOCHS // 2, EPOCHS}})

def train(dataset, epochs):
    for epoch in range(1, epochs + 1):
        start = time.time()
        g_l, d_l = [], []
        for image_batch in dataset:
            g, d = train_step(image_batch)
            g_l.append(float(g)); d_l.append(float(d))
        history["gen"].append(np.mean(g_l)); history["disc"].append(np.mean(d_l))
        if epoch in SNAP_EPOCHS:
            snapshots[epoch] = generator(seed, training=False).numpy()
        print("Epoch {{:>2}}/{{}}  gen_loss: {{:.4f}}  disc_loss: {{:.4f}}  - Time for epoch {{}} is {{:.2f}} sec".format(epoch, epochs, history["gen"][-1], history["disc"][-1], epoch, time.time() - start))

train(train_dataset, EPOCHS)
print("DCGAN training completed.")'''),
("Training curves",'''plt.figure(figsize=(8, 4.2))
plt.plot(history["gen"], label="Generator loss", color="#1f77b4")
plt.plot(history["disc"], label="Discriminator loss", color="#d62728")
plt.title("DCGAN - training loss"); plt.xlabel("Epoch"); plt.ylabel("Loss"); plt.legend(); plt.grid(alpha=.3)
plt.show()'''),
("Images generated during training",'''fig, axes = plt.subplots(1, len(snapshots), figsize=(3.1 * len(snapshots), 3.7))
for ax, ep in zip(axes, snapshots):
    grid = ((snapshots[ep][..., 0] + 1) / 2).reshape(4, 4, 28, 28).transpose(0, 2, 1, 3).reshape(4 * 28, 4 * 28)
    ax.imshow(grid, cmap="gray"); ax.set_title(f"Epoch {ep}"); ax.axis("off")
plt.suptitle("DCGAN - generated digits from the same 16 noise vectors", fontsize=13)
plt.show()'''),
("Generate the final images",'''predictions = generator(seed, training=False).numpy()
fig = plt.figure(figsize=(5.6, 5.6))
for i in range(predictions.shape[0]):
    plt.subplot(4, 4, i + 1)
    plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap="gray")
    plt.axis("off")
plt.suptitle("Images generated by the trained DCGAN", fontsize=12)
plt.show()
print("Final discriminator score on generated images (logit mean) : %.4f" % discriminator(generator(seed, training=False), training=False).numpy().mean())'''),
]
if __name__=='__main__':
    run_notebook('exp9',CELLS,'/tmp/claude-0/dl/out','/tmp/claude-0/dl/data')
