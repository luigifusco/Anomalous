"""
Contains functions to load data from St.Petersburg and to create the specific anomaly datasets
"""


import random
import wfdb
import numpy as np
import sklearn.model_selection
import os

import pynomalous.miscellaneous
from pynomalous.signals.processing import get_filter, filter_signal


def read_and_filter_wfdb(filename, length=None):
    """
    Reads and filters a signal in Physionet format and returns a numpy array

    :param filename: the name of the file
    :param length: the length of the file to return or None for max length
    :return: the filtered and cut signal as a numpy array
    """
    record = wfdb.rdrecord(filename)

    if length is None:
        signal = record.p_signal
    else:
        signal = record.p_signal[:length, :]
    filt = get_filter()
    signal = filter_signal(signal, filt)

    return signal


def segment_signal(signal, length=2, skip=0.5, sample_rate=257):
    """
    Segments a signal into overlapping sections with defined length and skip size

    :param signal: the signal to segment
    :param length: the length of each segment (in seconds)
    :param skip: length of the space between the start of two contiguous signals (in seconds)
    :param sample_rate: the sample rate of the signal
    :return: a list containing numpy arrays representing the signal segments
    """
    seg_len = int(length * sample_rate)
    skip_len = int(skip * sample_rate)
    segments = []
    for i in range(signal.shape[0], skip_len):
        segments.append(signal[i:i+seg_len])

    return segments


def create_segmented_signals(signal, annmap, sample_rate=257, sec=2):
    """
    Creates segmented signals containing all possible anomalies from a signal and its annmap

    :param signal: the signal to segment
    :param annmap: map containing the positions of the annotations
    :param sample_rate: the sample rate of the signal
    :param sec: length of the segments
    :return: a list of dictionaries containing the segments and metadata
    """
    seg_len = sec * sample_rate
    segments = []

    curr_ini = curr_fin = 0

    for i, sample in enumerate(annmap):
        if sample['ann'] == 'N':
            if curr_ini == 0:
                if i + 1 < len(annmap) - 1 and annmap[i + 1]['ann'] == 'N':
                    curr_ini = random.randint(sample['time'], annmap[i + 1]['time'])
                else:
                    continue
            curr_fin = sample['time']

            if curr_fin - curr_ini > seg_len and curr_ini + seg_len <= signal.shape[0]:
                segments.append(
                    {
                        'data': signal[curr_ini:curr_ini + seg_len, :],
                        'ann': 'N'
                    }
                )
                curr_ini = curr_fin
        else:
            curr_ini = curr_fin = 0
            if sample['time'] > 2 * seg_len and sample['time'] < signal.shape[0] - 2 * seg_len:
                rand_start = sample['time'] - random.randint(seg_len // 3, 2 * seg_len // 3)
                segments.append(
                    {
                        'data': signal[rand_start:rand_start + seg_len, :],
                        'ann': sample['ann'],
                        'time': sample['time']
                    }
                )

    return segments



def create_dataset(note, sample_rate=257):
    """
    Creates a dataset of a specific anomaly

    :param note: the anomaly
    :param sample_rate: the sample rate of the signals
    :return:
    """

    filt = get_filter()

    filelist = pynomalous.miscellaneous.get_filelist()

    train_test_ratio = 0.3
    threshold = 100

    test_threshold = int(threshold * train_test_ratio)
    train_threshold = threshold - test_threshold

    patient_sane_train = []
    patient_sane_test = []
    patient_ill_train = []
    patient_ill_test = []

    for file in filelist:
        segments = []
        record = wfdb.rdrecord(file)
        annotations = wfdb.rdann(file, 'atr')
        annmap = [{'time': samp, 'ann': symb} for samp, symb in zip(annotations.sample, annotations.symbol) if
                  symb == note or symb == 'N']

        # signal transformation pipeline
        signal = record.p_signal
        signal = filter_signal(signal, filt)

        segments += create_segmented_signals(signal, annmap, sample_rate, 2)
        del signal

        sane_segments = [s['data'] for s in segments if s['ann'] == 'N']
        ill_segments = [s['data'] for s in segments if s['ann'] != 'N']
        del segments

        if len(sane_segments) == 0 or len(ill_segments) == 0:
            continue

        try:
            sane_train, sane_test = sklearn.model_selection.train_test_split(sane_segments, test_size=train_test_ratio)
            ill_train, ill_test = sklearn.model_selection.train_test_split(ill_segments, test_size=train_test_ratio)
        except Exception:
            continue

        if len(sane_train) == 0 or len(sane_test) == 0 or len(ill_train) == 0 or len(ill_test) == 0:
            continue

        while len(sane_train) < train_threshold:
            sane_train += sane_train
        while len(sane_test) < test_threshold:
            sane_test += sane_test
        while len(ill_train) < train_threshold:
            ill_train += ill_train
        while len(ill_test) < test_threshold:
            ill_test += ill_test

        patient_sane_train += sane_train[:train_threshold]
        patient_sane_test += sane_test[:test_threshold]
        patient_ill_train += ill_train[:train_threshold]
        patient_ill_test += ill_test[:test_threshold]

    trainX = np.array(patient_sane_train + patient_ill_train)
    trainY = [[1, 0]] * len(patient_sane_train) + [[0, 1]] * len(patient_ill_train)
    testX = patient_sane_test + patient_ill_test
    testY = [[1, 0]] * len(patient_sane_test) + [[0, 1]] * len(patient_ill_test)

    return trainX, trainY, testX, testY


def create_and_save_datasets(root='data/mals/'):
    """
    Main function to create datasets and save them

    :param root: the root folder to save the datasets
    """
    notes = pynomalous.miscellaneous.get_notes()
    filelist = pynomalous.miscellaneous.get_filelist()

    for note in notes:
        print("creating dataset for anomaly", note)
        trainX, trainY, testX, testY = create_dataset(note, filelist)
        print("saving...")
        with open(os.path.join(root, 'mal_' + note + '.mal'), 'wb') as file:
            np.savez(file,
                     trainX=np.array(trainX, dtype=np.float32),
                     trainY=np.array(trainY, dtype=np.uint8),
                     testX=np.array(testX, dtype=np.float32),
                     testY=np.array(testY, dtype=np.uint8)
                     )