from cocoag.configuration.config import config
from cocoag.generator.utils.readme_writer.writer import ReadmeWriter
from cocoag.s3.s3_client import S3Client
from collections import namedtuple
import logging
import os
import pprint
import re
import subprocess
from typing import NamedTuple

BadgeInfo = NamedTuple('BadgeInfo', [("associated_branch", str), ("file_location", str)])

CoverageGeneratorConfig = NamedTuple('CoverageGeneratorConfig',
                                     [("bucket_root", str), ("project_root", str), ("sub_directories", list)])


class CoverageGenerator(object):
    # Values from config
    _package_root = config.get("general", "package_root")
    _svg_output_file_name = config.get("project", "svg_output_file_name")

    _badge_output_location = os.path.join(_package_root, _svg_output_file_name)
    _BadgeInfo = namedtuple("BadgeInfo", ["associated_branch", "file_location"])
    _CoverageGeneratorConfig = namedtuple("CoverageGeneratorConfig", ["bucket_root", "project_root", "sub_directories"])
    _current_branch_regex = re.compile(r"(CURRENT_BRANCH:\s)(.*)", re.MULTILINE)

    @classmethod
    def _get_make_badge_args(cls) -> str:
        return "py.test --cache-clear --cov={dir};" + \
               "coverage-badge -o {badge_output_location} -f;" + \
               "echo \"CURRENT_BRANCH: $(git rev-parse --abbrev-ref HEAD)\""

    @classmethod
    def generate(cls):
        ccg = cls._CoverageGeneratorConfig(bucket_root=config.get("s3", "bucket_root"),
                                           project_root=config.get("project", "root_dir"),
                                           sub_directories=config.getlist("generator", "subdirectories"))
        for sub_directory in ccg.sub_directories:
            cls._process(active_sub_directory=sub_directory, config=ccg)

    @classmethod
    def _add_to_readme(cls, directory: str, img_uri: str):
        logging.debug("_add_to_readme: directory -> {directory}, img_uri -> {img_uri}".format(
                        directory=directory, img_uri=img_uri))
        ReadmeWriter.upsert(directory=directory, img_uri=img_uri)

    @classmethod
    def _make_badge(cls, directory: str) -> BadgeInfo:
        # Run pytest with coverage and make the badge
        os.chdir(cls._package_root)
        logging.debug("_make_badge using badge_output_location: '{}'".format(cls._badge_output_location))
        args = cls._get_make_badge_args().format(badge_output_location=cls._badge_output_location, dir=directory)
        logging.debug("_make_badge using args: '{}'".format(pprint.pformat(args)))
        # TODO: Exception handling
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        # Get the github branch name
        out = result.stdout.decode('utf-8')
        m = cls._current_branch_regex.findall(out)
        branch_name = m[0][1]

        return cls._BadgeInfo(associated_branch=branch_name, file_location=cls._badge_output_location)

    @classmethod
    def _place_holder(cls):
        return "Write tests!"

    @classmethod
    def _process(cls, active_sub_directory: str, config: CoverageGeneratorConfig):
        full_directory = os.path.join(config.project_root, active_sub_directory)
        badge_info = cls._make_badge(directory=full_directory)
        badge_uri = cls._upload_badge(badge_info=badge_info, config=config, sub_directory=active_sub_directory)
        cls._add_to_readme(directory=full_directory, img_uri=badge_uri)

    @classmethod
    def _upload_badge(cls, badge_info: BadgeInfo, config: CoverageGeneratorConfig, sub_directory: str) -> str:
        logging.debug("_upload_badge using args:\n"
                      "badge_info ->  {badge_info}, config ->  {config}, , sub_directory ->  {sub_directory}, ".format(
                       badge_info=badge_info, config=config, sub_directory=sub_directory))

        root_key_path = "badges/coverage/{branch_name}/{dir}".format(branch_name=badge_info.associated_branch,
                                                                     dir=sub_directory)
        full_key_path = os.path.join(root_key_path, cls._svg_output_file_name)
        logging.debug("full_key_path: '{}'".format(full_key_path))

        with open(badge_info.file_location) as coverage_img:
            data = coverage_img.read()
            S3Client.save(data=data, bucket=config.bucket_root, key_name=full_key_path)

        # Return the location of the uploaded badge
        bucket_location = S3Client.get_bucket_location(bucket=config.bucket_root)
        obj_url_without_location = S3Client.get_obj_url(bucket=config.bucket_root, key_name=full_key_path)
        ins_point = obj_url_without_location.find(".")
        return obj_url_without_location[:ins_point] + "." + bucket_location + obj_url_without_location[ins_point:]