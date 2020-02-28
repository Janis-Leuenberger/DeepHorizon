import numpy as np
import cv2
import time
from alexnet import alexnet
import os

from get_keys import key_check
from grab_screen import grab_screen
from set_forza import set_forza
from directkeys import PressKey, ReleaseKey, W, A, S, D

name = 'Name_of_the_model'
MODEL_NAME = '../models/{}'.format(name)

WIDTH = 118
HEIGHT = 62
LR = 1e-3
EPOCHS = 10

speed = False

threshhold = 0.75
threshhold_2 = 0.25

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(A)
    ReleaseKey(D)

def right():
    ReleaseKey(A)
    PressKey(D)

def nothing():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked



model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)


def main():
    #countdown
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    
    paused = False

    vertices = np.array(
            [[5,600], [5,300], [250,180], [550,180], [795,300], [795,600]], 
            np.int32)

    while True:

        keys = key_check()

        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)

        if paused:
            continue

        #record screen and convert

        #record screen and convert
        screen = grab_screen(region=(17, 33, 800, 600))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        #roi        
        screen = roi(screen, [vertices])
        screen = cv2.resize(screen, (120, 90))

        #cut
        height, width = screen.shape
        screen = screen[28:height, 1:width-1]

        #predict
        prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
        moves = list(np.around(prediction))

        print(moves)

        if moves == [1, 0, 0]:
            left()
            #print("left")
            choices[0] += 1
        elif moves == [0, 1, 0]:
            straight()
            #print("straight")
            choices[1] += 1
        elif moves ==  [0, 0, 1]:
            right()
            #print("right")
            choices[2] += 1
        elif moves == [0, 0, 0]:
            nothing()
            choices[3] += 1
        else:
            print("Something went wrong")


        
        height, width = screen.shape
        cv2.imshow('AI', cv2.resize(screen, (width * 10, height * 10)))

        if cv2.waitKey(25) % 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        #print time the frame took
        print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()

choices = [0, 0, 0, 0]
setforza()
try:
    main()
except KeyboardInterrupt:
    print("lefts: {}, forwards: {}, rights: {}, nothings {}".format(choices[0], choices[1], choices[2], choices[3]))
