# Name: Anthony Tracy
# Email: antr9811@colorado.edu
# This is again code from Collective Intelligence and is intended for me learning machine learning.
# NOTES: whitespace is 2 spaces.

import feedparser
import re

# Return title and word count for RSS feed:
def getWordCounts(url):
  # Parsing:
  d=feedparser.parse(url)
  wc={}
  # Looping over entries:
  for e in d.entries:
    if 'summary' in e: summary = e.summary
    else: summary = e.discription

    # Get list of words:
    words=getwords(e.title+' '+summary)
    for word in words:
      wc.setdefault(word,0)
      wc[word]+=1
  return d.feed.title,wc

def getwords(html):
  # Removing HTML tags:
  txt=re.compile(r'<[^>]+>').sub('',html)
  # Split words by non-alpha charecters:
  words=re.compile(r'[^A-Z^a-z]+').split(txt)
  # Convert to lower case:
  return [word.lower() for word in words if word !='']


# Main script for using above functions:

# Read the feed in from feedlist.txt...
apcount={}
wordcounts={}
feedlist={}
for feedurl in file('feedlist.txt')
  feedlist.add(feedurl)
  title,wc=getWordCounts(feedurl)
  wordcounts[title]=wc
  for word,count in wc.items()
    apcount.setdefault(word,0)
    if count>1:
      apcount[word]+=1

# Create wordlists to work with :
# Using percentage of words as a threshold to reduce amount of words stored... (don't need overly commmon or uncommon words.)
wordlist=[]

minimum=0.1
maximum=0.5
for w,bc i apcount.items():
  frac=float(bc)/len(feedlist)
  if frac>minimum and frac<maximum: wordlist.append(w)




