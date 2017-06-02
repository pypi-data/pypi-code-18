import json
import logging
import os
import shutil


class MixIn(object):
    """
    Allows to create repository and to register them to a central repo.
    """

    @classmethod
    def repo_create(cls, section, name, template_name=None, public=False, customer_name=None, *options):
        """
        Creates a new repository and project (eventually using a template).

        repo_create section name [template_name] [public]
        """
        # create the repo
        if customer_name is None:
            customer_name = "wideio"

        rm = cls._ocean.RepoManager(cls._ocean)

        g = rm.find_group(section)

        try:
            rm.find_repo(section + "/" + name)
            print("There already exists a repository with that name")
            return -1
        except IndexError:
            pass
        if template_name is not None:
            template_url = rm.find_repo("templates/" + template_name)["url"]
        srvp = cls._ocean._asrc_folder(section, name)
        if os.path.exists(srvp):
            raise ValueError("The target path %s does already exists !\n" % (srvp,))

        result = rm.repo_create(name, g, public)

        url = result["url"]

        if template_name is None:
            # create src directory
            if not os.path.exists(srvp):
                os.makedirs(srvp)
        else:
            cls._ocean._subprocess_popen("git clone %s %s; rm -rf %s/.git" % (template_url, srvp, srvp),
                                         shell=True).communicate()
            cls._ocean._subprocess_popen("rm -f VERSION CHANGELOG", cwd=srvp, shell=True).communicate()
            cls._ocean._subprocess_popen("jed README.md", cwd=srvp, shell=True).communicate()

        # print (srvp, url)
        cls._ocean._subprocess_popen("git init .; git add .; git commit -a -m 'initial commit'", shell=True,
                                     cwd=srvp).communicate()
        cls._ocean._subprocess_popen("git remote add origin %s" % (url,), shell=True, cwd=srvp).communicate()

        # add to the manifest
        cls._ocean.omanifest.setdefault(section, {}).setdefault(name, {})["url"] = url
        open(cls._ocean.MANIFEST_PATH, "wb").write(json.dumps(cls._ocean.omanifest,
                                                              indent=2,
                                                              sort_keys=True
                                                              )
                                                   )

    @classmethod
    def repo_split(cls, section, name, path=None, *args, **kwargs):
        """
        Separate a directory into new repo and relink it as submodule.

        NOTE: EXPERIMENTAL CODE!
        This is designed to be useful to modularise software.
        """
        if path is None:
            path = os.getcwd()

        path = os.path.abspath(path)

        if not os.path.isdir(path):
            raise Exception("Path must be existent : " + path)

        sp = path.split("/")

        for ml in range(len(sp)):
            if os.path.isdir(os.path.join("/".join(sp[:-ml]), ".git")):
                break

        if not (os.path.isdir(os.path.join("/".join(sp[:-ml]), ".git"))):
            raise Exception("Could not find source repository.")

        new_src_dir = cls._ocean._asrc_folder(section, name)

        if os.path.isdir(new_src_dir):
            raise Exception("New repo must be non-existent:" + new_src_dir)

        new_src_dir_tmp = new_src_dir + ".tmp"

        if os.path.isdir(new_src_dir_tmp):
            raise Exception("New repo must be non-existent:" + new_src_dir_tmp)

        print ("cproject dir:" + "/".join(sp[:-ml]))
        print ("relative sub dir:" + "/".join(sp[-ml:]))
        print ("new_src_dir_tmp:" + new_src_dir_tmp)

        os.makedirs(new_src_dir_tmp)

        cls._ocean._subprocess_popen("git init .", shell=True, cwd=new_src_dir_tmp).communicate()
        cls._ocean._subprocess_popen("git remote add origin file://%s" % ("/".join(sp[:-ml]),), shell=True,
                                     cwd=new_src_dir_tmp).communicate()
        cls._ocean._subprocess_popen("git config core.sparsecheckout true", cwd=new_src_dir_tmp,
                                     shell=True).communicate()
        try:
            os.makedirs(os.path.join(new_src_dir_tmp, ".git", "info"))
        except BaseException:
            pass
        open(os.path.join(new_src_dir_tmp, ".git", "info", "sparse-checkout"), "a").write("/".join(sp[-ml:]) + "/")
        cls._ocean._subprocess_popen("git pull origin master", shell=True, cwd=new_src_dir_tmp).communicate()
        cls._ocean._subprocess_popen("rm -rf .git", shell=True, cwd=new_src_dir_tmp)

        # create new project
        cls._ocean._call_with_eh("repo_create", section, name, *args, **kwargs)
        srcd = os.path.join(new_src_dir_tmp, "/".join(sp[-ml:]))
        logging.info("recopying file from " + srcd)
        for fn in os.listdir(srcd):
            if fn == ".git":
                continue
            if os.path.isdir(os.path.join(srcd, fn)):
                shutil.copytree(os.path.join(srcd, fn), os.path.join(new_src_dir, fn))
            else:
                open(os.path.join(new_src_dir, fn), "wb").write(open(os.path.join(srcd, fn), "rb").read())
        logging.info("adding the files from " + srcd)
        cls._ocean._subprocess_popen("git status --porcelain | grep \"^\\?\\?\" | cut -c 4- | xargs git add",
                                     shell=True, cwd=new_src_dir).communicate()
        cls._ocean._subprocess_popen("git commit -a -n -m 'importing files from previous project'; git push --all",
                                     shell=True, cwd=new_src_dir).communicate()
        shutil.rmtree(new_src_dir_tmp)

        # remove from current project
        # os.system("find . | xargs git rm --cached")

        # find root of current repo and relative name
        # cls._ocean._subprocess_popen("git sumodule add %s %s"%(repo, "/".join(sp[-ml:]), path="/".join(sp[:-ml])).communicate())

    @classmethod
    def repo_rename(cls, section, name, newname, *options):
        """
        Rename a repository.
        """

        assert (False)  # Not implemented
        # create the repo
        repomgr = cls._ocean.RepoManager(cls._ocean)
        repomgr.rename_repo(section, name, newname)

        # create / link directory
        open(os.path.join(cls.MANIFEST_PATH, "manifest.json"), "wb").write(json.dumps(cls.omanifest,
                                                                                      indent=2,
                                                                                      sort_keys=True))

    @classmethod
    def repo_list(cls, *options):
        """
        List repositories in the registry.
        """
        repomgr = cls._ocean.RepoManager(cls._ocean)
        return repomgr.list_repos()

    @classmethod
    def repo_groups_list(cls, *options):
        """
        List repository groups in the registry.
        """
        repomgr = cls._ocean.RepoManager(cls._ocean)
        return repomgr.list_groups()

    @classmethod
    def repo_find(cls, rn, *options):
        """
        Find the the repository associated with a project name.
        """
        repomgr = cls._ocean.RepoManager(cls._ocean)
        return repomgr.find_repo(rn)

    @classmethod
    def repo_issues(cls, rn, *options):
        """
        List the issues associated with a repo.
        """
        repomgr = cls._ocean.RepoManager(cls._ocean)
        return repomgr.list_opened_issues(None, rn)

    @classmethod
    def repo_manifest(cls):
        """
        Create a manifest for all the repositories accessible with
        the repo manager.
        """
        repomgr = cls._ocean.RepoManager(cls._ocean)
        nmanifest = {}
        for r in repomgr.list_repos():
            nmanifest.setdefault(r["namespace"], {}).setdefault(r["name"], {})["url"] = r["url"]
        return json.dumps(nmanifest, indent=2, sort_keys=True)
