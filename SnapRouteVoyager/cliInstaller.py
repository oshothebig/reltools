import os
import subprocess
from optparse import OptionParser

PKG_NAME = 'cliPkg_v146.tar'

def executeCommands(commands):
    for cmd in commands:
        print 'Executing cmd : ', cmd
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            print 'Failed when executing : ', cmd

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--path",
            dest="cliInstallDir",
            action="store",
            help="Directory to use for CLI installation")
    (options, args) = parser.parse_args()
    executeCommands(['tar -xvf ' + PKG_NAME + ' -C ' + options.cliInstallDir])
    os.chdir(options.cliInstallDir)
    recipe = [
            'unzip cmdln-1.1.2.zip',
            'unzip jsonschema-2.5.1.zip',
            'tar -xvzf jsonref-ap-0.3-dev.tar.gz',
            'tar -xvzf requests-2.11.1.tar.gz',
            'rm cmdln-1.1.2.zip jsonschema-2.5.1.zip jsonref-ap-0.3-dev.tar.gz requests-2.11.1.tar.gz'
            ]
    executeCommands(recipe)
