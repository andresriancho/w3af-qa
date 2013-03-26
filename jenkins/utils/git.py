from __future__ import with_statement

import datetime

from fabric.api import task, sudo, run, env, cd, settings
from fabric.colors import green


def git_configure():
    # Make sure we've got the SSH keys in our knownhosts
    with settings(warn_only=True):
        if run("test -d ~/.ssh/").failed:
            run("mkdir ~/.ssh/")

        if sudo("test -d /root/.ssh/").failed:
            sudo("mkdir /root/.ssh/")

    run("ssh-keyscan -H github.com > ~/.ssh/known_hosts")
    sudo("ssh-keyscan -H github.com > /root/.ssh/known_hosts")

    sudo('git config --global user.email "andres.riancho@gmail.com"')
    sudo('git config --global user.name "Andres Riancho"')

    print(green('Git was configured'))

@task
def git_pull():
    with cd(env.conf['deploy_dir']):
        sudo("git pull")
        sudo("git submodule update --recursive")

        print(green('Repository updated to the latest version'))

@task
def git_clone():

    git_configure()

    with settings(warn_only=True):
        if sudo("test -d %s" % env.conf['deploy_dir']).failed:
            with cd(env.conf['deploy_dir_parent']):

                sudo("git clone git@github.com:andresriancho/w3af-qa.git")

            with cd(env.conf['deploy_dir']):
                sudo("git submodule init")
                sudo("git submodule update --recursive")

            print(green('Finished "git clone".'))

        else:
            print(green('Repository was already cloned'))

@task
def git_commit_push(message=''):
    with cd(env.conf['deploy_dir']):
        backup_message = "Backup for %s" % datetime.datetime.today()
        message = message if message else backup_message
        sudo("git commit -a -m '%s'" % message)
        sudo("git push")

        print(green('Pushed all data to git.'))

