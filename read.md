# Tensorflow Sudoku

## checklist steps

### Gather images from webcam with OpenCV

I've done this before so should be easy enough. Key learning from last time are that webcam is not supported in WSL2. 

```
 import cv2 
   cv2.destroyAllWindows()
  capture = cv2.VideoCapture(0)
 ret, frame = capture.read()
 if ret:
  cv2.imshow('frame', frame)
     key = cv2.waitKey(0)
       cv2.imwrite(imgName, frame)
      print('Image saved: ' + str(imgnum))
```
  
Code *somewhat* similar to that should sort capturing a frame from the webcam and saving it to disk under ``imgName`` 


### Convert images to ``grayscale`` colorspace

After we've captured a frame from the webcam we want to convert it to ``grayscale``, we dont care about the images been in ``srgb`` as its not relevant to our task. 

This is easy enough as ``CV2`` has a function made for this exact thing. 

```
cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
*Parameter 1* is the frame we captured earlier, and *parameter 2* is the color space conversion we are doing. 

### Find Sudoku grid 

### OCR numbers

### ...


### Spit out solved sudoku


### Overlay sudoku on webcam grid? 