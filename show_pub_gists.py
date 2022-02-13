#!/usr/bin/python3


# show_pub_gists.py will show listing of a user's publicly available gists.
#
# Usage: show_pub_gists.py <user> <option>
# User is the user whose gists are to be queried
# option cab be 'l' for list of gists only or 'd' for list with content of gists.

# The first time when user's gist is queried it will save the current
# gists for that user and show the date of the latest gist. The user
# will be saved in a file named "/tmp/show_pub_gists.<user>" and list of gists will be saved in
# /tmp/show_pub_gists.<user>-gists. Subsequent executions for the same user will tell
# you if a new gist has been added by the user and show the difference of previous list and new list.

import os, argparse, json
from datetime import datetime
import urllib, requests
from difflib import Differ
# Parse command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("git_user", help="Github user for gists query")
parser.add_argument("git_option", choices=['l', 'd'], help="List or details for gists query")
args = parser.parse_args()
GIT_GIST_URL = 'http://api.github.com/users/' + args.git_user + '/gists'

# Attempt to connect to Github and query user's Gists
# If status code is not 200 handle it and exit

r = requests.get(GIT_GIST_URL)
if r.status_code != 200:
    if r.status_code == 404:
        print ('Error: Github user "' + args.git_user + '" not found.')
    else:
        r.raise_for_status()
    exit(255)
gist = json.loads(r.content)

if not gist:
    print ('Github user "' + args.git_user + '" has not published any gists.')
    exit(1)

# Now check if user is previously queried if not create the record and show the list of gists otherwise
# amend the record of the user and show the new records.

configPath = '/tmp/show_pub_gists.' + args.git_user
if not os.path.isfile(configPath):
    print('Github user "' + args.git_user +
        '" gists have not been previously queried.')
    print('Creating checkpoint file: ' + configPath)
    try:
        configFile = open(configPath, "w")
        configFile.write(gist[0]['created_at'])
        configFile.close()
    except Exception as e:
        raise
    for k in gist:
        for key, value in k.items():
            for fl in k["files"]:
                if key == "created_at" and datetime.strptime(value,'%Y-%m-%dT%H:%M:%SZ') > datetime.strptime('1980-01-01T00:00:00Z','%Y-%m-%dT%H:%M:%SZ'):
                    if args.git_option == 'l':
                        print("File_name {}: URL {}: Created_at {}".format(k["files"][fl]["filename"],k["files"][fl]["raw_url"],str(value))) 
                    if args.git_option == 'd':
                        print("File_name {}: URL {}: Created_at {}".format(k["files"][fl]["filename"],k["files"][fl]["raw_url"],str(value)))
                        print("Contents of file:_ ")
                        response = requests.get(k["files"][fl]["raw_url"])
                        print(response.text)
                        
else:
    try:
        configFile = open(configPath,"r")
        stringDate = configFile.read()
    except Exception as e:
        raise
    lastCreateDate = datetime.strptime(stringDate,'%Y-%m-%dT%H:%M:%SZ')
    currentLastCreateDate = datetime.strptime(gist[0]['created_at'],'%Y-%m-%dT%H:%M:%SZ')
    if currentLastCreateDate > lastCreateDate:
        print('Github user "' + args.git_user + '" created a new gist since the last query.')
        try:
            configFile = open(configPath,"w")
            configFile.seek(0,0)
            configFile.write(gist[0]['created_at'])
        except Exception as e:
            raise
# compare the previous list with new list and show the difference.
        for k in gist:
            for key, value in k.items():
                for fl in k["files"]:
                    if key == "created_at" and datetime.strptime(value,'%Y-%m-%dT%H:%M:%SZ') > lastCreateDate:
                        if args.git_option == 'l':
                            print("File_name {}: URL {}: Created_at {}".format(k["files"][fl]["filename"],k["files"][fl]["raw_url"],str(value))) 
                        if args.git_option == 'd':
                            print("File_name {}: URL {}: Created_at {}".format(k["files"][fl]["filename"],k["files"][fl]["raw_url"],str(value)))
                            print("Contents of file:_ ")
                            response = requests.get(k["files"][fl]["raw_url"])
                            print(response.text)
    else:
        print('Github user "' + args.git_user +
            '" has not created a new gist since the last query.')
    configFile.close()
exit(0)
