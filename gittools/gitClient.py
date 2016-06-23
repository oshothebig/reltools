#!/usr/bin/python
import requests
import json
import urllib2
import getpass

headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
httpSuccessCodes = [200, 201, 202, 204]
class GitHubClient( object):
    def  __init__ (self, usr, passwd):
        self.usr = usr
        self.passwd = passwd

    def getReferences(self, org, repo, branch):
        qry = 'https://api.github.com/repos/%s/%s/git/refs' %(org, repo)
        response = requests.get(qry, auth=(self.usr, self.passwd ))
        if response.status_code in httpSuccessCodes:
            data = response.json()
            for entry in data:
                if entry['url'] ==  qry + '/heads/' + branch: 
                    return entry['object']['sha']

    def getReleases (self, org, repo):
        qry = 'https://api.github.com/repos/%s/%s/releases' %(org, repo)
        response = requests.get(qry, auth=(self.usr, self.passwd ))
        if response.status_code in httpSuccessCodes:
            data = response.json()
            for entry in data:
                for k,v in entry.iteritems():
                    print '%s    : %s' %(k, v)
                print entry
        
    def getShaForBranch (self, org, repo, branch):
        return self.getReferences(org, repo, branch)

    def createBranch (self, org, repo, branchFrom, newBranch):
        sha = self.getShaForBranch (org, repo, branchFrom)
        obj = {'ref' : 'refs/heads/%s' %(newBranch),
                'sha' : str(sha)}

        reqUrl = 'https://api.github.com/repos/%s/%s/git/refs' %(org, repo)
        response  = requests.post(reqUrl, data=json.dumps(obj), headers=headers, auth=(self.usr, self.passwd ))
        if response.status_code in httpSuccessCodes:
            print 'Successfully created branch %s for repo %s from %s' %(newBranch, repo, branchFrom)
        return response

    def applyReleaseTag(self, org, repo, branch, tagName, relName, description, draft=True, prerel=True):
        obj = {'tag_name' :  tagName,
               'targe_commitish' : branch,
               'name' : relName,
               'body' : description,
               'draft' : draft,
               'prerelease' : prerel
              }

        reqUrl = 'https://api.github.com/repos/%s/%s/releases' %(org, repo)
        response  = requests.post(reqUrl, data=json.dumps(obj), headers=headers, auth=(self.usr, self.passwd ))
        if response.status_code in httpSuccessCodes:
            print 'Successfully created release tag for repo %s on branch %s' %(branch, repo)
        return response
