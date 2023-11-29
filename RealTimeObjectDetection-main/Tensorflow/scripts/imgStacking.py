import cv2
import sys
import numpy as np
def showImg(image):
  cv2.imshow("Original", image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def cnv2Thsh(image):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
  image = cv2.GaussianBlur(image, (5, 5), 1)  # ADD GAUSSIAN BLUR
  image = cv2.adaptiveThreshold(image, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
  return image

def findContours(image):
  contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  checkContour(image, contours)
  
  return image

def checkContour(image, contours):
  biggestContour = max(contours, key=cv2.contourArea)
  cv2.drawContours(image, [biggestContour], -1, (0, 255, 0), 1)
  sides = len(cv2.approxPolyDP(biggestContour, 0.02 * cv2.arcLength(biggestContour, True), True))
  if sides == 4: 
    findPoints(biggestContour, image) 
    return image
  else: 
    print("Contour is not a rectangle \n Contour does not have 4 sides, it has " + str(sides) + " sides, the output image hightlight the contour we are looking at.")  
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image, [biggestContour], -1, (0, 255, 0), 1)
    cv2.imshow('contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    sys.exit()
   

def orderPoints(points): ##tricky function, warp perspective requires points to be in a specific order which this ensures
  points = points.reshape((4, 2))
  newPoints = np.zeros((4, 1, 2), dtype=np.int32)
  add = points.sum(1)
  newPoints[0] = points[np.argmin(add)]
  newPoints[3] = points[np.argmax(add)]
  diff = np.diff(points, axis=1)
  newPoints[1] = points[np.argmin(diff)]
  newPoints[2] = points[np.argmax(diff)]
  return newPoints

def findPoints(bigCountur, image):
  points = cv2.approxPolyDP(bigCountur, 0.02 * cv2.arcLength(bigCountur, True), True)
  points = orderPoints(points)
  
  image = cv2.drawContours(image, points, -1, (0,255,0), 1)
 
  warpPoints(points, image)
  
  return image 

def warpPoints(points, image):
  pts1 = np.float32(points)
  width = 640
  height = 480
  pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
  matrix = cv2.getPerspectiveTransform(pts1, pts2)
  image = cv2.warpPerspective(image, matrix, (width, height))
  cv2.imshow("Warp", image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  sys.exit()  




image = cv2.imread("image_1.jpg")
image = cnv2Thsh(image)
image = findContours(image)
showImg(image)







