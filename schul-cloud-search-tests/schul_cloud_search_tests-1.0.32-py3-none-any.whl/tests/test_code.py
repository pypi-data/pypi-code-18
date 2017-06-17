"""
For AGPL compatibility, we want to test the ability to view the code.
This is especially useful if we want to debug the application.
Suppose a test runs locally but not in the container.
There, we need to examine the versions of the tests.

The endpoints are
/source/...
  with listings and files
/source.zip -> /schul_cloud_search_tests.zip
  a zip file of the source code
"""
import requests
from pytest import mark


@mark.skip(reason="TODO")
def test_directories_are_listed():
    """Make sure the files listed to view them."""


@mark.skip(reason="TODO")
def test_can_download_files():
    """"""


@mark.skip(reason="TODO")
def test_can_download_joined_zip_file():
    """"""


@mark.skip(reason="TODO")
def test_listing_links_to_repository():
    pass


@mark.skip(reason="TODO")
def test_source_link_of_search_engine_refers_to_source_endpoint():
    pass

