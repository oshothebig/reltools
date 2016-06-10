import os
import sys
import json
import subprocess 
from optparse import OptionParser

PACKAGE_BUILD="PKG_BUILD=TRUE"
TEMPLATE_BUILD_TYPE="PKG_BUILD=FALSE"
TEMPLATE_CHANGELOG_VER = "0.0.1"
TEMPLATE_BUILD_DIR = "flexswitch-0.0.1"
TEMPLATE_BUILD_TARGET = "cel_redstone"

def buildDocker (command) :
    p = subprocess.Popen(command , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out.rstrip(), err.rstrip()
    print "Docker image return code ", p.returncode 
    print "Check version of  image -- docker images"
    return

def executeCommand (command) :
    out = ''
    if type(command) != list:
        command = [ command]
    for cmd in command:
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        out,err = process.communicate()
    return out

if __name__ == '__main__':
    with open("pkgInfo.json", "r") as cfgFile:
        pkgInfo = cfgFile.read().replace('\n', '')
        parsedPkgInfo = json.loads(pkgInfo)
    cfgFile.close()

    buildTargetList = parsedPkgInfo['platforms']
    for buildTarget in buildTargetList:
	if buildTarget == "docker":
	    cmd = 'python dockerGen/buildDocker.py'
            argCount = len(sys.argv)
            if argCount > 1:
	        print "Building Docker image with flex package ", sys.argv[1]
                buildDocker(cmd + " " + sys.argv[1])
        else:
            cmd = 'python  buildInfoGen.py'
            executeCommand(cmd)

            pkgVersion = parsedPkgInfo['major']+ '.' + parsedPkgInfo['minor'] +  '.' + parsedPkgInfo['patch'] + '.' + parsedPkgInfo['build']
            pkgName = "flexswitch_" + buildTarget + "-" + pkgVersion + "_amd64.deb"
            build_dir = "flexswitch-" + pkgVersion
            preProcess = [
                    'cp -a tmplPkgDir ' + build_dir,
                    'cp Makefile ' + build_dir,
                    'sed -i s/' + TEMPLATE_BUILD_DIR +'/' + build_dir + '/ ' + build_dir +'/Makefile',
                    'sed -i s/' + TEMPLATE_BUILD_TYPE +'/' + PACKAGE_BUILD + '/ ' + build_dir + '/Makefile',
                    'sed -i s/' + TEMPLATE_CHANGELOG_VER +'/' + pkgVersion+ '/ ' + build_dir + '/debian/changelog',
                    ]
            executeCommand(preProcess)

            executeCommand('sed -i s/' + TEMPLATE_BUILD_TARGET +'/' + buildTarget + '/ ' + build_dir + '/Makefile')

            os.chdir(build_dir)
            pkgRecipe = [
                    'fakeroot debian/rules clean',
                    'fakeroot debian/rules build',
                    'fakeroot debian/rules binary',
                    'make clean'
                    ]
            executeCommand(pkgRecipe)
            os.chdir("..")
            command = []
            command.append('rm -rf ' + build_dir)
            executeCommand(command)
            cmd = 'mv flexswitch_' + parsedPkgInfo['major'] + "*" + parsedPkgInfo['build'] + '*_amd64.deb ' + pkgName
            subprocess.call(cmd, shell=True)
