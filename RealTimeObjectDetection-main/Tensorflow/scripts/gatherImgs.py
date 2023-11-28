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
  img_counter = 0 #update this when done adding imgs

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