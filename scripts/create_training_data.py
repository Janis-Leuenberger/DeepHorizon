import numpy as np
import cv2
import time
import os

from grab_screen import grab_screen
from get_keys import key_check
from set_forza import setforza

def keys_to_output(keys):
    #        [A, W, D, N]
    output = [0, 0, 0, 0]

    if 'Z' in keys:
        print("exiting... ")
        exit()
    elif 'A' in keys:
        output[0] = 1
    elif '+' in keys:
        output[2] = 1
    elif 'W' in keys:
        output[1] = 1
    else:
        output[3] = 1

    return output

# Region of interest
def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def main():
    #countdown
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    vertices = np.array(
            [[5,600], [5,300], [250,180], [550,180], [795,300], [795,600]], 
            np.int32)
    
    while True:
        #record screen and convert
        screen = grab_screen(region=(17, 33, 800, 600))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        #roi        
        screen = roi(screen, [vertices])
        screen = cv2.resize(screen, (120, 90))

        #record key input
        keys = key_check()
        output = keys_to_output(keys)

        #save training data
        training_data.append([screen, output])
        if len(training_data) % 4000 == 0:
            print("Saving... Size: " + str(len(training_data)))
            np.save(file_name, training_data)
        
        if len(training_data) % 10000 == 0:
            print("Backing up... Size: " + str(len(training_data)))
            np.save(file_name + "-{}".format(int(time.time())), training_data)


# if there is no folder for the current version create one
if not os.path.exists("../data/"):
    print("Making new directory...")
    os.makedirs("../data/")

# load training data if exists
file_name = "../data/training_data.npy"
if os.path.isfile(file_name):
    print("file exists, loading data")
    training_data = list(np.load(file_name))
else:
    print("file doesn't exist, creating new file")
    training_data = []

set_forza()
main()