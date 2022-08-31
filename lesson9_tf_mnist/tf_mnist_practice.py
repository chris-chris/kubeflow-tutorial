from kfp import dsl
from kfp.components import func_to_container_op, OutputPath, InputPath


def download_dataset(output_dir_path: OutputPath()):
    import tensorflow as tf

    tf.keras.datasets.mnist.load_data(output_dir_path)


def train_model(data_path: InputPath(), model_output: OutputPath()):
    import tensorflow as tf
    import numpy as np
    with np.load(data_path, allow_pickle=True) as f:
        x_train, y_train = f["x_train"], f["y_train"]
        x_test, y_test = f["x_test"], f["y_test"]

    x_train = x_train / 255.0
    x_test = x_test / 255.0

    print(x_train.shape)
    print(y_train.shape)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(256, activation="leaky_relu"),
        tf.keras.layers.Dense(10, activation="softmax")
    ])
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(lr=0.01),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    model.fit(
        x_train, y_train,
    )

    model.evaluate(x_test, y_test)

    model.save(model_output)


@dsl.pipeline(name="tf-mnist-chris-pipeline")
def tf_mnist_pipeline():
    download_dataset_op = func_to_container_op(
        download_dataset, base_image="tensorflow/tensorflow")
    train_model_op = func_to_container_op(
        train_model, base_image="tensorflow/tensorflow")
    train_model_op(download_dataset_op().output)


if __name__ == "__main__":
    from kfp.v2 import compiler
    compiler.Compiler().compile(tf_mnist_pipeline, "tf-mnist-chris-pipeline.json")
