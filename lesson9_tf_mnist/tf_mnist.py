from typing import NamedTuple

import numpy as np
import kfp
from kfp import dsl, components

EXPERIMENT_NAME = 'Train TF MNIST'        # Name of the experiment in the UI
KUBEFLOW_HOST = "http://127.0.0.1:8080/pipeline"


def download_mnist() -> NamedTuple(
    'MNISTData',
    [
        ('x_train', np.ndarray),
        ('y_train', np.ndarray),
        ('x_test', np.ndarray),
        ('y_test', np.ndarray),
    ]):
    import tensorflow as tf

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    from collections import namedtuple
    mnist_data = namedtuple('MNISTData', ['x_train', 'y_train', 'x_test', 'y_test'])
    return mnist_data(x_train, y_train, x_test, y_test)


def train_mnist(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray):
    import tensorflow as tf
    print(x_train)
    print(y_train)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    model.fit(
        x_train, y_train,
    )
    model.evaluate(x_test, y_test)

    model.save("/tmp")

    return "/tmp"


def tf_mnist_pipeline():
    # Convert the function to a pipeline operation.
    download_mnist_op = components.func_to_container_op(
        download_mnist,
        base_image="tensorflow/tensorflow",
    )
    train_mnist_op = components.func_to_container_op(
        train_mnist,
        base_image="tensorflow/tensorflow"
    )

    download_mnist_op = download_mnist_op()
    _ = train_mnist_op(download_mnist_op.outputs["x_train"], download_mnist_op.outputs["y_train"],
                       download_mnist_op.outputs["x_test"], download_mnist_op.outputs["y_test"])


if __name__ == '__main__':
    kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
        tf_mnist_pipeline,
        arguments={},
        experiment_name=EXPERIMENT_NAME)
