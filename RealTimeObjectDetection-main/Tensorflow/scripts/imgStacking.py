import cv2
import sys
import numpy as np
import os 
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
  image = checkContour(image, contours)
  return image

def checkContour(image, contours):
  biggestContour = max(contours, key=cv2.contourArea)
  cv2.drawContours(image, [biggestContour], -1, (0, 255, 0), 1)
  sides = len(cv2.approxPolyDP(biggestContour, 0.02 * cv2.arcLength(biggestContour, True), True))
  if sides == 4: # check if the shape we have is a quadrliteral 
    image = findPoints(biggestContour, image) 
    return image
  else: 
    print("Contour is not a rectangle \n Contour does not have 4 sides, it has " + str(sides) + " sides, the output image hightlight the contour we are looking at.")  
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image, [biggestContour], -1, (0, 255, 0), 1)
    showImg(image)
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
  image = warpPoints(points, image)
  return image 

def warpPoints(points, image):
  pts1 = np.float32(points)
  width = 640
  height = 480
  pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
  matrix = cv2.getPerspectiveTransform(pts1, pts2)
  image = cv2.warpPerspective(image, matrix, (width, height))
  return (image) 

def imgSplit(image):
  boxes= []

  if image.size % 9 != 0: #validate image is correct size
    print("Image is not divisible by 9, reshaping array")
    image= cv2.resize(image, (450, 450))
    print(image.shape) #450,450,3
    
  rows = np.vsplit(image, 9)
  for r in rows:
    cols = np.hsplit(r, 9)
    for box in cols:
      boxes.append(box)
  
  if len(boxes) != 81:
    print("Error, there are not 81 boxes, there are " + str(len(boxes)) + " boxes")
    sys.exit()

  print(getPrediction(boxes))
  return boxes

def getPrediction(boxes):
  import tensorflow as tf # dont import these till they are needed as they slow everything
  from tensorflow.keras.models import load_model
  if os.path.exists("myModel.h5"):
    model = load_model("myModel.h5")
  else: 
    print("Error, model.h5 does not exist")
    sys.exit()
  result = []
  above_threshold = 0
  for index, image in enumerate(boxes):
    ## PREPARE IMAGE
    img = np.asarray(image)
    img = img[4:img.shape[0] - 4, 4:img.shape[1] -4]
    img = cv2.resize(img, (28, 28))
    img = img / 255
    img = img.reshape(1, 28, 28, 1)
    ## GET PREDICTION
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # disable gpu
    predictions = model.predict(img)
    classIndex = np.argmax(predictions, axis=-1)
    probabilityValue = np.amax(predictions)
    ## SAVE TO RESULT
    if probabilityValue > 0.8:
      above_threshold += 1
      row = index // 9
      col = index % 9
      print(f"Predicted class: {classIndex[0]}, Box number: {index}, Coordinates: ({row}, {col})") 
      result.append(classIndex[0])   
    
  print(f"Number of indices above 0.8 confidence: {above_threshold}") #prints 55 when it should print 36
  sys.exit()
  return result

  
image = cv2.imread("image_0.jpg")
image = cnv2Thsh(image)
image = findContours(image)
imgSplit(image)
showImg(image)