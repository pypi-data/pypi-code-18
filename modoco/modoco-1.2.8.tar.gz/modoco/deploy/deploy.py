# coding: utf-8
import glob
import os
import sys
from MoinMoin.web.contexts import ScriptContext
from MoinMoin import user, packages
from MoinMoin.Page import Page
from MoinMoin.action import language_setup
from werkzeug import MultiDict, CombinedMultiDict
import util
import shutil

def run():
    '''
    Do the actual work of deployment
    '''
    request = ScriptContext()
    configfile = os.path.join(request.cfg.wikiconfig_dir, 'wikiconfig.py')

    # create the PublisherAgent bot user
    publisher_agent_name = request.cfg.publisher_agent_user
    publisher_agent_pwd = util.pwd_gen(16)
    with open(configfile, 'a') as fh:
        fh.write('''
    # password for publisher agent - do NOT remove from this file!
    publisher_agent_pwd = "%s"\n''' % publisher_agent_pwd)
    util.create_user(request, publisher_agent_name, publisher_agent_pwd)

    # create the superuser
    superuser_name = request.cfg.superuser[0]
    superuser_pwd = util.pwd_gen(16)
    with open(configfile, 'a') as fh:
        fh.write('''
    # password for default superuser - note it down and remove from this file
    superuser0_pwd = "%s"\n''' % superuser_pwd)
    superuser = util.create_user(request, superuser_name, superuser_pwd)

    # install packaged things (requires superuser)
    this_dir = os.path.dirname(os.path.realpath(__file__))
    package_dir = os.path.join(this_dir, 'moin_package')
    zipfile = shutil.make_archive('package', 'zip', package_dir)
    request.user = superuser
    package = packages.ZipPackage(request, zipfile)
    if not package.installPackage():
        print(package.msg)
        sys.exit(1)

    # Finally, add custom security policy to config - we do this last
    # because the policy prohibits everyone (including the superuser) from
    # editing non-draft pages: if it's in place during the install phase we
    # wouldn't be able to install packaged pages :)
    with open(configfile, 'a') as fh:
        fh.write('''
    # security policy                                                           
    from CustomSecurityPolicy import CustomSecurityPolicy                       
    SecurityPolicy = CustomSecurityPolicy\n''')
