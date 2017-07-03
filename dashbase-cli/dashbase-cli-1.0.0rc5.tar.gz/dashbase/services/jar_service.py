# -*- coding:utf-8 -*-
import os
import time

from dashbase.utils.errors import NotFound


class JarService(object):
    """
    Dashbase Jar Service
    """

    @classmethod
    def _path_to_version(cls, path, type):
        return os.path.basename(path)[10 + len(type):-4]

    @classmethod
    def find_jar_path_by_version(cls, type, home_path, version, exception=False):
        if not version:
            return cls.find_jar_path(type, home_path)
        type = "dashbase-{}".format(type)
        path = os.path.join(home_path, type, "target", "{}-{}.jar".format(type, version))
        if os.path.isfile(path):
            return path
        if exception:
            raise NotFound("Can't find {}-{}.jar.".format(type, version))
        return None

    @classmethod
    def get_jar_name(cls, type, version):
        return "dashbase-{type}-{version}.jar".format(type=type, version=version)

    @classmethod
    def is_dashbase_jar(cls, type, s):
        if s.startswith("dashbase-{}-".format(type)) and s.endswith(".jar"):
            return True
        return False

    @classmethod
    def find_jar_path(cls, type, home_path, exception=False):
        search_dir = os.path.join(home_path, "dashbase-{}".format(type), "target")
        if os.path.isdir(search_dir):
            files = filter(lambda x: cls.is_dashbase_jar(type, x), os.listdir(search_dir))
            files = [os.path.join(search_dir, f) for f in files]  # add path to each file
            if len(files) > 0:
                files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                return files[0]

        if exception:
            raise NotFound("Can't find dashbase-{} jar.".format(type))
        return None

    @classmethod
    def set_default_jar(cls, home, type, version):
        path = os.path.join(home, "dashbase-{}".format(type), "target", cls.get_jar_name(type, version))
        os.utime(path, (time.time(), time.time()))

    @classmethod
    def get_jar_versions(cls, type, home_path, exception=False):
        search_dir = os.path.join(home_path, "dashbase-{}".format(type), "target")
        if os.path.isdir(search_dir):
            files = filter(lambda x: cls.is_dashbase_jar(type, x), os.listdir(search_dir))
            if len(files) > 0:
                results = []
                files = [os.path.join(search_dir, f) for f in files]
                files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                current_file = cls._path_to_version(files[0], type)
                files.sort()
                for file in files:
                    results.append(cls._path_to_version(file, type))
                return results, current_file

        if exception:
            raise NotFound("Can't find dashbase-{} jar.".format(type))
        return None

    @classmethod
    def get_jar_version(cls, type, home_path):
        jar_name = cls.find_jar_path(type, home_path)
        if not jar_name:
            return

        return os.path.basename(jar_name)[10 + len(type):-4]
