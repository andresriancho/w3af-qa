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
from utils.ubuntu import update, install


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
        # TODO: This test is too simple
        if sudo("test -e /var/lib/jenkins/config.xml").succeeded:
            print(green('Jenkins is already configured'))
            return

    #TODO: What to do here?

    print(green('Finished Jenkins configuration.'))

def restart_jenkins():
    sudo('service jenkins restart')
    