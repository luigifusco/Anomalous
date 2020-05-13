import glob
import os
import numpy as np

from src.signals import create_dataset
from src.learning import train_model

filelist = [filename.split('.')[0] for filename in glob.glob('data/files/*.dat')]
notes = ['A', 'F', 'Q', 'n', 'R', 'B', 'S', 'j', '+', 'V']

# create and save datasets (mal files)
for note in notes:
    print("creating dataset for anomaly", note)
    trainX, trainY, testX, testY = create_dataset(note, filelist, 257)
    print("saving...")
    with open('data/mals/mal_' + note + '.mal', 'wb') as file:
        np.savez(file,
                 trainX=np.array(trainX, dtype=np.float32),
                 trainY=np.array(trainY, dtype=np.uint8),
                 testX=np.array(testX, dtype=np.float32),
                 testY=np.array(testY, dtype=np.uint8)
                 )

for note in notes:
    print("creating net for anomaly", note)
    data = np.load(os.path.join('mals', 'mal_' + note + '.mal'))
    model = train_model(data['trainX'], data['trainY'], data['testX'], data['testY'])
    print("saving...")
    model.save(os.path.join('models', 'model_' + note + '.h5'))
