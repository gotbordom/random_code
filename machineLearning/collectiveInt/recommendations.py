# Name: Anthony Tracy
# Email: Antr9811@colorado.edu
# Notes:
#   1. This is my code I wrote but was taken and altered from Collective Intelligence published by O'Reilly
#   2. I am using a 2 space whitespace...

from math import sqrt

# Euclidian Distance for finding similarities:
def sim_dist(prefs,person1,person2):
  # shared items:
  si={}
  for item in prefs[person1]:
    if item in prefs[preson2]:
      # Label the dataset with True or false:
      si[item]=1
  # Return zero for nothing in common:
  if len(si)==0:
    return 0

  # Sum of squares:
  sum_sqrs = sum([pow(prefs[person1][item],2)-pow([person2][item],2) for item in si])
  
  return 1/(1+sum_sqrs)


# Pearson Correlation Score:
def sim_pearson(prefs,p1,p2):
  si={}
  for item in prefs[p1]
    if item in prefs[2]:
      # Again label for true or false:
      si[item]=1

  # Retrun 0 for no items in common:
  n = len(si)  # Number of elements
  if n==0:
    return 0
  
  # Pearson score:
  # Add up all prefs:
  s1=sum([prefs[p1][item] for item in si])
  s2=sum([prefs[p2][item] for item in si])

  # Sum of squares for each prefs:
  s1Sq = sum([pow(prefs[p1][item],2) for item in si])
  s2Sq = sum([pow(prefs[p2][item],2) for item in si])

  # Sum of products of p1 and p2:
  pSum = sum([prefs[p1][item]*prefs[p2][item] for item in si])

  # Calc Pearson score:
  num=pSum-(s1*s2/n)
  den=sqrt((s1Sq-pow(s1,2)/n)*(s2Sq-pow(s2,2)/n)
  if den==0: return 0
  return num/den




