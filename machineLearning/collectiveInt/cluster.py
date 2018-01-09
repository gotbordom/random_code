# Name: Anthony Tracy
# Email: antr9811@colorado.edu
# Description: Same as all the others in this folder. I am learning machine learning stuff....
# NOTE: whitespace is 2 spaces.

from math import sqrt
from PIL import Image,ImageDraw

# Hoping to make a thematic clustering of blogdata.txt...
def readfile(filename):
  lines=[line for line in file(filename)]
  # Titles:
  colnames=lines[0].strip().split('\t')[1:]  # Words
  rownames=[]                               # Blogs
  data=[]                                   # Word Counts
  for line in lines[1:]:
    p=line.strip().split('\t')
    # First column in each row is Blog name:
    rownames.append(p[0])
    # Remainder is data:
    data.append([float(x) for x in p[1:]])
  return rownames,colnames,data

# Using Pearson score to define 'closness'
# this is different from just importing old code because i'm now looking at the closeness of two groups
# not just one person to a list of other people, but n items compared to m items.
def pearson(v1,v2):
  # Simple sums
  sum1=sum(v1)
  sum2=sum(v2)
  # Sum of squares:
  sum_sqr1=sum([pow(v,2) for v in v1])
  sum_sqr2=sum([pow(v,2) for v in v2])
  # Sum of products:
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
  # Calculate r (pearson score):
  num=pSum-(sum1*sum2/len(v1))
  den=sqrt((sum_sqr1-pow(sum1,2)/len(v1))*(sum_sqr2-pow(sum2,2)/len(v1)))
  if den==0: return 0

  return 1.0-(num/den)

class bicluster:
  def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
    self.left=left
    self.right=right
    self.vec=vec
    self.distance=distance
    self.id=id

def hcluster(rows,distance=pearson):
  distances={}
  currentclustid=-1
  # Clusters are initially just every row:
  clust=[bicluster(rows[i],id=i) for i in range(len(rows))]
  while len(clust)>1:
    lowestpair=(0,1)
    closest=distance(clust[0].vec,clust[1].vec)
    # Loop through all pairs to verify lowest and closest:
    for i in range(len(clust)):
      for j in range(i+1,len(clust)):
        # make the distance calculations to save on time, only run dist once for each pair:
        if (clust[i].id,clust[j].id) not in distances:
          distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)
        d=distances[(clust[i].id,clust[j].id)]
        if d < closest:
          closest=d
          lowestpair=(i,j)
    # Calculate average of the two clusters made:
    mergevec=[(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]
    # Create the new clusters:
    newcluster=bicluster(mergevec,
                         left=clust[lowestpair[0]],
                         right=clust[lowestpair[1]],
                         distance=closest,
                         id=currentclustid)
    # Cluster ids are negative if they are not from the initial N clusters made by N-words.
    currentclustid-=1
    del clust[lowestpair[1]]  # Order does matter on how these are deleted. Delete the later in the list first.
    del clust[lowestpair[0]]
    clust.append(newcluster)
  return clust[0]


def printclust(clust,labels=None,n=0):
  # Use indents for visual:
  for i in range(n): print ' ',
  if clust.id<0:
    # We have a negative id and thus a branch:
    print '-'
  else:
    # Positive id and thus an endpoint:
    if labels==None: print clust.id
    else: print labels[clust.id]
  # Print left and right branches:
  if clust.left != None: printclust(clust.left,labels=labels,n=n+1)
  if clust.right != None: printclust(clust.right,labels=labels,n=n+1)

# Want a better visual for the data than just printing them with print clust:
# How wide the image will need to be:
def getheight(clust):
  # If endpoint height is 1:
  if clust.left==None and clust.right==None: return 1
  # Otherwise we have a hight:
  # Using just a recursive simple weighting for getting height:
  return getheight(clust.left)+getheight(clust.right)
# How tall the image will need to be:
def getdepth(clust):
  # Dist of endpoints are always just 0.0:
  if clust.left==None and clust.right==None: return 0
  # Otherwise we need to get sum of max distance:
  return max(getdepth(clust.left),getdepth(clust.right))+clust.distance

# Actually drawing the dendragram:
def drawDendrogram(clust,labels,jpeg='cluster.jpg',params=(20,1200,150,10)):
  # The default image hight is at least 20 pixels:
  # Added these to make it easier to change later if needed:
  pixHeight,pixWidth,sf,xInt=params
  # Get hight and width:
  h=getheight(clust)*pixHeight
  w=pixWidth
  depth=getdepth(clust)
  # Width stays fixed so we can scale dist according to it:
  scaling=float(w-sf)/depth
  # Create image with white background:
  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw((img))

  # Drawing the first node:  
  draw.line((0,h/2,xInt,h/2),fill=(255,0,0))
  drawNode(draw,clust,xInt,(h/2),scaling,labels,params=params)
  img.save(jpeg,'JPEG')

# Drawing the rest of the nodes:
def drawNode(draw,clust,x,y,scaling,labels,params=(20,1200,150,10)):
  pixHeight,pixWidth,sf,xInt=params
  if clust.id<0:
    h1=getheight(clust.left)*pixHeight
    h2=getheight(clust.right)*pixHeight
    top=y-(h1+h2)/2
    bottom=y+(h1+h2)/2
    # Line length:
    l1=clust.distance*scaling
    # Vertical line from l1 to children nodes:
    draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))
    # Horizontal to left:
    draw.line((x,top+h1/2,x+l1,top+h1/2),fill=(255,0,0))
    # Horizontal to right:
    draw.line((x,bottom-h2/2,x+l1,bottom-h2/2),fill=(255,0,0))
    # Call the fucntion recursivly
    drawNode(draw,clust.left,x+l1,top+h1/2,scaling,labels)
    drawNode(draw,clust.right,x+l1,bottom-h2/2,scaling,labels)
  else:
    # Endpoints just get lines to labels:
    draw.text((x+5,y-7),labels[clust.id],(0,0,0))

# rotate the cluster dataset so that clustering will occur on words not blogs:
def rotateMatrix(data):
  newdata=[]
  for i in range(len(data[0])):
    newrow=[data[j][i] for j in range(len(data))]
    newdata.append(newrow)
  return newdata

# Adding k-means clustering:
import random

def kCluster(rows,distance=pearson,k=4):
  # Min and max values for each centroid:
  ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
  # Create k randomly placed centroids:
  clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]

  lastmatches=None
  for t in range(100):
    print 'Iteration: %d' % t
    bestmatches=[[] for i in range(k)]
    # Find closest centroid for each row:
    for j in range(len(rows)):
      row=rows[j]
      bestmatch=0
      for i in range(k):
        d=distance(clusters[i],row)
        if d<distance(clusters[bestmatch],row): bestmatch=i
      bestmatches[bestmatch].append(j)
    # If best == last then we no longer need to cycle through:
    if bestmatches==lastmatches: break
    lastmatches=bestmatches
    # Move centroids:
    for i in range(k):
      avgs=[0.0]*len(rows[0])
      if len(bestmatches[i])>0:
        for rowid in bestmatches[i]:
          for m in range(len(rows[rowid])):
            avgs[m]+=rows[rowid][m]
        for j in range(len(avgs)):
          avgs[j]/=len(bestmatches[i])
        clusters[i]=avgs
  return bestmatches







