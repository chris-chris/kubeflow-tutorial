from kfp import dsl
from kfp.components import (
    create_component_from_func,
    InputPath,
    OutputPath
)


@create_component_from_func
def produce_dir_with_files_python_op(
        output_dir_path: OutputPath(),
        num_files: int = 20):
    import os
    os.makedirs(output_dir_path, exist_ok=True)
    for i in range(num_files):
        file_path = os.path.join(output_dir_path, f"{i}.txt")
        with open(file_path, 'w') as f:
            f.write(str(i))


@create_component_from_func
def list_dir_files_python_op(input_dir_path: InputPath()):
    import os
    dir_items = os.listdir(input_dir_path)
    for dir_item in dir_items:
        print(dir_item)
        with open(os.path.join(input_dir_path, dir_item), 'r') as f:
            print(f.read())


@dsl.pipeline(name="file-passing-pipeline")
def file_passing_pipeline():
    produce_files_task = produce_dir_with_files_python_op(num_files=5)
    list_dir_files_python_op(input_dir=produce_files_task.output)


if __name__ == "__main__":
    from kfp.v2 import compiler
    compiler.Compiler().compile(file_passing_pipeline, "file-passing-pipeline.json")
