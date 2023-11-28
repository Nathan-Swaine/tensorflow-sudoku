import cv2

def showImg(image):
  cv2.imshow("Original", image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()



def cnv2Thsh(image):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
  image = cv2.GaussianBlur(image, (5, 5), 1)  # ADD GAUSSIAN BLUR
  image = cv2.adaptiveThreshold(image, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
  return image

image = cv2.imread("image_0.jpg")
image = cnv2Thsh(image)
showImg(image)






