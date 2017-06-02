import os
import types
import importlib.util


def get_all_python_files_path_in_directory():
    root = '/home/dmytryi/cleannaming/cleannaming/cleannaming'

    python_files_in_project = []

    for path, sub_directory, files in os.walk(root):
        for name in files:
            if name.endswith('.py') and not (name.startswith('__') or name.startswith('_')):
                python_files_in_project.append(os.path.join(path, name))

    return python_files_in_project

def all_current_imported_modules():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__

def import_module_by_name_and_path(file_name, file_path):
    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module_variables = get_module_variables(module)
    return module_variables

def get_module_variables(module):
    variables = {}

    for variable, statement in module.__dict__.items():
        if not (variable.startswith('__') or variable.startswith('_')):
            if variable not in all_current_imported_modules():
                variables[variable] = statement

    return variables

def hello():
    print('main!')

if __name__ == "__main__":
    hello()
