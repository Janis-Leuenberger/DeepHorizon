import numpy as np
import cv2
import time
from grabscreen import grab_screen
from getkeys import key_check
import os

from get_version import DATA_VERSION

def keys_to_output(keys):
    #        [A, W, D]
    output = [0, 0, 0]

    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    elif 'W' in keys:
        output[1] = 1

    return output

def main():
    #countdown
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    
    while True:
        #record screen and convert
        screen = grab_screen(region=(0, 40, 800, 640))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80, 60))

        #record key input
        keys = key_check()
        output = keys_to_output(keys)

        #save training data
        training_data.append([screen, output])
        if len(training_data) % 2000 == 0:
            print("Saving... Size: " + str(len(training_data)))
            np.save(file_name, training_data)
        
        if len(training_data) % 10000 == 0:
            print("Backing up... Size: " + str(len(training_data)))
            np.save(file_name + "-{}".format(int(time.time())), training_data)

        #print time frame  took
        #print('Frame took {} seconds'.format(time.time()-last_time))
        #last_time = time.time()


# if there is no folder for the current version create one
if not os.path.exists('../data/{}/'.format(DATA_VERSION)):
    print('Making new directory for Version {}'.format(DATA_VERSION))
    os.makedirs('../data/{}/'.format(DATA_VERSION))

# load training data if exists
file_name = '../data/{}/training_data.npy'.format(DATA_VERSION)
if os.path.isfile(file_name):
    print("file exists, loading data")
    training_data = list(np.load(file_name))
else:
    print("file doesn't exist, creating new file")
    training_data = []

main()


