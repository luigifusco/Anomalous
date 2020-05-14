"""
Contains functions relative to neural network creation and training
"""

from keras.models import Sequential
from keras.layers import Dense, Activation, Conv1D, MaxPooling1D, Flatten
import numpy as np
import os

import src.miscellaneous


def get_model():
    """
    Generates and return the standard convolution based neural network

    :return: the neural network
    """
    return Sequential([
        Conv1D(32, kernel_size=5, input_shape=(514, 12)),
        MaxPooling1D(),
        Activation('relu'),
        Conv1D(64, kernel_size=5),
        MaxPooling1D(),
        Activation('relu'),
        Conv1D(128, kernel_size=5),
        MaxPooling1D(),
        Activation('relu'),
        Flatten(),
        Dense(20),
        Activation('relu'),
        Dense(2),
        Activation('softmax')
    ])


def train_model(model, trainX, trainY, testX, testY):
    """
    Compiles the model and trains it on the input training data

    :param model: the model to compile and train
    :param trainX: the train data
    :param trainY: the train labels
    :param testX: the test data
    :param testY: the test labels

    :return:  the trained model
    """
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(trainX,
              trainY,
              epochs=10,
              batch_size=32,
              validation_data=(testX, testY))

    return model


def create_and_save_networks(root='data/mals/'):
    """
    Creates and trains neural networks for all notes (as returned by src.miscellaneous.get_notes())

    :param root: the root of the mals
    """
    notes = src.miscellaneous.get_notes()

    for note in notes:
        print("creating net for anomaly", note)
        data = np.load(os.path.join(root, 'mal_' + note + '.mal'))
        model = train_model(data['trainX'], data['trainY'], data['testX'], data['testY'])
        print("saving...")
        model.save(os.path.join('models', 'model_' + note + '.h5'))