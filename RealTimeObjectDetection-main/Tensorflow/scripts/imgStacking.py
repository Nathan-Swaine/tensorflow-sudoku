import cv2

# Load the image
image = cv2.imread("image_0.jpg")

# Check if the image was successfully loaded
if image is not None:
    # Display the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)

else:
    print("Failed to load the image.")