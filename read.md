# Tensorflow Sudoku

## checklist steps

### [Install RTOBJD package](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html)
  **pip3 install --ignore-installed --upgrade tensorflow==2.5.0**

  *NO GPU SUPPORT, LAPTOP NO LIKEY*

  skipped COCOAPI install as ive already got it from *tensorflow-bsl* project

  testing if RTOBJD package install is still working from *tensorflow-bsl*:
    python object_detection/builders/model_builder_tf2_test.py

  the above command gave me an error

    ``` 
      RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd
      RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd
      RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd
      RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd
    ```
    - changed numpy version to 1.16.5
      - uninstalled numpy in WSL 
      - uninstalled numpy in PS
      - installed numpy in PS
      - inslled numpy in WSL with 
        - ``conda install numpy==1.16.5``
      - uninstalled and reinstalled pycocotools
  - installed anaconda prompt
    - ``python3 object_detection/builders/model_builder_tf2_test.py`` 
    - would report that no moduel numpy was found, *however* ``pip3 show numpy`` would report numpy as been installed in ``natha\miniconda3\lib\site-packages`` so I copied numpy from that directory and pasted inside the ``C:\Users\natha\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages`` directory.
    - running ``python3 object_detection/builders/model_builder_tf2_test.py`` now ran the test succesfully
  



### Create Py script to get images from webcam and store em 
  
  ```
  import cv2

  def capture_images():
    # Open the webcam
    cap = cv2.VideoCapture(0)

      # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Failed to open webcam")
        return

    # Create a window to display the webcam feed
    cv2.namedWindow("Webcam")

    # Initialize image counter
    img_counter = 65 #update this when done adding imgs

    while True:
        # Read frame from the webcam
        ret, frame = cap.read()

        # Display the frame in the "Webcam" window
        cv2.imshow("Webcam", frame)

        # Wait for a key press
        key = cv2.waitKey(1)

        # If the 's' key is pressed, save the current frame as an image
        if key == ord('s'):
            img_name = f"image_{img_counter}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"Image {img_name} saved")
            img_counter += 1

        # If the 'q' key is pressed, exit the loop
        elif key == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

  # Call the capture_images function to start capturing images
  capture_images()
  ```
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

### Find Sudoku grid 
  

### Convert images to ``grayscale`` colorspace
  After we've captured a frame from the webcam we want to convert it to ``grayscale``, we dont care about the images been in ``srgb`` as its not relevant to our task. 

  This is easy enough as ``CV2`` has a function made for this exact thing. 

  ```
  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  ```
  *Parameter 1* is the frame we captured earlier, and *parameter 2* is the color space conversion we are doing. 

### Isolate biggest contour in image
  By isolating the biggest contours in the image we can look for the sudoku grid. 

  #### find all contours in image 
  First to find the bigget contours we need to find all of them. 

  This is relatively easy and we can use 
  ``cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`` Simple *right into left* will give us all the ``contour`` in the image. 

  We can then draw these contours in a image with ``cv2.drawContours(image, [contour], -1, (0,255,0) ,2)`` 

  and display them using ``cv2.imshow('contours', image)``


  #### Find biggest contour in image
  this also returns contours in order of size, becuase of the retrieval mode ``cv2.RETR_EXTERNAL``

  Once we've got the contours we should isolate the biggest one. We can do that with ``BiggestContour = max(contours, key=cv2.contourArea)``

  This isolates the contour with the biggest Area, so we might need to change that criteria depending on how our testing goes. 


### Run Error checking on contour to ensure we have correct data point
 After running a simple error check of ``if len(cv2.approxPolyDP) == 4`` we have eliminted roughly 40% of bad data / images

 We could stretch this logic, by checking if we have a rectangle instead of a quadrilateral. Lets leave this as a stretch goal for now though. 
   
   
    


### Warp Perspective
  We are going to do this to normalise the data, as not all of our training data will have correctly aligned pads. 

  This was somewhat tricky as it require some complex math functions and ordering of the spacial points from the biggest contour. 

  ``cv2.getPerspectiveTransform`` and ``cv2.warpPerspective`` where both used. This results in much more consistent and regular data than before, although we do not have perfectly straight lines in the resulting ``image`` which might be an issues later on down the line. 

  ``cv2.warpPerspective`` does a good job of correcting the rotation of the contour / pads, although it might be benefical to try align the contour / pad *before* calling warp perspective. 

### OCR numbers
  OCR on digits now works. Thanks to tfLite! Shoutout keras_ocr. Very happy with that. 

  Model is consistent even when challenged with partial or warped digits. 

### ...


### Spit out solved sudoku


### Overlay sudoku on webcam grid? 