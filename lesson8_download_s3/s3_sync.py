import kfp
from kfp import dsl
from kfp.aws import use_aws_secret


EXPERIMENT_NAME = 'AWS S3 sync'        # Name of the experiment in the UI
KUBEFLOW_HOST = "http://127.0.0.1:8080/pipeline"


def s3_sync():
    return kfp.dsl.ContainerOp(
        name="s3_sync",
        image="amazon/aws-cli:latest",
        command=["aws", "s3", "sync", "s3://inside-private/dataset/casa_grande/2021-04-01/", "/tmp"],
        file_outputs={
            "data": "/tmp"
        }
    )


@dsl.pipeline(name="s3_sync_pipeline", description="s3 sync pipeline.")
def s3_sync_pipeline():
    echo_task = s3_sync().apply(use_aws_secret('aws-secret', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'))


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(s3_sync_pipeline, __file__ + ".zip")
    kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
        s3_sync_pipeline,
        arguments={},
        experiment_name=EXPERIMENT_NAME,
    )
