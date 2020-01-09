import numpy as np
import cv2
import time
from grabscreen import grab_screen
from getkeys import key_check
from alexnet import alexnet
import os

from get_version import DATA_VERSION, WIDTH, HEIGHT, LR, EPOCHS

from directkeys import PressKey, ReleaseKey, W, A, S, D

name = 'deephorizon-0.001-alexnet-20-1578519745-epochs.model'
MODEL_NAME = '../models/new_try/{}'.format(name)

speed = False

threshhold = 0.75
threshhold_2 = 0.25

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    global speed
    if(speed):
        PressKey(W)
        speed = False
    else:
        ReleaseKey(W)
        speed = True
    #ReleaseKey(W)
    
    PressKey(A)
    ReleaseKey(D)

def right():
    global speed
    if(speed):
        PressKey(W)
        speed = False
    else:
        ReleaseKey(W)
        speed = True
    #ReleaseKey(W)

    ReleaseKey(A)
    PressKey(D)

def slow_ya_roll():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)


def main():
    #countdown
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    
    paused = False
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
        screen = grab_screen(region=(0, 40, 800, 640))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80, 60))

        prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
        moves = list(np.around(prediction))

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
            slow_ya_roll()
            choices[3] += 1
        else:
            print("duck")

        # if prediction[0] > threshhold:
        #     left()
        #     choices[0] += 1
        # elif prediction[2] > threshhold:
        #     right()
        #     choices[2] += 1
        # elif prediction[1] > threshhold_2:
        #     straight()
        #     choices[1] += 1

        
        
        cv2.imshow('test', cv2.resize(screen, (800, 600)))

        if cv2.waitKey(25) % 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        #print time frame  took
        print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()

        # deephorizon-0.001-alexnet-16-D1-1578461649-epochs.model

choices = [0, 0, 0, 0]
try:
    main()
except KeyboardInterrupt:
    print("lefts: {}, forwards: {}, rights: {}, nothings {}".format(choices[0], choices[1], choices[2], choices[3]))
