from snek.core import shell_command


def update():
    """
    Pull all changes from the git repo to local
    """
    shell_command('git submodule update --recursive --remote')
    shell_command('git add .')
    shell_command('git commit -m "Update"')
    shell_command('git pull')
    shell_command('git push')
