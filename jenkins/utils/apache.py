from __future__ import with_statement
from fabric.api import task, sudo, env, settings, cd
from fabric.colors import green

from utils.filesystem import links_to


@task
def configure_apache():
    with settings(warn_only=True):
        if sudo("test -e /etc/apache2/sites-enabled/jenkins").succeeded:
            print(green('Apache is already configured'))
            return

    deploy_dir = env.conf['deploy_dir']

    # Configure enabled sites
    sudo('rm -rf /etc/apache2/sites-enabled/*')
    links_to('/etc/apache2/sites-enabled/jenkins', '%sjenkins/config/apache/jenkins' % deploy_dir)

    apache_modules = ['proxy', 'proxy_http', 'vhost_alias']

    for module in apache_modules:
        enable_module(module)

    print(green('Finished Apache configuration.'))

def enable_module(module):
    sudo('a2enmod %s' % module)

def restart_apache():
    sudo('service apache2 restart')
