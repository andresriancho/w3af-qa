# -*- coding: utf-8 -*-
'''
fabfile.py

Copyright 2013 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
from __future__ import with_statement
from fabric.api import task, env, sudo

from utils.apache import configure_apache, restart_apache
from utils.jenkins import install_jenkins, configure_jenkins, restart_jenkins
from utils.git import git_pull, git_configure, git_clone
from utils.sudo import configure_sudo
from utils.cloudflare import (update_cname_pointer,
                              encrypt_api_key_for_storage)
from utils.ubuntu import (install_packages, set_etc_hosts, remove_bash_history,
                          keep_sudo_env, set_hostname)

import config

# http://docs.fabfile.org/en/latest/usage/env.html#forward-agent
# Use our local SSH keys for accessing github for pull, useful for deploy,
# and backups.
env.forward_agent = True


@task
def deploy():

    set_hostname('ci.w3af.org')
    install_packages(env.conf['packages'])

    # Workaround for "sudo -E", which is required for ssh key forwarding
    # https://github.com/fabric/fabric/issues/503
    keep_sudo_env()

    sudo('mkdir %s' % env.conf['deploy_dir_parent'])

    git_configure()
    git_clone()
    git_pull()

    install_jenkins()
    configure_jenkins()
    configure_apache()
    configure_sudo()
    
    set_etc_hosts()

    restart_daemons()
    
    update_cname_pointer()
    
    # It contains all the passwords!
    remove_bash_history()

@task
def restart_daemons():
    restart_apache()
    restart_jenkins()



