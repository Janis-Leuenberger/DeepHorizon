import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

file_name = '../data/training_data-combined.npy'
training_data = np.load(file_name)

df = pd.DataFrame(training_data)
print(df.head())
print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []

# shuffling the list fucks with my programm
# data is going to be shuffled later
# legit i am so pissed 
# wtf is this bullshit?
# python why did u let me down? :(

for data in training_data:
    img = data[0]
    choice = data[1]

    #        [A, W, D, N]

    if choice == [1, 0, 0, 0]:
        lefts.append([img, [1, 0, 0]])
    elif choice == [0, 1, 0, 0]:
        forwards.append([img, [0, 1, 0]])
    elif choice == [0, 0, 1, 0]:
        rights.append([img, [0, 0, 1]])
    elif choice == [0, 0, 0, 1]:
        continue
        #nothings.append([img, [0, 0, 0]])
    else:
        print("ERROR unknown keycode")

shuffle(lefts) 
shuffle(rights) 
shuffle(forwards) 

max_size = min([len(lefts), len(rights), len(forwards)])

print("max_size: {}".format(max_size))

lefts = lefts[:max_size]
rights = rights[:max_size]
forwards = forwards[:max_size]

final_data = lefts + rights + forwards

shuffle(final_data)

print("initial data size: " + str(len(training_data)))
print("final data size: " + str(len(final_data)))
np.save('../data/training_data_balanced-combined.npy'.format(len(final_data)), final_data)
