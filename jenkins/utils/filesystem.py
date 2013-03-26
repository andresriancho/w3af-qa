from __future__ import with_statement
from fabric.api import sudo, env

def links_to(orig, dest):
    sudo('rm -rf %s' % orig)
    sudo('ln -s %s %s' % (dest, orig))

