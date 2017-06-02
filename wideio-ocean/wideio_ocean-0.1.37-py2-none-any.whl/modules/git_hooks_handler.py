import os


class GitHookHandler(object):
    """
    Automatically links git hooks on new repo or when clone is being performed
    """

    @classmethod
    def on_ocean_start(cls, ocean):
        cls._ocean = ocean

    @classmethod
    def _activate_git_hooks(cls, section, name):
        srvp = cls._ocean._asrc_folder(section, name)
        if os.path.exists(os.path.join(srvp, "scripts", "install_git_hooks.sh")):
            cls._ocean._subprocess_popen("scripts/install_git_hooks.sh", cwd=srvp).communicate()

    @classmethod
    def on_post_clone(cls, name, *args):
        section = cls._ocean._find_section(name)
        cls._activate_git_hooks(section, name)

    @classmethod
    def on_post_repo_create(cls, section, name, *args):
        cls._activate_git_hooks(section, name)
        srvp = cls._ocean._asrc_folder(section, name)
        if os.path.exists(os.path.join(srvp, "scripts", "install_git_hooks.sh")):
            cls._ocean._subprocess_popen("git push --all", cwd=srvp, shell=True).communicate()
            cls._ocean._subprocess_popen("git push --tags", cwd=srvp, shell=True).communicate()

    @classmethod
    def on_post_repo_split(cls, section, name, *args):
        cls._activate_git_hooks(section, name)
        srvp = cls._ocean._asrc_folder(section, name)
        if os.path.exists(os.path.join(srvp, "scripts", "install_git_hooks.sh")):
            cls._ocean._subprocess_popen("git flow release start 1.0.0", cwd=srvp, shell=True).communicate()
            cls._ocean._subprocess_popen("git flow release finish", cwd=srvp, shell=True).communicate()


__handler__ = GitHookHandler
