import logging
import os
from pathlib import Path


class ReadmeWriter(object):
    _img_text = "[![Codecov]({uri})]()"
    _TEMP_README_FILE_NAME = "_TEMP_README.md"

    @classmethod
    def upsert(cls, directory: str, img_uri: str):
        cov_img_markdown = cls._gen_cov_img_markdown(img_uri=img_uri)
        potential_location = os.path.join(directory, "README.md")
        readme_file = Path(potential_location)
        logging.debug("Checking readme_file: {}".format(readme_file))
        if readme_file.exists():
            if readme_file.is_dir():
                # TODO: Custom exception
                raise Exception("Dir exists!")
            else:
                cls._handle_existing_file(cov_img_markdown=cov_img_markdown, readme_file=readme_file)

        else:
            title = os.path.basename(directory)
            logging.debug("Using title '{}' for new README.md".format(title))
            cls._handle_new_file(cov_img_markdown=cov_img_markdown, readme_file=readme_file, title=title)

    @classmethod
    def _append_after_title(cls, cov_img_markdown: str, lines: list, title_line_index: int) -> list:
        # TODO: Deduplicate
        code_cov_index = cls._get_code_cov_line(lines=lines)
        if code_cov_index > -1:
            lines[code_cov_index] = (cov_img_markdown + "\n")
            return lines
        else:
            ins_index = title_line_index + 1
            lines.insert(ins_index, (cov_img_markdown + "\n"))
            return lines

    @classmethod
    def _append_top(cls, cov_img_markdown: str, lines: list) -> list:
        # TODO: Deduplicate
        code_cov_index = cls._get_code_cov_line(lines=lines)
        if code_cov_index > -1:
            lines[code_cov_index] = (cov_img_markdown + "\n")
            return lines
        else:
            lines.insert(0, cov_img_markdown)
            return lines

    @classmethod
    def _gen_cov_img_markdown(cls, img_uri: str) -> str:
        return cls._img_text.format(uri=img_uri)

    @classmethod
    def _get_code_cov_line(cls, lines: list) -> int:
        for index, line in enumerate(lines):
            if line.startswith("[![Codecov]"):
                return index
        return -1

    @classmethod
    def _get_title_line(cls, lines: list) -> int:
        # Check for the first line that starts with "="
        for index, line in enumerate(lines):
            if line.startswith("="):
                return index
        return -1

    @classmethod
    def _handle_existing_file(cls, cov_img_markdown: str, readme_file: Path):
        with readme_file.open(mode='r') as existing_file:
            lines = existing_file.readlines()
            title_line = cls._get_title_line(lines=lines)
            if title_line > -1:
                new_lines = cls._append_after_title(cov_img_markdown=cov_img_markdown, lines=lines,
                                                    title_line_index=title_line)
            else:
                new_lines = cls._append_top(cov_img_markdown=cov_img_markdown, lines=lines)

            with open(cls._TEMP_README_FILE_NAME, "w") as temp_readme:
                to_write = "".join(new_lines)
                logging.debug("Writing to {path}:\n{to_write}".format(path=readme_file, to_write=to_write))
                temp_readme.write(to_write)
        os.rename(cls._TEMP_README_FILE_NAME, str(readme_file))

    @classmethod
    def _handle_new_file(cls, cov_img_markdown: str, readme_file: Path, title: str):
        with readme_file.open(mode='w') as rd_file:
            below_title = ("=" * len(title))
            to_write = "\n".join([title, below_title, cov_img_markdown])
            logging.debug("Writing to {path}:\n{to_write}".format(path=readme_file, to_write=to_write))
            rd_file.write(to_write)