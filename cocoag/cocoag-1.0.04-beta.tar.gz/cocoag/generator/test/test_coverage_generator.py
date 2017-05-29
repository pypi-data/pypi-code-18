from cocoag.generator.coverage_generator import CoverageGenerator
from cocoag.generator.settings_prod import GENERATOR_DIR_PATH
from cocoag.generator.settings_prod import S3_DIR_PATH
import logging


def test_place_holder():
    assert CoverageGenerator._place_holder() == "Write tests!"


# TODO: Figure out how to test a file that runs tests. As of now, this results in an infinite loop
# def test_make_badge(badge_outputs):
#     # NOTE: Cannot test associated branch without ensuring that tests are run on a specific branch
#     generator_badge_info = CoverageGenerator._make_badge(directory=GENERATOR_DIR_PATH)
#     logging.debug("generator_badge_info: '{}'".format(generator_badge_info))
#
#     with open(generator_badge_info.file_location, 'r') as gen_badge:
#         d = gen_badge.read()
#         logging.debug(d)
#         assert d == badge_outputs["generator_svg"]
#
#     s3_badge_info = CoverageGenerator._make_badge(directory=S3_DIR_PATH)
#     logging.debug("s3_badge_info: '{}'".format(s3_badge_info))


# def test_make_badge_uses_new_temp_directory():
#     first_run_badge_info = CoverageGenerator._make_badge(directory=GENERATOR_DIR_PATH)
#     second_run_badge_info = CoverageGenerator._make_badge(directory=GENERATOR_DIR_PATH)
#     assert first_run_badge_info.file_location != second_run_badge_info.file_location
