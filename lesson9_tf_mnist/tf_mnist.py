import kfp
from kfp import dsl
from kfp.components import func_to_container_op, OutputPath, InputPath

EXPERIMENT_NAME = 'Train TF MNIST'        # Name of the experiment in the UI
KUBEFLOW_HOST = "http://127.0.0.1:8080/pipeline"


def download_mnist(output_dir_path: OutputPath()):
    import tensorflow as tf

    tf.keras.datasets.mnist.load_data(output_dir_path)


def train_mnist(data_path: InputPath(), model_output: OutputPath()):
    import tensorflow as tf
    import numpy as np
    with np.load(data_path, allow_pickle=True) as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']
    print(x_train.shape)
    print(y_train.shape)

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

    model.save(model_output)


@dsl.pipeline(name="tf-mnist-pipeline")
def tf_mnist_pipeline():
    download_op = func_to_container_op(
        download_mnist, base_image="tensorflow/tensorflow")
    train_mnist_op = func_to_container_op(
        train_mnist, base_image="tensorflow/tensorflow")
    train_mnist_op(download_op().output)


if __name__ == '__main__':
    import kfp.compiler as compiler
    # compiler.Compiler().compile(tf_mnist_pipeline, __file__ + '.zip')
    # kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
    #     tf_mnist_pipeline,
    #     arguments={},
    #     experiment_name=EXPERIMENT_NAME)

    from kfp.v2 import compiler
    compiler.Compiler().compile(tf_mnist_pipeline, "tf-mnist-pipeline.json")
