import os

from src.learning.training import get_model


def load_model_with_weights(mal, weights_root='data/models/'):
    model = get_model()
    model.load_weights(os.path.join(weights_root, 'model_' + mal + '.h5'))

    return model
