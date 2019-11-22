import sys
import json
import requests
from subprocess import call

#can be changed accordingy to your repo
REPO_NAME = 'My Repository'
REPO_URL = 'http://my-repo.repo.org'
BUILD_DIRECTORY = './my-repo'
#per_page=200 may be critical if maintaina ever has over 200 repos
MAINTAINA_URL = 'https://api.github.com/orgs/maintaina-com/repos?per_page=200'
AUTH_TOKEN = 'e7cbed50c078f1b9b91a0952cc4d2908ed03ef21'
SATIS_JSON_FILE_NAME = 'satis.json'

#request all repos from maintaina
try:
    print('Requesting Repos from {}'.format(MAINTAINA_URL))
    headers = {'Authorization': 'token {}'.format(AUTH_TOKEN)}
    r = requests.get(MAINTAINA_URL, headers=headers)
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
    sys.exit(1)

repo_data = r.json()

#format for satis.json file
satis_json_data = {}
satis_json_data['name'] = REPO_NAME
satis_json_data['homepage'] = REPO_URL
satis_json_data['repositories'] = []
satis_json_data['require-all'] = True

#add all repos from maintaina
for entry in repo_data:
    url = entry['html_url']
    repo_obj = {}
    repo_obj['type'] = 'vcs'
    repo_obj['url'] = url
    satis_json_data['repositories'].append(repo_obj)
    print('Adding Repo: {}'.format(url))

#save satis.json file
print('Saving {}'.format(SATIS_JSON_FILE_NAME))
try:
    with open(SATIS_JSON_FILE_NAME, 'w') as outfile:  
        json.dump(satis_json_data, outfile)
except IOError as err:
    print(err)
    sys.exit(1)

#Set Auth token for composer to increase api call limit, else it is limited to 60/h

#print('Setting auth for composer')
#call('composer config -g github-oauth.github.com {}'.format(AUTH_TOKEN), shell=True)

#build the project from satis.json
#print('Building the project to directory {}'.format(BUILD_DIRECTORY))
#call('php bin/satis build {} {}'.format(SATIS_JSON_FILE_NAME, BUILD_DIRECTORY), shell=True)


