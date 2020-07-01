"""
Contrains functions relative to predicting using the neural networks
"""

import os

from pynomalous.learning.training import get_model
from keras.models import load_model


def load_trained_net(mal):
    """
    Generates a neural network, loads in the neural network the pretrained weights and returns it

    :param mal: the mal the net has to recognize
    :param weights_root: the root directory of the network weights
    :return: the trained model
    """
    model_root = os.path.join(os.getcwd(), 'data', 'models')
    model = load_model(os.path.join(model_root, 'model_' + mal + '.h5'))

    return model
