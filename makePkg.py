import os
import sys
import json
import time
import fileinput
import subprocess 
from optparse import OptionParser


PACKAGE_BUILD="PKG_BUILD=TRUE"
TEMPLATE_BUILD_TYPE="PKG_BUILD=FALSE"
TEMPLATE_CHANGELOG_VER = "0.0.1"
TEMPLATE_BUILD_DIR = "flexswitch-0.0.1"
TEMPLATE_BUILD_TARGET = "cel_redstone"
TEMPLATE_ALL_TARGET = "ALL_DEPS=buildinfogen codegen installdir ipc exe install"
PKG_ONLY_ALL_TARGET = "ALL_DEPS=installdir install"

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
    firstBuild = True
    buildTargetList = parsedPkgInfo['platforms']
    pkgVersion = parsedPkgInfo['major']+ '.' + parsedPkgInfo['minor'] +  '.' + parsedPkgInfo['patch'] + '.' + parsedPkgInfo['build']
    build_dir = "flexswitch-" + pkgVersion
    startTime = time.time()
    for buildTarget in buildTargetList:
        print "Building pkg for", buildTarget
        pkgName = "flexswitch_" + buildTarget + "-" + pkgVersion + "_amd64.deb"
        if firstBuild:
            preProcess = [
                    'cp -a tmplPkgDir ' + build_dir,
                    'cp Makefile ' + build_dir,
                    'sed -i s/' + TEMPLATE_BUILD_DIR +'/' + build_dir + '/ ' + build_dir +'/Makefile',
                    'sed -i s/' + TEMPLATE_BUILD_TYPE +'/' + PACKAGE_BUILD + '/ ' + build_dir + '/Makefile',
                    'sed -i s/' + TEMPLATE_CHANGELOG_VER +'/' + pkgVersion+ '/ ' + build_dir + '/debian/changelog',
                    'sed -i s/' + TEMPLATE_BUILD_TARGET +'/' + buildTarget + '/ ' + build_dir + '/Makefile'
                    ]
            executeCommand(preProcess)
            #Build all binaries only once
            os.chdir(build_dir)
            executeCommand('make all')
            os.chdir("..")
            executeCommand('python buildInfoGen.py')
            firstBuild = False
            #Change all target prereqs
            for line in fileinput.input(build_dir+'/Makefile', inplace=1):
                print line.replace(TEMPLATE_ALL_TARGET, PKG_ONLY_ALL_TARGET).rstrip('\n')
        else :
            #Change build target and all target prereqs
            for line in fileinput.input(build_dir+'/Makefile', inplace=1):
                print line.replace(prevBldTgt, buildTarget).rstrip('\n')
            os.chdir(build_dir)
            executeCommand('make asicd')
            os.chdir("..")
        prevBldTgt = buildTarget
        os.chdir(build_dir)
        pkgRecipe = [
                'fakeroot debian/rules clean',
                'fakeroot debian/rules build',
                'fakeroot debian/rules binary',
                ]
        executeCommand(pkgRecipe)
        os.chdir("..")
        cmd = 'mv flexswitch_' + parsedPkgInfo['major'] + "*" + parsedPkgInfo['build'] + '*_amd64.deb ' + pkgName
        subprocess.call(cmd, shell=True)
	if buildTarget == "docker":
            cmd = 'python dockerGen/buildDocker.py'
            print "Building Docker image with flex package ", pkgName
            buildDocker(cmd + " " + pkgName)
    command = [
            'rm -rf ' + build_dir,
            'make clean_all'
            ]
    executeCommand(command)
