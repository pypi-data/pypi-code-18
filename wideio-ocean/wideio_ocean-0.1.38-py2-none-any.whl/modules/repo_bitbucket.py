import os
import webbrowser

try:
    from bitbucket.bitbucket import Bitbucket
except BaseException:
    Bitbucket = None


class RepoManager(object):
    def __init__(self):
        username, password = open(os.path.expanduser("~/.bitbucket.account")).read().strip().split(":")
        self.bb = Bitbucket(username, password)

    def repo_create(self, slug_name):
        url = "git@bitbucket.org:wideio/%s.git" % (slug_name,)
        success, result = self.bb.repository.create(slug_name)
        assert success
        webbrowser.open("https://bitbucket.org/wideio-admin/%s/admin/transfer" % (slug_name,))
        result['owner'] = "wideio"
        self.bb.repository.update(result)

        return result, url

    def rename_repo(self, name):
        success, result = self.bb.repository.get(name)
        assert success

        success, result = self.bb.repository.update(name, result)
        assert success

    def list_repos(self):
        res = []
        success, result = self.bb.repository.all()
        for r in sorted(result, key=lambda x: x["name"]):
            res.append({'name': r["name"], 'visibility': ("private" if r["is_private"] else "public"),
                        'updated': r["last_updated"]})
        success, result = self.bb.repository.all(username="wideio")
        for r in sorted(result, key=lambda x: x["name"]):
            res.append({'name': r["name"], 'visibility': ("private" if r["is_private"] else "public"),
                        'updated': r["last_updated"]})
        return res
