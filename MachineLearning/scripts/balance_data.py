import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

file_name = '../data/D1/training_data.npy'
training_data = np.load(file_name)

df = pd.DataFrame(training_data)
print(df.head())
print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []
nothings = []

# shuffling the list fucks with my programm
# data is going to be shuffled later
# legit i am so pissed 
# wtf is this bullshit?
# shuffle(training_data)

for data in training_data:
    img = data[0]
    choice = data[1]

    if choice == [1, 0, 0]:
        lefts.append([img, choice])
    elif choice == [0, 1, 0]:
        forwards.append([img, choice])
    elif choice == [0, 0, 1]:
        rights.append([img, choice])
    elif choice == [0, 0, 0]:
        nothings.append([img, choice])
    else:
        print("ERROR unknown keycode")

shuffle(lefts) 
shuffle(rights) 
shuffle(forwards) 
shuffle(nothings) 

#print(len(forwards), len(nothings), len(lefts), len(rights))

max_size = min([len(lefts), len(rights), len(forwards), len(nothings)])

print("max_size: {}".format(max_size))

lefts = lefts[:max_size]
rights = rights[:max_size]
forwards = forwards[:max_size]
nothings = nothings[:max_size]

final_data = lefts + rights + forwards + nothings

shuffle(final_data)

print("initial data size: " + str(len(training_data)))
print("final data size: " + str(len(final_data)))
np.save('../data/D1/training_data_balanced-{}-V2.npy'.format(len(final_data)), final_data)

#for data in training_data:
#    img = data[0]
#    choice = data[1]

#    #visualization
#    cv2.imshow('test', cv2.resize(img, (800, 600)))
#    print(choice)

#    if cv2.waitKey(25) % 0xFF == ord('q'):
#        cv2.destroyAllWindows()
#        break