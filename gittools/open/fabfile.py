import os
from fabric.api import local, run, env
from fabric.context_managers import lcd
from fabric.operations import prompt
from fabric.context_managers import settings

env.use_ssh_config = True
gSrRepos = ['l2', 'l3','utils', 'config', 'infra', 'flexSdk', 'apps', 'reltools', 'models', 'docs']
gBranches = ['master', 'gh-pages','pre_rel_1.x']
def syncRepo( comp = None):
    global gSrRepos
    global gBranches
    srRepos = gSrRepos
    if comp != None :
        srRepos = [comp]
    for repo in srRepos:
        print '## Working on Repo %s' %(repo)
        for branch in gBranches:
            '## Working on Branch %s' %(branch)
            with  lcd(repo):
                checkoutCmd = 'git checkout ' + branch 
                with settings(warn_only=True):                                                                                         
                    ret = local(checkoutCmd, capture=True)                                                                                                                                                                                       
                    if ret.failed:
                        cmdList = ['git checkout -b ' + branch]
                    else:
                        cmdList = []
                    

                cmds = cmdList + [ 'git branch %s -u upstream/%s' %(branch, branch),
                       'git fetch origin',
                       'git merge origin %s' %(branch),
                       'git pull origin %s' %(branch),
                       'git push origin']
                for cmd in cmds:
                    local(cmd)

def fetchRepos (comp=None):
    global gSrRepos
    global gBranches
    print 'Fetching Snaproute repositories dependencies....'
    srRepos = gSrRepos
    if comp != None :
        srRepos = [comp]

    for repo in srRepos:
        local('git clone '+ 'https://github.com/OpenSnaproute/' + repo + '.git')
        with lcd(repo):
            local('git remote add upstream https://github.com/SnapRoute/' +  repo + '.git')
            local('git fetch upstream')


def syncAll (comp = None):
    fetchRepos(comp)
    syncRepo(comp)
