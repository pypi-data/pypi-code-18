
import distutils
import json
import os
import tempfile
import traceback

import pip
import pkg_resources
from setuptools.package_index import PackageIndex

from integration_pip_inspector.BlackDuckPackage import BlackDuckPackage
from integration_pip_inspector.FileHandler import *
from integration_pip_inspector.LogHandler import *
from integration_pip_inspector.TreeHandler import TreeHandler


try:
    import configparser
except:
    from six.moves import configparser


class BlackDuckCore(object):

    config = None

    project_name = None
    project_version = None

    fail = False
    fail_on_match = False

    def __init__(self, black_duck_config):
        self.config = black_duck_config
        self.project_name = black_duck_config.project_name
        self.project_version = black_duck_config.project_version_name
        self.fail = not black_duck_config.ignore_failure

    def run(self):
        try:
            return self.execute()
        except Exception as e:
            error(message=e, exit=self.fail)
        return None

    def execute(self):
        info("Gathering dependencies")

        if self.project_name is None or self.project_version is None:
            error(error("Project name or version is not set", exit=self.fail))

        project_av = self.project_name + "==" + self.project_version
        pkgs = get_raw_dependencies(project_av, self.fail_on_match)
        if pkgs == []:
            error(project_av + " does not appear to be installed")

        pkg = pkgs.pop(0)  # The first dependency is itself
        pkg_dependencies = get_dependencies(pkg, self.fail_on_match)
        optional = self._fetch_optional_requirements()
        if optional:
            pkg_dependencies.extend(optional)

        info("Building dependency tree")

        tree = BlackDuckPackage(pkg.key, pkg.project_name,
                                pkg.version, pkg_dependencies)

        tree_handler = TreeHandler(tree)
        tree_list = tree_handler.render_tree(self.config.output_path)
        info("Generated tree")
        return tree

    def _fetch_optional_requirements(self):
        requirements = self.config.requirements_file_path

        # If the user wants to include their requirements.txt file
        if requirements:
            try:
                assert os.path.exists(requirements), (
                    "The requirements file %s does not exist." % requirements)
                requirements = pip.req.parse_requirements(
                    requirements, session=pip.download.PipSession())
            except:
                error(message="Requirements file @ " + requirements +
                      " was not found", exit=self.fail)

        if requirements is None:
            return None

        pkg_dependencies = []
        for req in requirements:
            req_package = get_best(req.req, self.fail)
            if req_package:
                found = False
                for existing in pkg_dependencies:
                    if existing.key.lower() == req_package.key.lower():
                        found = True
                        break
                if not found:
                    req_dependencies = get_dependencies(
                        req_package, self.fail_on_match)
                    key = req_package.key
                    name = req_package.project_name
                    version = req_package.version
                    dependencies = req_dependencies
                    req_package = BlackDuckPackage(
                        key, name, version, dependencies)
                    pkg_dependencies.append(req_package)

        return pkg_dependencies


def get_raw_dependencies(package, fail_on_match):
    dependencies = []
    try:
        project_requirement = pkg_resources.Requirement.parse(package)

        environment = pkg_resources.Environment(
            distutils.sysconfig.get_python_lib(),
            platform=None,
            python=None
        )

        dependencies = pkg_resources.working_set.resolve(
            [project_requirement], env=environment)
    except Exception as e:
        m = "No matching packages found for declared dependency: "
        error(message=m + package, exit=fail_on_match)
    return dependencies


def get_dependencies(pkg, fail_on_match):
    dependencies = []

    for dependency in pkg.requires():
        pkg = get_best(dependency, fail_on_match)
        if pkg:
            pkg_dependencies = get_dependencies(pkg, fail_on_match)
            package = BlackDuckPackage(
                pkg.key, pkg.project_name, pkg.version, pkg_dependencies)
            dependencies.append(package)
    return dependencies


# Can take in an object with a key or just a string
def get_best(dependency, fail_on_match):
    installed = pip.get_installed_distributions(
        local_only=False, user_only=False)

    if hasattr(dependency, "key"):
        dependency = dependency.key
    elif hasattr(dependency, "name"):
        dependency = dependency.name

    for pkg in installed:
        if pkg.key.lower() == dependency.lower():
            return pkg
    m = "No matching packages found for declared dependency: "
    error(message=m + dependency, exit=fail_on_match)
    return None
