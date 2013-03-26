# -*- coding: utf-8 -*-
'''
jenkins.py

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

from fabric.api import task, sudo, settings
from fabric.colors import green
from fabric.operations import prompt
from fabric.api import env
from fabric.contrib import files

from utils.ubuntu import update, install
from utils.filesystem import links_to


@task
def install_jenkins():
    with settings(warn_only=True):
        if sudo("test -e /etc/defaults/jenkins").succeeded:
            print(green('Jenkins is already configured'))
            return
    
    sudo('wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -')
    sudo("sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'")
    update()
    install('jenkins')
    print(green('Finished Jenkins installation.'))

@task
def configure_jenkins():
    with settings(warn_only=True):
        if files.contains('/var/lib/jenkins/config.xml', 'hudson.security.PAMSecurityRealm'):
            print(green('Jenkins is already configured'))
            return

    # I want to have user authentication based on the unix pam
    sudo('usermod -a -G shadow jenkins')

    # And I want to be able to login!
    username = prompt("Jenkins username: ")
    password = prompt("%s username password: ")
    sudo('useradd %s -p `openssl passwd -1 %s`' % (username, password))

    deploy_dir = env.conf['deploy_dir']
    links_to('/var/lib/jenkins/config.xml', '%sjenkins/config/jenkins/global.config.xml' % deploy_dir)
    
    print(green('Finished Jenkins configuration.'))

def restart_jenkins():
    sudo('service jenkins restart')
    