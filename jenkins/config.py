# -*- coding: utf-8 -*-
'''
config.py

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
from fabric.api import env


# Configuration is set to the env singleton and then we can access it from
# any location using env.conf['packages']
env.conf = { 
            'domains': ['ci.w3af.org', 'ci.w3af.com'],
             
            'packages': ['python-virtualenv', 'git', 'python-pip', 'python2.7-dev',
                         'python-setuptools', 'build-essential', 'libsqlite3-dev',
                         'libxml2-dev', 'libxslt-dev', 'apache2', 'joe'],
            
            'deploy_dir': '/opt/ci.w3af.org/w3af-qa/',
            'deploy_dir_parent': '/opt/ci.w3af.org/',
            }
