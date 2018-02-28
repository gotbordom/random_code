# Name: Anthony Tracy
# Email: antr9811@colorado.edu
# Description: I am aiming to use this to create a dataset from a folder / video of images. 
# NOTES:
#  - Whitespace = 2 spaces
#  - Make sure to have cv2 installed and sourced... mine is on a different virtual machine on my computer... 
#    (ROS and Anaconda don't play well together and was working two different projects at the time...)


import cv2
import numpy as np
import os, os.path
import argparse
import PythonMagick as Magick   # In the event I have .tif images and need to convert those...

# Leaving sapce for making this work from command line...



######

path='/home/anthony/school/Fall2017/random_code/machineLearning/convNN'
valid_imgs=[".jpg",".gif",".png",".tga"]

featName='features/feat_%06u.png'

xImgs=5    # X is usually larger than y...
yImgs=4


def crop_feat(c,img):
  #print "cropping feature"
  # Shouldn't need to limit this or put bounds on it as MAX_PIXELS is already bounding c
  # to be smaller than the image itself.
  #x,y,w,h = cv2.boundingRect(c) <- seems to make very small features to test on...
  dim = c.size + max(int(c.size*0.15),9) # was 6
  x1 = int(c.pt[0]-dim/2)
  x2 = int(x1+dim)
  y1 = int(c.pt[1]-dim/2)
  y2 = int(y1+dim)
  crop_img = img[y1:y2, x1:x2]
  if y1 >= 360 or y2 >= 360 or x1 >= 480 or x2 >= 480 or y1 < 0 or y2 < 0 or x1 < 0 or x2 < 0:
    return None

  if len(crop_img) == 0:
    return None

  return cv2.resize(crop_img,(32,32))



# Read file into cv2:
for f in os.listdir(path):
  print f
  ext=os.path.splitext(f)[1]
  if ext.lower() not in valid_imgs: continue
  # Fix this later, for now I just wont use tif...
  #if ext.lower() is ".tif":
  #  tmp=Magick.Image(os.path.join(path,f))
  
  # Now do what I want to do to each image:
  img=cv2.imread(os.path.join(path,f),cv2.IMREAD_GRAYSCALE)
  # # # # REMEBER TO ADD A STEP WHERE EACH IMAGE IS SHOWN AND LABELED:
  # # # # SO THAT EACH IMAGE WITHOUT A CRATER WON'T BE SERACHED FOR FEATURES
  




  # Detector:
  detector=cv2.MSER_create()
  # Get blobs:
  feats=detector.detect(img.copy())
  for c in feats:
    cv_feat=crop_feat(c,img.copy())
    if cv_feat==None:
      continue
    cv2.imshow("feat",cv_feat)


