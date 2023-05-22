from warnings import warn

from tensorflow.keras.layers import MaxPool1D, Activation, Layer, Conv1D, Dense, Dropout, Reshape, Flatten, Add, \
    MaxPool1D, BatchNormalization, ZeroPadding1D

import numpy as np

import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices("GPU")
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
import random

random.seed(10)
np.random.seed(10)

from tensorflow.keras.models import Sequential
import pickle



from warnings import warn
from tensorflow.keras.layers import Conv1D, Dense, Dropout, Reshape, Flatten
import pandas as pd
import numpy as np
from collections import OrderedDict
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow.keras.backend as K
from statistics import mean
import os
import json


# The following are the parameters that were used during the preprocessing phase 
# when training these models. You can use them to generate the predictions. 


MAINS_MEAN = 1800
MAINS_STD = 600

APP_PARAMS = {'washing machine': {'mean': 34.28564, 'std': 224.33687}, 
              'fridge': {'mean': 39.32627, 'std': 50.269016}, 
              'kettle': {'mean': 14.282732, 'std': 167.7649}, 
              'microwave': {'mean': 7.1103287, 'std': 88.2785}}



def return_seq2point():
    model = Sequential()
    model.add(Conv1D(30, 10, activation="relu", input_shape=(99, 1), strides=1))
    model.add(Conv1D(30, 8, activation='relu', strides=1))
    model.add(Conv1D(40, 6, activation='relu', strides=1))
    model.add(Conv1D(50, 5, activation='relu', strides=1))
    model.add(Dropout(.2))
    model.add(Conv1D(50, 5, activation='relu', strides=1))
    model.add(Dropout(.2))
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(.2))
    model.add(Dense(1))
    optim = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(loss='mse', optimizer=optim)  # ,metrics=[mse])
    return model


def return_seq2seq():
    model = Sequential()
    model.add(Conv1D(30, 10, activation="relu", input_shape=(99, 1), strides=2))
    model.add(Conv1D(30, 8, activation='relu', strides=2))
    model.add(Conv1D(40, 6, activation='relu', strides=1))
    model.add(Conv1D(50, 5, activation='relu', strides=1))
    model.add(Dropout(.2))
    model.add(Conv1D(50, 5, activation='relu', strides=1))
    model.add(Dropout(.2))
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(.2))
    model.add(Dense(99))
    optim = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(loss='mse', optimizer=optim)

    return model

def return_dae():
    model = Sequential()
    sequence_length = 99
    model.add(Conv1D(8, 4, activation="linear", input_shape=(sequence_length, 1), padding="same", strides=1))
    model.add(Flatten())
    model.add(Dense((sequence_length)*8, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense((sequence_length)*8, activation='relu'))
    model.add(Reshape(((sequence_length), 8)))
    model.add(Conv1D(1, 4, activation="linear", padding="same", strides=1))
    model.compile(loss='mse', optimizer='adam')
    return model

def return_forecast():
    """
    A function that returnss the architecture of the forecasting model suggested 
    A pre-trained model can be found here: 
    https://drive.google.com/file/d/1PvcBgNPbCRiBSJBbmkrmpf8QtcuBgWHQ/view?usp=sharing
    """
    model4 = tf.keras.Sequential()
    model4.add(tf.keras.layers.LSTM(32, activation="tanh", dropout=0.1, return_sequences=True, input_shape=(4, 4)))
    model4.add(tf.keras.layers.LSTM(16, activation="tanh", dropout=0.1))
    model4.add(tf.keras.layers.Dense(1))

    opt = tf.keras.optimizers.Adam(learning_rate=0.0001)

    metric = tf.keras.losses.MeanAbsoluteError()
    model4.compile(loss=metric, optimizer=opt, metrics=[metric])
    return model4


def aggregate_seq(prediction):
    """
    For the case of seq2seq model the outputs needs to be postprocessed to generate 
    the predictions through aggregation. As a help, the following function allows to do the post processing.
    """
    l = 99
    n = len(prediction) + l - 1
    sum_arr = np.zeros((n))
    counts_arr = np.zeros((n))
    o = len(sum_arr)
    for i in range(len(prediction)):
        sum_arr[i:i + l] += prediction[i].flatten()
        counts_arr[i:i + l] += 1
    for i in range(len(sum_arr)):
        sum_arr[i] = sum_arr[i] / counts_arr[i]
        
    return sum_arr
