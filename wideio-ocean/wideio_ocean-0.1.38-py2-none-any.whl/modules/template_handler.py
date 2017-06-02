import logging
import os
import shutil
import uuid


class TemplateHandler(object):
    """
    Automatically removes information related to the template itself from the project.

    This handler also allow to perform various housekeeping operation related to the template project.
    """

    @classmethod
    def on_ocean_start(cls, ocean):
        cls._ocean = ocean

    @classmethod
    def _clean_template(cls, section, name):
        srvp = cls._ocean._asrc_folder(section, name)
        if os.path.exists(os.path.join(srvp, "_template")):
            shutil.rmtree(os.path.join(srvp, "_template"))
        if os.path.exists(os.path.join(srvp, "gitlab-ci.yml")):
            if os.path.exists(os.path.join(srvp, ".gitlab-ci.yml")):
                os.unlink(os.path.join(srvp, ".gitlab-ci.yml"))
            shutil.copy2(os.path.join(srvp, "gitlab-ci.yml"), os.path.join(srvp, ".gitlab-ci.yml"))

    @classmethod
    def on_post_repo_create(cls, section, name, *args):
        cls._clean_template(section, name)

    @classmethod
    def template_update(cls, name, template_name=None, template_version=None, *args):
        section = cls._ocean._find_section(name)
        srvp = cls._ocean._asrc_folder(section, name)

        if template_name is None:
            if os.path.exists(os.path.join(srvp, ".template-project")):
                template_name, template_version = open(os.path.join(srvp, ".template-project")).read().split("#")

        if template_name is None:
            if os.path.exists("setup.py"):
                template_name = "python-project"
                template_version = "2f5d77d5b1c4a1fd3993f85a3806fefc3287d7ee"

        if template_name is None:
            logging.error("Unable to determine repository type - please specify using command line")

        # rm = cls._ocean.RepoManager(cls._ocean)
        # if template_name is not None:
        #    template_url = rm.find_repo("templates/" + template_name)["url"]

        new_template_version = template_version
        # cls._ocean._subprocess_popen("git clone %s %s; rm -rf %s/.git" % (template_url, srvp, srvp), shell=True).communicate()
        # cls._ocean._subprocess_popen("rm -f VERSION CHANGELOG", cwd=srvp, shell=True).communicate()
        # cls._ocean._subprocess_popen("jed README.md", cwd=srvp, shell=True).communicate()

        if new_template_version != template_version:
            o, e = cls._ocean._subprocess_popen("git diff -p %s..%s" % (template_version, new_template_version)).communicate()
            patch_file = "/tmp/tmppatch.%s" % (str(uuid.uuid4()))
            cls._ocean._subprocess_popen("git apply --exclude=_template %s" % (patch_file,)).communicate()
            open(os.path.join(srvp, ".template-project"), "w").write("%s#%s" % (template_name, new_template_version))


__handler__ = TemplateHandler
