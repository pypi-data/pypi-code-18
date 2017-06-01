import os

FILE_NAME = "dependencyTree.txt"

def get_file_path(file_name, output_path):
    file_path = output_path + "/"
    file_path += file_name
    return file_path


def generate_file(data, file_name, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_file_path = get_file_path(file_name, output_path)
    with open(output_file_path, "w+") as output_file:
        output_file.write(data)
    return output_file_path
