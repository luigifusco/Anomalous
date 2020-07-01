import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from pynomalous import Pynomalous

if __name__ == '__main__':
    pyn = Pynomalous()
    print('Successfully loaded Pynomalous!')
    print('Running tests...')
    print('notes found: ' + ', '.join(pyn.notes))
    for note in pyn.notes:
        print('Testing anomaly ' + note)
        testX, testY = pyn.load_test_data(note)
        net = pyn.nets[note]
        score, acc = net.evaluate(testX, testY)
        print('Accuracy: ' + str(acc))
        print()
    print('Done!')