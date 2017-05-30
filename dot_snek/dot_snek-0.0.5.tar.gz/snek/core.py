from codecs import decode
from os import link
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, call


def __base_cond(path: Path):
    """
    Base condition for all link operations.
    :param path: the base file/dir path
    :return: True if the base file/dir name passed the base condition check
    """
    return path.name.lower() not in (
        '.git', '.gitignore', '.gitkeep', '.directory', '.gitmodules',
        '.github', '.travis.yml'
    )


def shell_command(cmd: str, print_output=True):
    """
    Run a shell command and prints its output to stdout
    :param cmd: the shell command
    :param print_output: if True this will print the output, if false this will
    yield the output
    """
    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    lines = []
    for line in process.stdout:
        res = decode(line)
        if print_output:
            print(res)
        else:
            lines.append(res)
    return lines


def create_link(src: Path, dest: Path):
    """
    Create a link from the src file to the dest directory

    :param src: the src file path

    :param dest: the dest dir path.
    """
    if not dest.parent.is_dir():
        dest.parent.mkdir(parents=True, exist_ok=True)
    assert src.is_file()
    assert dest.parent.is_dir()
    assert not dest.is_dir()
    if dest.exists():
        dest.unlink()
    link(src.absolute(), dest.absolute())
    dest.resolve()


def __link_all(src: Path, dest: Path):
    """
    Recursively link all files under a the root path to the dest path
    :param src: the source path
    :param dest: the dest path
    """
    if __base_cond(src):
        if src.is_file():
            print('Linking {} to {}'.format(src, dest))
            create_link(src, dest)
        elif src.is_dir():
            for sub in src.iterdir():
                __link_all(src.joinpath(sub), dest.joinpath(sub.name))


def link_all(src: Path, dest: Path):
    """
    Link all your dot files from source to dest
    :param src: the source path
    :param dest: the dest path
    """
    __link_all(src, dest)
    print('Done!')
