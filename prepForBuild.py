import json
from fabric.api import run, env, local
from fabric.context_managers import lcd
from json import dumps, load

SETUPFILE = 'setupInfo.json'

if __name__ == '__main__':

    with open(SETUPFILE) as fd:
        info = json.load(fd)
    repoList = info['PrivateRepos']

    with open('pkgInfo.json') as pkg_info:
	pk_info = json.load(pkg_info)
    pkg_num = str(int(pk_info["build"]) + 1)
    pk_info["build"] = str(int(pk_info["build"]) + 1)
    
    with open("pkgInfo.json", "w+") as fd_pkg:
        json.dump(pk_info, fd_pkg, indent=4)

    for repo in  repoList:
	print "path of repo %s is : ~/git/snaproute/src/%s" %(repo, repo)
	if repo == 'asicd' :
		with lcd ('~/git/snaproute/src/'+repo):
			local('git lfs install')
			local('git lfs fetch')
			local('git lfs checkout')
	with lcd ('~/git/snaproute/src/'+repo):
		local ('git reset --hard')
		local ('git checkout master')
		local ('git fetch upstream')
		local ('git merge upstream/master')
