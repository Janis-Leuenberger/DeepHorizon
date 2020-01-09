import numpy as np
from PIL import ImageGrab
import cv2
import time
from pynput.keyboard import Key, Controller

W = "w"
A = "a"
S = "s"
D = "d"

# Region of interest
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
    except:
        pass

def process_img(original_image):
    #edge detection
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)

    #blur
    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0) #(5,5) needs 2 be odd xD

    #roi
    vertices = np.array(
        [[5,680], [5,300], [330,200], [570,200], [895,300], [895,680]], 
        np.int32)

    processed_img = roi(processed_img, [vertices])

    #[0,540], [240,500], [320,380], [580,380], [680,540], [900,540], [800,680], [0,680] stuff 2 cut out !=roi

    #line detection
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 30, np.array([]), 200, 5) #needs 2 be edges
    draw_lines(processed_img, lines)

    keyboard.release(D)
    keyboard.release(A)

    for i in range(20):
        if(processed_img[i*10+400, 10] == 255):
            #print("right")
            keyboard.press(D)
            break
        if(processed_img[i*10+400, 890] == 255):
            
            #print("left")
            keyboard.press(A)
            break


    # left = False
    # right = False

    # for i in range(20):

    #     if(processed_img[i*10+400, 10] == 255):
    #         #print("right")
    #         #keyboard.press(D)
    #         #break
    #         right = True
    #     if(processed_img[i*10+400, 890] == 255):
    #         #print("left")
    #         #keyboard.press(A)
    #         #break
    #         left = True

    # if(right and left):
    #     print("passing")
    # elif(right):
    #     keyboard.press(D)
    #     print("r")
    # elif(left):
    #     keyboard.press(A)
    #     print("l")
    

    # if(processed_img[400, 10] == 255):
    #     print("right")
    #     keyboard.press(D)
    # elif(processed_img[400, 990] == 255):
    #     print("left")
    #     keyboard.press(A)
    # else:
    #     pass


    return processed_img


keyboard = Controller()

#keyboard.press('w')
# time.sleep(2)
# keyboard.release('w')

for i in range(0):
    print((i - 2) * -1)
    time.sleep(1)


last_time = time.time()
while(True):
    screen =  np.array(ImageGrab.grab(bbox=(0,30, 900,680)))
    new_screen = process_img(screen)

    cv2.imshow('Press q to quit', new_screen)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    print(f"Loop took: {time.time() -last_time} seconds")
    last_time = time.time()