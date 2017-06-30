# -*- coding: utf-8 -*-

"""
 (c) 2017 - Copyright Red Hat Inc

 Authors:  The Dream Team
   Pierre-Yves Chibon <pingou@pingoured.fr>
   Ralph Bean <rbean@redhat.com>

"""
from __future__ import print_function

import logging
import os

import dogpile.cache
import pdc_client
import werkzeug

if 'PAGURE_CONFIG' not in os.environ \
        and os.path.exists('/etc/pagure/pagure.cfg'):
    os.environ['PAGURE_CONFIG'] = '/etc/pagure/pagure.cfg'

import pagure  # noqa: E402
from pagure import APP  # noqa: E402
from pagure.lib import model  # noqa: E402
from pagure.lib.git_auth import Gitolite3Auth, _read_file  # noqa: E402

logging.config.dictConfig(APP.config.get('LOGGING') or {'version': 1})
_log = logging.getLogger(__name__)

cache = dogpile.cache.make_region().configure(
    'dogpile.cache.memory',
    expiration_time=600,
)


_blacklist = '''  -    f[0-9][0-9] = @all
  -    epel[0-9] = @all
  -    epel[0-9][0-9] = @all
  -    el[0-9] = @all
  -    olpc[0-9] = @all'''

namespace2pdctype = {
    'rpms': 'rpm',
    'modules': 'module',
    'container': 'container',
}

@cache.cache_on_arguments()
def get_supported_branches(namespace, package):
    default_url = 'https://pdc.fedoraproject.org/rest_api/v1/'
    url = pagure.APP.config.get('PDC_URL', default_url)
    pdc = pdc_client.PDCClient(url, develop=True)
    kwargs = dict(
        global_component=package,
        type=namespace2pdctype[namespace],
        active=True,  # Not EOL.
    )
    branches = pdc.get_paged(pdc['component-branches'], **kwargs)
    return [branch['name'] for branch in branches]


class DistGitoliteAuth(Gitolite3Auth):
    """ A dist-git's gitolite authentication module. """

    @classmethod
    def write_gitolite_acls(
            cls, session, configfile, preconf=None, postconf=None):
        ''' Generate the configuration file for gitolite for all projects
        on the forge.
        '''
        _log.info('Write down the dist-git\'s gitolite configuration file')

        preconfig = None
        if preconf:
            _log.info(
                'Loading the file to include at the top of the generated one')
            preconfig = _read_file(preconf)

        postconfig = None
        if postconf:
            _log.info(
                'Loading the file to include at the end of the generated one')
            postconfig = _read_file(postconf)

        global_pr_only = pagure.APP.config.get('PR_ONLY', False)
        config = []
        groups = {}
        query = session.query(model.Project).order_by(model.Project.id)
        for project in query.all():
            _log.debug('    Processing project: %s', project.fullname)
            for group in project.committer_groups:
                if group.group_name not in groups:
                    groups[group.group_name] = [
                        user.username for user in group.users]

            # Check if the project or the pagure instance enforce the PR
            # only development model.
            pr_only = project.settings.get('pull_request_access_only', False)

            for repos in ['repos', 'requests/']:
                if repos == 'repos':
                    # Do not grant access to project enforcing the PR model
                    if pr_only or (global_pr_only and not project.is_fork):
                        continue
                    repos = ''

                config.append('repo %s%s' % (repos, project.fullname))
                if repos not in ['tickets/', 'requests/']:
                    config.append('  R   = @all')

                access = 'RWC'
                if project.is_fork:
                    access = 'RW+'

                if repos == '':
                    # First, whitelist the supported branches from PDC
                    for branch in get_supported_branches(project.namespace, project.name):
                        config.append('  %s %s = %s' % (access, branch, project.user.user))
                        for user in project.committers:
                            if user != project.user:
                                config.append('  %s = %s' % (access, branch, user.user))

                    # Then, blacklist a pattern over that (after).
                    config.append(_blacklist)

                if project.committer_groups:
                    config.append('  %s+ = @%s' % (access, ' @'.join(
                        [
                            group.group_name
                            for group in project.committer_groups
                        ]
                    )))

                config.append('  %s = %s' % (access, project.user.user))
                for user in project.committers:
                    if user != project.user:
                        config.append('  %s = %s' % (access, user.user))

                for deploykey in project.deploykeys:
                    access = 'R'
                    if deploykey.pushaccess:
                        access = 'RW'
                        if project.is_fork:
                            access = 'RW+'
                    # Note: the replace of / with _ is because gitolite
                    # users can't contain a /. At first, this might look
                    # like deploy keys in a project called
                    # $namespace_$project would give access to the repos of
                    # a project $namespace/$project or vica versa, however
                    # this is NOT the case because we add the deploykey.id
                    # to the end of the deploykey name, which means it is
                    # unique. The project name is solely there to make it
                    # easier to determine what project created the deploykey
                    # for admins.
                    config.append('  %s = deploykey_%s_%s' %
                                  (access,
                                   werkzeug.secure_filename(project.fullname),
                                   deploykey.id))
                config.append('')

        with open(configfile, 'w') as stream:
            if preconfig:
                stream.write(preconfig + '\n')

            for key, users in groups.iteritems():
                stream.write('@%s   = %s\n' % (key, ' '.join(users)))
            stream.write('\n')

            for row in config:
                stream.write(row + '\n')

            if postconfig:
                stream.write(postconfig + '\n')
