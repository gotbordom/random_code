# Name: Anthony Tracy
# Email: antr9811@colorado.edu

# Learning about PageRank algorithm

import urllib2
from BeautifulSoup import *
from urlparse import urljoin

# words to ignore:
ignoreWords=['the','of','to','and','a','in','is','it']
# Testing git save....

class crawler:
  def __init__(self,dbName):
    pass
  def __del__(self):
    pass
  def dbCommit(self):
    pass

  # Aux functions:
  def getEntryId(self,table,field,value,createNew=True):
    return None

  # Index single page:
  def addtoInd(self,url,soup):
    print 'Indexing %s' % url

  # Extract text from HTML:
  def getTxtOnly(self,soup):
    return None

  # Seperate words from whitespace:
  def seperateWords(self,txt):
    return None

  # Return true is already indexed:
  def isIndexed(self,url):
    return False

  # Add link between pages:
  def addLinkRef(self,urlFrom,urlTo,linkTxt):
    pass

  # Starting with a list of pages, do a breadth
  # first search to get depth and ind pages as we go:
  def crawl(self,pages,depth=2)
    pass
