# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kfp
from kfp import dsl

BASE_IMAGE = "library/bash:4.4.23"
KUBEFLOW_HOST = "http://127.0.0.1:8080/pipeline"


def echo_op():
    return dsl.ContainerOp(
        name="echo",
        image=BASE_IMAGE,
        command=["sh", "-c"],
        arguments=['echo "hello world"'],
    )


@dsl.pipeline(name="hello-world-bash-pipeline", description="A hello world pipeline.")
def hello_world_bash_pipeline():
    echo_task = echo_op()


if __name__ == "__main__":
    from kfp.v2 import compiler
    compiler.Compiler().compile(hello_world_bash_pipeline,'hello-world-bash-pipeline.json')
    # kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
    #     hello_world_bash_pipeline,
    #     arguments={},
    #     experiment_name="hello-world-bash-experiment",
    # )
