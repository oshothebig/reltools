import os
from fabric.api import local, run, env
from fabric.context_managers import lcd
from fabric.operations import prompt
from fabric.context_managers import settings

env.use_ssh_config = True
gSrRepos = ['asicd', 'l2', 'l3','config', 'utils','infra', 'flexSdk', 'apps', 'reltools', 'models', 'docs']
#gSrRepos = ['l3', 'asicd' ]
def mergeRepos (comp=None):
    global gSrRepos
    print 'Fetching Snaproute repositories dependencies....'
    srRepos = gSrRepos
    if comp != None :
        srRepos = [comp]

    for repo in srRepos:
        cmds = ['git checkout -b pre_rel_1.x origin/pre_rel_1.x ',
                'git remote add upstream https://github.com/snaproute/%s.git' %(repo),
                'git pull',
                'git fetch upstream',
                'git merge upstream/master',
                'git push origin'
                ]
        local('git clone '+ 'https://github.com/snaproute/' + repo + '.git')
        with lcd(repo):
            for cmd in cmds:
                local(cmd)

def push(comp=None):
    global gSrRepos
    print 'Pushing Snaproute repositories' 
    srRepos = gSrRepos
    if comp != None :
        srRepos = [comp]

    for repo in srRepos:
        cmds = ['git push origin']
        with lcd(repo):
            for cmd in cmds:
                print 'Pushing repo %s'  %(repo)
                local(cmd)

