import numpy as np
import time

from alexnet import alexnet

WIDTH = 118
HEIGHT = 62
LR = 1e-3
EPOCHS = 20

MODEL_NAME = 'deephorizon-{}-{}-{}-{}-epochs.model'.format('alexnet', EPOCHS, LR, int(time.time()))
model = alexnet(WIDTH, HEIGHT, LR)

file_name = '.../data/training_data_balanced-combined.npy'
training_data = np.load(file_name)

train = training_data[:-2000]
test = training_data[-2000:]

X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
Y = [i[1] for i in train]

test_X = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
test_Y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS, 
            validation_set=({'input': test_X}, {'targets': test_Y}),
            snapshot_step=500, show_metric=True, run_id=MODEL_NAME)


model.save("../models/{}".format(MODEL_NAME))
