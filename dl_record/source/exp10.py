import sys,os; sys.path.insert(0,'/tmp/claude-0/dl/run')
import tensorflow as tf; tf.config.threading.set_intra_op_parallelism_threads(int(os.environ.get('NT','2'))); tf.config.threading.set_inter_op_parallelism_threads(2)
from nbrun import run_notebook
EP=int(os.environ.get('CG_EPOCHS','20'))
CELLS=[
("Import libraries",'''import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(42)
tf.random.set_seed(42)
print("TensorFlow version :", tf.__version__)'''),
("Load the MNIST images with their class labels",'''(x_train, y_train), (_, _) = keras.datasets.mnist.load_data()
x_train = np.expand_dims(x_train.astype("float32"), -1)
x_train = (x_train - 127.5) / 127.5                    # scale to [-1, 1]

LATENT_DIM = 100
NUM_CLASSES = 10
print("Images :", x_train.shape, "| Labels :", y_train.shape)
print("Classes:", np.unique(y_train))

fig, axes = plt.subplots(2, 10, figsize=(11, 3.1))
for d in range(10):
    for r in range(2):
        axes[r, d].imshow(x_train[np.where(y_train == d)[0][r], :, :, 0], cmap="gray"); axes[r, d].axis("off")
    axes[0, d].set_title(f"{d}")
plt.suptitle("Real MNIST images with their class labels", fontsize=13)
plt.show()'''),
("Conditional discriminator",'''def build_discriminator(in_shape=(28, 28, 1), n_classes=NUM_CLASSES):
    in_label = keras.Input(shape=(1,))
    li = layers.Embedding(n_classes, 50)(in_label)             # label -> 50-d vector
    li = layers.Dense(in_shape[0] * in_shape[1])(li)           # scale up to image size
    li = layers.Reshape((in_shape[0], in_shape[1], 1))(li)
    in_image = keras.Input(shape=in_shape)
    merge = layers.Concatenate()([in_image, li])               # image + label channel (28x28x2)
    x = layers.Conv2D(64, (5, 5), strides=(2, 2), padding="same")(merge)
    x = layers.LeakyReLU(negative_slope=0.2)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Conv2D(128, (5, 5), strides=(2, 2), padding="same")(x)
    x = layers.LeakyReLU(negative_slope=0.2)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Flatten()(x)
    out = layers.Dense(1, activation="sigmoid")(x)
    return keras.Model([in_image, in_label], out, name="discriminator")

discriminator = build_discriminator()
discriminator.summary()'''),
("Conditional generator",'''def build_generator(latent_dim=LATENT_DIM, n_classes=NUM_CLASSES):
    in_label = keras.Input(shape=(1,))
    li = layers.Embedding(n_classes, 50)(in_label)
    li = layers.Dense(7 * 7)(li)
    li = layers.Reshape((7, 7, 1))(li)                         # label as a 7x7 feature map
    in_lat = keras.Input(shape=(latent_dim,))
    gen = layers.Dense(7 * 7 * 128, use_bias=False)(in_lat)
    gen = layers.BatchNormalization()(gen)
    gen = layers.LeakyReLU(negative_slope=0.2)(gen)
    gen = layers.Reshape((7, 7, 128))(gen)
    merge = layers.Concatenate()([gen, li])                    # noise map + label map (7x7x129)
    x = layers.Conv2DTranspose(64, (5, 5), strides=(1, 1), padding="same", use_bias=False)(merge)
    x = layers.BatchNormalization()(x)
    x = layers.LeakyReLU(negative_slope=0.2)(x)                # 7x7x64
    x = layers.Conv2DTranspose(32, (5, 5), strides=(2, 2), padding="same", use_bias=False)(x)
    x = layers.BatchNormalization()(x)
    x = layers.LeakyReLU(negative_slope=0.2)(x)                # 14x14x32
    out = layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding="same", activation="tanh")(x)   # 28x28x1
    return keras.Model([in_lat, in_label], out, name="generator")

generator = build_generator()
generator.summary()'''),
("Loss function and optimizers",'''cross_entropy = keras.losses.BinaryCrossentropy()
generator_optimizer = keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5)
discriminator_optimizer = keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5)
print("Loss      : Binary cross-entropy")
print("Optimizer : Adam (learning rate = 0.0002, beta_1 = 0.5) for the generator and the discriminator")'''),
("Conditional training step",'''@tf.function
def train_step(real_imgs, real_labels):
    batch = tf.shape(real_imgs)[0]
    noise = tf.random.normal((batch, LATENT_DIM))
    fake_labels = tf.random.uniform((batch, 1), 0, NUM_CLASSES, dtype=tf.int32)   # random class to generate
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        fake_imgs = generator([noise, fake_labels], training=True)
        real_output = discriminator([real_imgs, real_labels], training=True)
        fake_output = discriminator([fake_imgs, fake_labels], training=True)
        d_real = cross_entropy(tf.ones_like(real_output), real_output)
        d_fake = cross_entropy(tf.zeros_like(fake_output), fake_output)
        d_loss = 0.5 * (d_real + d_fake)
        g_loss = cross_entropy(tf.ones_like(fake_output), fake_output)
    d_grads = disc_tape.gradient(d_loss, discriminator.trainable_variables)
    g_grads = gen_tape.gradient(g_loss, generator.trainable_variables)
    discriminator_optimizer.apply_gradients(zip(d_grads, discriminator.trainable_variables))
    generator_optimizer.apply_gradients(zip(g_grads, generator.trainable_variables))
    return d_real, d_fake, g_loss

print("Conditional training step defined.")'''),
("Train the Conditional GAN",f'''EPOCHS = {EP}
BATCH_SIZE = 128
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train.astype("int32").reshape(-1, 1))).shuffle(60000).batch(BATCH_SIZE, drop_remainder=True)
fixed_noise = np.random.normal(0, 1, (100, LATENT_DIM)).astype("float32")
fixed_labels = np.repeat(np.arange(10), 10).reshape(-1, 1).astype("int32")     # 10 samples for every digit
history = {{"d_real": [], "d_fake": [], "g": []}}
snapshots = {{}}
SNAP_EPOCHS = sorted({{1, EPOCHS // 4, EPOCHS // 2, EPOCHS}})

for epoch in range(1, EPOCHS + 1):
    a, b, c = [], [], []
    for img_batch, lab_batch in dataset:
        d_real, d_fake, g_loss = train_step(img_batch, lab_batch)
        a.append(float(d_real)); b.append(float(d_fake)); c.append(float(g_loss))
    history["d_real"].append(np.mean(a)); history["d_fake"].append(np.mean(b)); history["g"].append(np.mean(c))
    if epoch in SNAP_EPOCHS:
        snapshots[epoch] = generator([fixed_noise, fixed_labels], training=False).numpy()
    if epoch == 1 or epoch % 2 == 0:
        print(f"Epoch {{epoch:>2}}/{{EPOCHS}}  d_loss(real)={{history['d_real'][-1]:.3f}}  d_loss(fake)={{history['d_fake'][-1]:.3f}}  g_loss={{history['g'][-1]:.3f}}")
generator.save("cgan_generator.keras")
print("Conditional GAN training completed. Generator saved.")'''),
("Training curves",'''plt.figure(figsize=(8, 4.2))
plt.plot(history["d_real"], label="Discriminator loss (real)", color="#2ca02c")
plt.plot(history["d_fake"], label="Discriminator loss (fake)", color="#d62728")
plt.plot(history["g"], label="Generator loss", color="#1f77b4")
plt.title("Conditional GAN - training loss"); plt.xlabel("Epoch"); plt.ylabel("Binary cross-entropy"); plt.legend(); plt.grid(alpha=.3)
plt.show()'''),
("Class-controlled generation (progress)",'''fig, axes = plt.subplots(1, len(snapshots), figsize=(3.7 * len(snapshots), 4.2))
for ax, ep in zip(axes, snapshots):
    g = ((snapshots[ep][..., 0] + 1) / 2).reshape(10, 10, 28, 28).transpose(0, 2, 1, 3).reshape(280, 280)
    ax.imshow(g, cmap="gray"); ax.set_title(f"Epoch {ep}"); ax.set_xticks([]); ax.set_yticks(np.arange(14, 280, 28)); ax.set_yticklabels(range(10))
axes[0].set_ylabel("Requested class label")
plt.suptitle("cGAN - rows are the class labels 0-9 given to the generator", fontsize=13)
plt.show()'''),
("Generate digits for the requested labels",'''labels = np.arange(10).reshape(-1, 1).astype("int32")
noise = np.random.normal(0, 1, (10, LATENT_DIM)).astype("float32")
images = (generator([noise, labels], training=False).numpy() + 1) / 2
print("Requested labels :", labels.ravel().tolist())
print("Generated batch  :", images.shape)

fig, axes = plt.subplots(2, 5, figsize=(10, 4.6))
for ax, img, lab in zip(axes.ravel(), images, labels.ravel()):
    ax.imshow(img[:, :, 0], cmap="gray"); ax.set_title(f"Class {lab}"); ax.axis("off")
plt.suptitle("Images generated by the trained cGAN for each class label", fontsize=12)
plt.show()'''),
("Verify that the generated digits obey the label",'''# a small CNN classifier trained on real MNIST is used as an independent judge
(xc, yc), (xt, yt) = keras.datasets.mnist.load_data()
xc = np.expand_dims(xc / 255.0, -1).astype("float32"); xt = np.expand_dims(xt / 255.0, -1).astype("float32")
judge = keras.Sequential([keras.Input((28, 28, 1)), layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(),
                          layers.Conv2D(64, 3, activation="relu"), layers.MaxPooling2D(), layers.Flatten(),
                          layers.Dense(10, activation="softmax")])
judge.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
judge.fit(xc, yc, epochs=2, batch_size=128, verbose=2)
print("Judge accuracy on real MNIST test set : %.2f%%" % (100 * judge.evaluate(xt, yt, verbose=0)[1]))

n = 2000
lab = np.random.randint(0, 10, (n, 1)).astype("int32"); z = np.random.normal(0, 1, (n, LATENT_DIM)).astype("float32")
fake = (generator([z, lab], training=False).numpy() + 1) / 2
pred = judge.predict(fake, verbose=0).argmax(1)
print("Conditional accuracy (generated digit == requested label) : %.2f%%" % (100 * (pred == lab.ravel()).mean()))
for d in range(10):
    m = lab.ravel() == d
    print(f"  class {d}: {100 * (pred[m] == d).mean():6.2f}%   ({m.sum()} images)")'''),
]
if __name__=='__main__':
    run_notebook('exp10',CELLS,'/tmp/claude-0/dl/out','/tmp/claude-0/dl/data')
