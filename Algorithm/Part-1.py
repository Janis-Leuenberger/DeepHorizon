import numpy as np
from PIL import ImageGrab
import cv2
import time

last_time = time.time()
while(True):

    # Record a screenshot of the top left corner of the screen. Size: 900 x 650
    screen = np.array(ImageGrab.grab(bbox=(0,30, 900,680)))

    # Show the screenshot in a new window.
    cv2.imshow('Press q to quit', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    # Calculate time used for the processing.
    print(f"Loop took: {time.time() -last_time} seconds")
    last_time = time.time()

##
#   Important
#
#
## 