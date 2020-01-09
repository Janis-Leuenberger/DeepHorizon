import numpy as np
from PIL import ImageGrab
import cv2
import time

# Function, which uses cv2 to find edges
def process_img(original_image):
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
	return processed_img


last_time = time.time()
while(True):

    # Record a screenshot of the top left corner of the screen. Size: 900 x 650
    screen = np.array(ImageGrab.grab(bbox=(0,30, 900,680)))

    # Run the edge detection function
    new_screen = process_img(screen)

    # Show the processed image in a new window.
    cv2.imshow('Press q to quit', new_screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    # Calculate time used for the processing.
    print(f"Loop took: {time.time() -last_time} seconds")
    last_time = time.time()