#!/usr/bin/env python3

import sys
import requests
import base64
import argparse

# Uncomment statement for user or computer
#statement = "match (u:User) where TOUPPER(u.email) contains TOUPPER('{}') set u.owned=true RETURN u".format(o)
statement = "match (c:Computer) where TOUPPER(c.name) contains TOUPPER('{}') set u.owned=true RETURN u".format(o)

# Put Neo4j DB info here
host = '<IP>:7474'
auth = base64.b64encode('<user>:<password>'.encode("ascii"))

parser = argparse.ArgumentParser(description='Mark Bloodhound owned from list.')
parser.add_argument('file',
                    nargs='?',
                    type=argparse.FileType('r'),
                    action='store',
                    help='File containing a list of users/computers split by a newline, otherwise read from STDIN',
                    metavar='FILE',
                    default=sys.stdin)
args = parser.parse_args()

#Run Cypher query in Neo4j
def runcypher(server,statement,auth):
    headers = { "Accept": "application/json; charset=UTF-8",
                "Content-Type": "application/json",
                "Authorization": auth }
    data = {"statements": [{'statement': statement}]}
    url = 'http://{}/db/data/transaction/commit'.format(server)
    r = requests.post(url=url,headers=headers,json=data)
    r.raise_for_status()

try:
    owned = [line.strip() for line in args.file if len(line.strip())>0 and line[0] != '#']
except KeyboardInterrupt:
    exit()

x=0
for o in owned:
        runcypher(host,statement,auth)
        print('{}: Marked user: {} owned'.format(x, o))
        x=x+1
