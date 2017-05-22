from MoinMoin.security import Permissions

edit_whitelist = set([
    'FrontPage',
])

class CustomSecurityPolicy(Permissions): 
    '''
    Custom permissions defaults (in addition to whatever ACLs are in play for the page)
    '''
    def write(self, pagename, **kw):
        return (
            self.request.user.valid and
            Permissions.__getattr__(self, 'write')(pagename) and
            (
                # draft pages are editable
                pagename.endswith('_DRAFT') or
                # help and group pages are editable by admins
                (
                    self.request.user.name in self.request.cfg.superuser and
                    (pagename.startswith('Help') or pagename.endswith('Group'))
                ) or
                # publisher agent can edit any
                self.request.user.name == self.request.cfg.publisher_agent_user or
                # specific pages are editable
                pagename in edit_whitelist
            )
        )
