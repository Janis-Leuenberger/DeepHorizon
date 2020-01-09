import numpy as np
from alexnet import alexnet
import time

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 20

MODEL_NAME = 'deephorizon-{}-{}-{}-{}-epochs.model'.format(LR, 'alexnet', EPOCHS, int(time.time()))

model = alexnet(WIDTH, HEIGHT, LR)

file_name = '../data/D1/training_data_balanced-52452-V2.npy'
training_data = np.load(file_name)

train = training_data[:-1000]
test = training_data[-1000:]

X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
Y = [i[1] for i in train]

test_X = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
test_Y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS, 
            validation_set=({'input': test_X}, {'targets': test_Y}),
            snapshot_step=500, show_metric=True, run_id=MODEL_NAME)



# tensorboard --logdir=foo:C:/Users/janis/Desktop/Tensorflow/DeepHorizon/MachineLearning/logs

model.save("../models/new_try/{}".format(MODEL_NAME))