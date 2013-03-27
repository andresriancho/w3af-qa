# -*- coding: utf-8 -*-
'''
cloudflare.py

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
import urllib2
import urllib
import json
import sys

from fabric.api import env, task
from fabric.operations import prompt
from fabric.colors import green, red

from utils.security import decrypt_aes, encrypt_aes


def get_api_key():
    cloudflare_api_key = env.conf['cloudflare_api_key']
    api_key_passwd = prompt('Please enter your API key encryption password:')
    return decrypt_aes(api_key_passwd, cloudflare_api_key)

@task
def update_cname_pointer():
    url = 'https://www.cloudflare.com/api_json.html'
    
    amazon_ec2_domain = prompt('Please enter the amazon ec2 domain name: ')
    
    data = {'a': 'rec_edit',
            'tkn': get_api_key(),
            'id': '59142700',   #FIXME: Hardcoded, ugly!
            'email': 'andres.riancho@gmail.com',
            'z': 'w3af.org',
            'type': 'CNAME',
            'name': 'ci',
            'content': amazon_ec2_domain,
            'service_mode': '1', #enable cloudflare
            'ttl': '1',
            }
    
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json_response = response.read()
    
    json_inst = json.loads(json_response)
    if json_inst['result'] == 'success':
        print(green('Updated CNAME for ci.w3af.org'))
    else:
        print(red('Failed to update CNAME for ci.w3af.org!'))
        sys.exit(1)

@task
def encrypt_api_key_for_storage():
    api_key = prompt('Enter your cloudflare API key:')
    api_key_secret = prompt('Enter the password for encrypting the API key in config.py:')
    
    api_key_encrypted = encrypt_aes(api_key_secret.strip(), api_key.strip())
    
    msg = 'Please set %s as cloudflare_api_key and store your password.'
    print(green(msg % api_key_encrypted))
    