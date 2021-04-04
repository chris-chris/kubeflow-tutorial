#!/usr/bin/env python3
# Copyright 2021 Chris Hoyean Song (sjhshy@gmail.com)
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
from kfp import components

BASE_IMAGE = "python:3.7"
KUBEFLOW_HOST = "http://127.0.0.1:8080/pipeline"


@kfp.dsl.python_component(
    name="hello_world_component",
    description="Print Hello World",
    base_image=BASE_IMAGE
)
def hello_world_component():
    ret = "Hello World!"
    print(ret)
    return ret


hello_world_op = components.func_to_container_op(
    hello_world_component,
    base_image=BASE_IMAGE,
)


@kfp.dsl.pipeline(name="hello_pipeline", description="Hello World Pipeline!")
def hello_world_pipeline():
    _ = hello_world_op()


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        hello_world_pipeline,
        'hello-world-pipeline.zip')
    kfp.Client(host=KUBEFLOW_HOST).create_run_from_pipeline_func(
        hello_world_pipeline,
        arguments={},
        experiment_name="hello-world-experiment")
