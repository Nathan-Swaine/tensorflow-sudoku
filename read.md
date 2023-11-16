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
  - 1) Send our webcam frame to the model we trained
  - 2) get marked up grid from model
  - 3) use models markings to solve grid
  

### Convert images to ``grayscale`` colorspace
  After we've captured a frame from the webcam we want to convert it to ``grayscale``, we dont care about the images been in ``srgb`` as its not relevant to our task. 

  This is easy enough as ``CV2`` has a function made for this exact thing. 

  ```
  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  ```
  *Parameter 1* is the frame we captured earlier, and *parameter 2* is the color space conversion we are doing. 


### Warp Perspective

### OCR numbers


### ...


### Spit out solved sudoku


### Overlay sudoku on webcam grid? 