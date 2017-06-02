from gitlab import Gitlab

MAX_PER_PAGE = 100


def query_as_needed(f, *args, **kwargs):
    finished = False
    cpage = 1
    per_page = MAX_PER_PAGE
    ares = []
    while not finished:
        kwargs['page'] = cpage
        kwargs['per_page'] = per_page
        res = f(*args, **kwargs)
        finished = (len(res) < MAX_PER_PAGE)
        ares = ares + res
        cpage = cpage + 1
    return ares


class RepoManager(object):
    host = None

    def __init__(self, ocean, host=None):
        self.host = host
        if self.host is None:
            self.host = ocean._get_config("gitlab.host")
            self.gl = Gitlab(self.host, ocean._get_config("gitlab.access_token"))
        else:
            assert False

    def repo_create(self, name, namespace=None, public=False):
        ca = {'name': name, 'visibility_level': 0}
        if namespace:
            ca['namespace_id'] = namespace.id
        if public:
            ca['visibility_level'] = 20
        p = self.gl.projects.create(ca)
        return {'name': p.name, 'namespace': p.namespace.name, 'url': p.ssh_url_to_repo}

    def list_repos(self):
        """List repositories in GITLAB"""
        r = []
        for p in query_as_needed(self.gl.projects.list):
            r.append({'name': p.name, 'namespace': p.namespace.name, 'url': p.ssh_url_to_repo, 'visibility': p.visibility_level})
        return r

    def list_groups(self):
        r = []
        for g in query_as_needed(self.gl.groups.list):
            r.append({'name': g.name, 'id': g.id})
        return r

    def find_group(self, gn):
        for g in query_as_needed(self.gl.groups.list):
            if g.name == gn:
                return g
        raise IndexError(gn)

    def find_repo(self, rn, raw=False):
        gn = None
        if "/" in rn:
            gn, rn = rn.split("/")
        for r in query_as_needed(self.gl.projects.all):
            if r.name == rn and (gn is None or r.namespace.name == gn):
                if raw:
                    return r
                else:
                    return {'name': r.name,
                            'namespace': r.namespace.name,
                            'url': r.ssh_url_to_repo,
                            'visibility': r.visibility_level
                            }
        raise IndexError(rn)

    def list_opened_issues(self, p=None, project=None):
        r = []
        if p is None:
            p = self.gl.issues
        for i in query_as_needed(self.gl.issues.list, state='opened'):
            # print((i.__dict__))
            r.append({'title': i.title,
                      'id': i.id,
                      'iid': i.iid,
                      'milestone': ((i.milestone.due_date, i.milestone.title) if i.milestone else None),
                      'state': i.state,
                      'url': i.web_url,
                      'project': i.web_url.split("/")[-3]
                      }
                     )
        for p in r:
            if (not project) or p["project"] == project:
                print(p)
