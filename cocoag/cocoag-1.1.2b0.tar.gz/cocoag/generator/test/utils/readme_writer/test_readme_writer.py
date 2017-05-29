from cocoag.generator.utils.readme_writer.writer import ReadmeWriter
import os
import pytest


@pytest.fixture
def img_uri():
    return "WWW.TEST.COM"

def test_upsert_new_file(img_uri, tmpdir):
    ReadmeWriter.upsert(directory=tmpdir, img_uri=img_uri)

    new_readme_file = os.path.join(tmpdir, "README.md")
    with open(new_readme_file) as readme_file:
        lines = readme_file.read().splitlines()
        title, equals, cov_img_markdown = lines
        dir_name = os.path.basename(tmpdir)

        assert title == dir_name
        assert equals == ("=" * len(dir_name))
        assert cov_img_markdown == "[![Codecov](WWW.TEST.COM)]()"


def test_upsert_existing_file(img_uri, tmpdir):
    initial_title = "DONT REPLACE ME\n"
    initial_equals = "===============\n"
    initial_cov_markdown = "[![Codecov](WWW.REPLACEME.COM)]()"
    expected_updated_cov_markdown = "[![Codecov](WWW.TEST.COM)]()\n"

    os.chdir(tmpdir)
    with open("README.md", "w") as initial_readme:
        initial_readme.write(initial_title)
        initial_readme.write(initial_equals)
        initial_readme.write(initial_cov_markdown)
    ReadmeWriter.upsert(directory=tmpdir, img_uri=img_uri)

    updated_readme_file_path = os.path.join(tmpdir, "README.md")
    with open(updated_readme_file_path) as updated_readme:
        lines = updated_readme.readlines()
        title, equals, cov_img_markdown = lines

        assert title == initial_title
        assert equals == initial_equals
        assert cov_img_markdown == expected_updated_cov_markdown


def test_append_after_title():
    lines_with_codecov = [
        "LINE1\n",
        "=====\n",
        "[![Codecov](coverage.svg)]()\n",
        "OTHER"
    ]
    lines_without_codecov = [
        "LINE1\n",
        "=====\n",
        "NO_CODE_COV\n",
        "OTHER"
    ]
    expected_lines_with_codecov_out = [
        "LINE1\n",
        "=====\n",
        "NEW_MARKDOWN\n",
        "OTHER"
    ]
    expected_lines_without_codecov_out = [
        "LINE1\n",
        "=====\n",
        "NEW_MARKDOWN\n",
        "NO_CODE_COV\n",
        "OTHER"
    ]
    new_markdown = "NEW_MARKDOWN"
    title_line_index = 1

    assert ReadmeWriter._append_after_title(cov_img_markdown=new_markdown,
                                            lines=lines_with_codecov,
                                            title_line_index=title_line_index) == expected_lines_with_codecov_out

    assert ReadmeWriter._append_after_title(cov_img_markdown=new_markdown,
                                            lines=lines_without_codecov,
                                            title_line_index=title_line_index) == expected_lines_without_codecov_out
