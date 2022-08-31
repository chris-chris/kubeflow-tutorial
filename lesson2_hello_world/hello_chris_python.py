import kfp


def hello_chris_component():
    ret = "Hello Chris!"
    print(ret)
    return ret


@kfp.dsl.pipeline(name="hello-chris-pipeline", description="Hello Chris Pipeline!")
def hello_chris_pipeline():
    hello_chris_op = kfp.components.func_to_container_op(hello_chris_component)
    _ = hello_chris_op()


if __name__ == "__main__":
    from kfp.v2 import compiler
    compiler.Compiler().compile(hello_chris_pipeline, 'hello-chris-pipeline.json')
