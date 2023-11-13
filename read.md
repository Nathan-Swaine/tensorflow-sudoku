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
  There are a couple ways we could do this.

  - 1) Use ``LabelImg`` to create a ``model`` that finds the sudoku grid. Some practice doing this but it will be overkill. 
      - Benefits
        - Famailar 
      - Drawbacks
        - Inefficent
        - Technically difficult
        - imperfect accuracy at best, rarely working at worst
        - multiple sets of training data
        - including a package that would only be used for one thing (``LabelImg``)

  - 2) ``cv2.contourArea()``  we might be able to use this, along with some clever data validation to find the sudoku grid. This method might fail though if the grid is relatively small and the rest of the image does not have many contours. ``cv2.approxPolyDP()``, ``cv2.arcLength()`` and ``cv2.contureArea()`` 

        ```
          def biggestConture(contures):
            import numpy as np
            max_area=0 
            for i in contours: 
              area = cv2.contourArea(i)
              if area > 20: 
                peri = cv2.arcLength()
                approx = cv2.approxPolyDP(i, 0.02 * peri, true)
                if area> maxArea and len(approx) == 4: 
                  biggest = approx 
                  max_area = area
        ```

        This code, or some code *similar* to it should return the biggest conture / shape that has 4 sides. *After* we've supplied it with an array of contours in a image. 

        - Benefits
          - video to [follow](https://www.youtube.com/watch?v=qOXDoYUgNlU&ab_channel=Murtaza%27sWorkshop-RoboticsandAI) 
          - more accurate / consistent
          - easily tweekable
          - not *very* technical
        - Drawbacks
          - need to order points 
          - need to warp perspective to enable flat images
          - this might find the outer rectangle of the sudoku pad instead of the pad *inside* the grid

  - 3) find clusters of numbers and use that to get a rough idea of where the grid is. We could skip this step, and start OCR'ing numbers before we've found the grid, then look for a sudoku like cluster of numbers to find where the grid is 

### Warp Perspective

### OCR numbers


### ...


### Spit out solved sudoku


### Overlay sudoku on webcam grid? 