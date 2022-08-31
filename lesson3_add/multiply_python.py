from kfp import dsl
from kfp import components

BASE_IMAGE = "python:3.9"


@dsl.python_component(
    name="mulitply-op",
    base_image=BASE_IMAGE,
)
def multiply(x: float, y: float) -> float:
    """Multiplies two numbers"""
    print(x, "*", y, "=", x * y)
    return x * y


multiply_op = components.func_to_container_op(
    multiply,
    base_image=BASE_IMAGE,
)


@dsl.pipeline(
    name="multiplication-pipeline",
    description="",
)
def multiplication_pipeline(
    x: float = 2,
    y: float = 3,
):
    multiply_task = multiply_op(x, y)

    multiply2_task = multiply_op(3, y)

    multiply3_task = multiply_op(multiply_task.output, multiply2_task.output)

    multiply4_task = multiply_op(multiply3_task.output, 10)


if __name__ == "__main__":
    from kfp.v2 import compiler
    compiler.Compiler().compile(multiplication_pipeline, "multiplication-pipeline.json")
