import random
import wfdb
import numpy as np
import scipy.signal
import sklearn.model_selection


def create_segmented_signals(signal, annmap, sample_rate, sec):
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


def filter_signal(signal, sample_rate, n_samp):
    filt = scipy.signal.firwin(n_samp, cutoff=5, fs=sample_rate, pass_zero='highpass')
    padding = (n_samp // 2)

    return np.convolve(signal, filt)[padding:-padding]


def create_dataset(note, filelist, sample_rate):
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
        for i in range(signal.shape[-1]):
            signal[:, i] = filter_signal(signal[:, i], sample_rate, 101)

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
