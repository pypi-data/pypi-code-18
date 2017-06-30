import os
import zipfile

def zip_directory(filename, path):
    absolute_filename = os.path.abspath(filename)
    with zipfile.ZipFile(absolute_filename, 'w', zipfile.ZIP_DEFLATED) as zip_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                absolute_filepath = os.path.join(root, file)
                if absolute_filename == absolute_filepath:
                    continue
                zip_handle.write(absolute_filepath, file)
