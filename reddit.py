#!/usr/bin/env python2.7

import re
import sys
import requests
import json
import os

# GLOBAL VARS 

FIELD = 'title'
LIMIT = 10
SUBREDDIT = 'linux'
REGEX = ' '

# FUNCTIONS

def usage(status=0):
  print '''Usage: reddit.py [ -f FIELD -s SUBREDDIT ] regex

  -f FIELD        Which field to search (default: title)
  -n LIMIT        Limit number of articles to report (default: 10)
  -s SUBREDDIT    Which subreddit to search (default: linux)'''
  sys.exit(status)

# parse command line

args = sys.argv[1:]
while len(args) and args[0].startswith('-') and len(args[0]) > 1:
  arg = args.pop(0)
  if arg == '-f':
    FIELD = args.pop(0)
  elif arg == '-n':
    LIMIT = int(args.pop(0))
    if LIMIT <= 0:
      print 'Invalid Number'
      sys.exit(1)
  elif arg == '-s':
    SUBREDDIT = args.pop(0)
  elif arg == '-h':
    usage(0)
  else:
    usage(1)

if len(args) != 1:
  REGEX = '.*'
else:
  REGEX = args[0]

# 429 too many requests


headers  = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
response = requests.get('https://www.reddit.com/r/linux/.json', headers=headers)

# json

link = 'https://www.reddit.com/r/%s.json' % SUBREDDIT 
r = requests.get(link, headers=headers)
jsondata = r.json()

# check fields

articleinfo = []
for count, check in enumerate(jsondata['data']['children']):
  check = check['data']
  if FIELD in check:
    if re.search(REGEX, check[FIELD]):
      article = {}
      article['Title'] = check['title']
      article['Author'] = check['author']
      article['Link'] = check['url']
      articleinfo.append(article)
  else:
    print 'Invalid field: ', FIELD
    break
  if (count+1 > LIMIT):
    break

# limits

articleNUM = LIMIT
for count, i in enumerate(articleinfo):
  print '{})\tTitle: '.format(count+1), i['Title']
  print '\t', 'Author: ', i['Author']
  print '\t', 'Link: ', i['Link'], '\n'
  articleNUM = articleNUM - 1
  if articleNUM == 0:
    break
