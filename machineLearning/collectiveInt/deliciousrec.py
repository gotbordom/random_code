# Name: Anthony Tracy
# Email: Antr9811@colorado.edu
# Notes:
#   1. This is my code I wrote but was taken and altered from Collective Intelligence published by O'Reilly
#   2. I am using a 2 space whitespace...

import time
from pydelicious import get_popular,get_userposts,get_urlposts

# Building a dataset - pulling data from del.icio.us <- funny name...
# Create user_dict and fill it later:
def initializeUserDict(tag,count=5):
  user_dict={}
  # get top "count" of popular posts:
  for p1 in get_popular(tag=tag)[0:count]:
    # Find the users who poseted them:
    for p2 in get_urlposts(p1['href']):
      user=p2['user']
      user_dict[user]={}
  return user_dict

# Fill user_dict:
def fillItems(user_dict):
  all_items={}
  # Finding links posted by the users in user_dict:
  for user in user_dict:
    # Make only three attempts to get data:
    for i in range(3):
      try:
        posts=get_urlposts(user)
        break
      except:
        print "Failed user"+user+", trying again"
        time.sleep(4)
    for post in posts:
      url=post['fref']
      user_dict[user][url]=1.0
      all_items[url]=1
  # Fill in missing items with 0:
  for ratings in user_dict.values():
    for item in all_items:
      if item not in ratings:
        ratings[item]=0.0
