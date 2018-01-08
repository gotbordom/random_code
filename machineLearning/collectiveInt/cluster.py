# Name: Anthony Tracy
# Email: antr9811@colorado.edu
# Description: Same as all the others in this folder. I am learning machine learning stuff....
# NOTE: whitespace is 2 spaces.

from math import sqrt

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
  sum2=sum(vw2)
  # Sum of squares:
  sum_sqr1=sum([pow(v,2) for v in v1])
  sum_sqr2=sum([pow(v,2) for v in v2])
  # Sum of products:
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
  # Calculate r (pearson score):
  num=pSum-sum(sum1*sum2/len(v1))
  den=sqrt((sum_sqr1-pow(sum1,2)/len(v1))*(sum_sqr2-pow(sum2,2)/len(v1)))
  if len(den)==0: return 0

  return 1.0-(num/den)

class bicluster:
  def __init__(self,vec,left=None,right=None,distnace=0.0,id=None):
    self.left=left
    self.right=right
    self.vec=vec
    self.distamce=distance
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
    newcluster=bicluster(meergevec,
                         left=clust[lowestpair[0]],
                         right=clust[lowestpair[1]],
                         distance=closest,
                         id=currentclusterid)
    # Cluster ids are negative if they are not from the initial N clusters made by N-words.
    currentclustid-=1
    del clust[lowestpair[1]]  # Order does matter on how these are deleted. Delete the later in the list first.
    del clust[lowestpair[0]]
    clust.append(newcluster)
  return clust[0]

