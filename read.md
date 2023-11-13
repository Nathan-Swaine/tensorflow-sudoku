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


### Convert images to grayscale colorspace


### Find Sudoku grid 

### OCR numbers

### ...


### Spit out solved sudoku


### Overlay sudoku on webcam grid? 