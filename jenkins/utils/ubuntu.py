from __future__ import with_statement

from fabric.api import sudo, env, puts, task, abort
from fabric.contrib import files

@task
def keep_sudo_env():
    if not files.contains('/etc/sudoers', '!env_reset', use_sudo=True):
        files.sed('/etc/sudoers', 'Defaults\tenv_reset',
                                  'Defaults\t!env_reset', use_sudo=True)

def set_etc_hosts():
    if not files.contains('/etc/hosts', 'ci.w3af.org'):
        for domain in env.conf['domains']:
            line = '127.0.0.1       %s' % domain
            files.append('/etc/hosts', line, use_sudo=True)

            line = '127.0.0.1       www.%s' % domain
            files.append('/etc/hosts', line, use_sudo=True)

def set_hostname(hostname):
    sudo('echo %s > /etc/hostname' % hostname)

def remove_bash_history():
    sudo('history -c')

def pip_install(packages):
    sudo('pip install %s' % ' '.join(packages))

def install_packages(packages):
    update()
    dist_upgrade()
    update()
    install(' '.join(packages))

def install(package):
    sudo("apt-get -y install %s" % package)

def update():
    sudo('apt-get update')

def dist_upgrade():
    sudo('apt-get -y dist-upgrade')
    sudo('apt-get -y autoremove')

DETECTION_ERROR_MESSAGE = """
OS detection failed. This probably means your OS is not
supported by django-fab-deploy. If you really know what
you are doing, set env.conf.OS variable to desired OS
name in order to bypass this error message.
If you believe the OS is supported but the detection
fails or you want to get your OS supported, please fire an issue at
https://bitbucket.org/kmike/django-fab-deploy/issues/new
"""

def _codename(distname, version, id):
    patterns = [
        ('lenny', ('debian', '^5', '')),
        ('squeeze', ('debian', '^6', '')),
        ('maverick', ('Ubuntu', '^10.10', '')),
        ('lucid', ('Ubuntu', '^10.04', '')),
        ('precise', ('Ubuntu', '12.04', 'precise')),
    ]
    for name, p in patterns:
        if p[0] == distname and p[1] == version and p[2] == id:
            return name

def detect_os():
    if 'conf' in env and 'OS' in env.conf:
        return env.conf['OS']
    output = sudo('python -c "import platform; print platform.dist()"')
    name = _codename(*eval(output))
    if name is None:
        abort(DETECTION_ERROR_MESSAGE)

    puts('%s detected' % name)
    return name
