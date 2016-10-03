#!/usr/bin/env python
import os
from optparse import OptionParser
import syslog

if __name__=="__main__":
    parser = OptionParser()

    parser.add_option("-d", "--dir", 
                      dest="directory",
                      default="/opt/flexswitch",
                      action='store',
                      help="Directory where the python modules located")

    parser.add_option("-o", "--op", 
                      dest="op",
                      default="install",
                      action='store',
                      help="Operation (install/uninstall) ")

    (opts, args) = parser.parse_args()
    baseDir = opts.directory if opts.directory.endswith('/') else opts.directory+'/'
    op = opts.op
    pkgDirs = [x for x in os.listdir(baseDir) if os.path.isdir(baseDir +x)]
    for pkg in pkgDirs:
        if os.path.exists(baseDir + pkg + '/setup.py'):
            os.chdir(baseDir + pkg)
            os.system('python setup.py  %s' %(op))

