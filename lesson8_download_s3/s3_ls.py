import kfp
from kfp import dsl
from kfp.aws import use_aws_secret


EXPERIMENT_NAME = 'AWS S3 ls'        # Name of the experiment in the UI
KUBEFLOW_HOST = "http://127.0.0.1:8080/pipeline"


def s3_ls():
    return kfp.dsl.ContainerOp(
        name="s3_ls",
        image="amazon/aws-cli:latest",
        command=["aws", "s3", "ls"],
    )


@dsl.pipeline(name="s3_ls_pipeline", description="s3 ls pipeline.")
def s3_ls_pipeline():
    echo_task = s3_ls().apply(use_aws_secret('aws-secret', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'))


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(s3_ls_pipeline, __file__ + ".zip")
    kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
        s3_ls_pipeline,
        arguments={},
        experiment_name=EXPERIMENT_NAME,
    )
