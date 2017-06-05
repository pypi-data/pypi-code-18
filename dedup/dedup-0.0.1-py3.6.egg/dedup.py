import json
import os
import fire
from collections import defaultdict
from dedup.file import File


class FileManager:
    def __init__(self):
        self.__root_path = None
        self.__processed = set()
        self.__hash_to_files = defaultdict(list)

    def __add(self, file):
        if file.path not in self.__processed:
            self.__processed.add(file.path)
            self.__hash_to_files[file.mini_hash].append(file)

    def __scan_directory(self):
        for dirpath, _, filenames in os.walk(self.__root_path):
            for filename in filenames:
                print(' ' * 100, end="\r")
                print("Processing: {}".format(filename[:80]), end="\r")
                path = os.path.join(dirpath, filename)
                self.__add(File(path))
        print(' ' * 100, end="\r")

    def __write_result_to_file(self):
        duplicates = []
        print("Processing Result")
        for k, v in self.__hash_to_files.items():
            if len(v) > 1:
                duplicates.append({"total_size": sum([f.size for f in v]),
                                   "count": len(v),
                                   "mini_hash": k,
                                   "files": [f.info() for f in v]})
        if len(duplicates) == 0:
            print("No duplicate file")
        else:
            print("Writing result to duplicates.json")
            with open('duplicates.json', 'w') as fp:
                duplicates.sort(key=lambda x: -x['total_size'])
                json.dump(duplicates, fp, indent=4, separators=(',', ': '), sort_keys=True)
            print("Done")

    def find(self, path=None):
        if path is None:
            self.__root_path = os.getcwd()
        else:
            self.__root_path = path

        self.__scan_directory()
        self.__write_result_to_file()


def main():
    fire.Fire(FileManager)
