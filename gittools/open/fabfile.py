import os
from fabric.api import local, run, env
from fabric.context_managers import lcd
from fabric.operations import prompt
from fabric.context_managers import settings

env.use_ssh_config = True
gSrRepos = ['l2', 'l3','utils', 'config', 'infra', 'flexSdk', 'apps', 'reltools', 'models', 'docs']
gBranches = ['stable']
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
                cmds = [ 'git checkout master',
                         'git fetch upstream',
                         'git merge upstream/stable',
                         'git push origin'
                         ]

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
