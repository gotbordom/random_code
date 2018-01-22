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
feedlist=[line for line in file('feedlist.txt')]
for feedurl in feedlist:
  try:
    title,wc=getWordCounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
      apcount.setdefault(word,0)
      if count>1:
        apcount[word]+=1
  except:
    print 'Failed to parse feed %s' % feedurl



# Create wordlists to work with :
# Using percentage of words as a threshold to reduce amount of words stored... (don't need overly commmon or uncommon words.)
wordlist=[]

minimum=0.1
maximum=0.5
for w,bc in apcount.items():
  frac=float(bc)/len(feedlist)
  if frac>minimum and frac<maximum: wordlist.append(w)

out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
  # unicode outside ascii range:
  blog=blog.encode('ascii','ignore')
  out.write(blog)
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
  out.write('\n')





