#!/usr/bin/env python

import commands
import getopt
import os
import re
import sys

PYLINT_CMD = "pylint --errors-only -f parseable plugins/ core/"
IGNORE_PATTERNS = (
	# MISC
	"Undefined variable '_'", # Ignore translation function 
	"Instance of 'exec_shell' has no 'execute' member",
	"callback is not callable",
	"Class 'Thread' has no '_Thread__stop' member",
	"Class 'Thread' has no '_stop' member",
	"No name 'util' in module 'LazyModule'",
	"No name 'reader' in module 'LazyModule'",
	"Instance of 'AbstractNtlmAuthHandler' has no 'auth_header' member",
	"Class 'message' has no 'startswith' member",
	"Instance of 'logHandler' has no 'max_repeats' member",
	"Instance of 'logHandler' has no 'max_redirections' member",
	"Instance of '_deque' has no 'popleft' member",
	"Module 'webkit' has no 'WebView' member",
	# Ignore test classes "violations"
	"Instance of 'Testw3afSVNClient'",
	"Instance of 'test_keepalive' has no",
	"Instance of 'TestVersionMgr'",
	"Instance of 'test_http_vs_https_dist'",
	# Pysvn wrong messages
	"Module 'pysvn' has no 'Revision' member", 
	"Module 'pysvn' has no 'opt_revision_kind' member",
	"Module 'pysvn' has no 'ClientError' member",
	"No name 'wc_notify_action' in module 'pysvn'",
	"No name 'Revision' in module 'pysvn'",
	"No name 'wc_status_kind' in module 'pysvn'",
	# GTK stuff
	"Class 'vbox' has no 'pack_start' member",
	"Class 'vbox' has no 'pack_end' member",
	"Instance of '_RememberingPane' has no 'set_position' member",
	"Instance of 'Searchable' has no 'connect' member",
	"Instance of 'Searchable' has no 'get_colormap' member",
	"Instance of 'Searchable' has no 'pack_start' member",
	# scapy imports
	"from scapy.all import IP",
	"from scapy.all import TCP",
	"from scapy.all import UDP",
	"No name 'traceroute' in module 'scapy.all'",
	)
STATUS_OK = (0, 512)

def _exec_pylint():
    status, output = commands.getstatusoutput(PYLINT_CMD)
    if status not in STATUS_OK:
        print "There was an error while running pylint:"
	print '='*80
	print output
        sys.exit(1)
    return output   


def _get_pylint_output(dir):
    if dir:
        commands.getoutput('cd %s' % dir)
    print "Running pylint on %r..." % dir
    output = _exec_pylint()
    lines = output.split('\n')
    return filter(lambda ln: not any(re.search(patt, ln) 
                       for patt in IGNORE_PATTERNS), lines)

def usage():
    print """
Usage:
    ./w3af_pylint -h
    ./w3af_pylint [-d <script_file>]

Options:

    -h or --help
        Display this help message.

    -d <script_file> or --dir=<script_file>
        Source code directory where to run pylint.
    """

def main(dir=None):
    sys.stdout.write('\n'.join(_get_pylint_output(dir)))
    sys.exit(0)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ['dir=', 'help'])
    except getopt.GetoptError, e:
        usage()
        sys.exit(1)

    dir = None
    
    for o, a in opts:
        if o in ('-d', '--dir'):
            dir = a
            if not os.path.isdir(dir):
                print "Invalid directory: '%s'" % dir
                sys.exit(1)
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
    main(dir=dir)
