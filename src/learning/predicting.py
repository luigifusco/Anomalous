"""
Contrains functions relative to predicting using the neural networks
"""

import os

from src.learning.training import get_model


def load_weights(mal, weights_root='data/models/'):
    """
    Generates a neural network, loads in the neural network the pretrained weights and returns it

    :param mal: the mal the net has to recognize
    :param weights_root: the root directory of the network weights
    :return: the trained model
    """
    model = get_model()
    model.load_weights(os.path.join(weights_root, 'model_' + mal + '.h5'))

    return model
