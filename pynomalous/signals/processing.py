"""
Contains function to manipulate raw data
"""

import scipy.signal
import numpy as np
import heartpy as hp


def get_filter():
    return scipy.signal.firwin(n_samp, cutoff=5, fs=sample_rate, pass_zero='highpass')


def filter_signal(signal, filt, sample_rate=257, n_samp=101):
    """
    Filters signals

    :param signal: the data to filter
    :param sample_rate: sample rate of the data
    :param n_samp: number of samples of the filter
    :return:
    """
    newsig = np.array(signal)
    padding = (n_samp // 2)
    for i in range(newsig.shape[-1]):
        newsig[:, i] = np.convolve(newsig[:, i], filt)[padding:-padding]

    return newsig


def get_bpm(ecg_signal, sample_rate, start_at, finish_at):
    """
    calculate bpm filtering the signal and upsampling it for better results
    :param ecg_signal: 1 lead from an ecg
    :param sample_rate: the sample rate of the ecg
    :param start_at: this defines the start portion of the ecg that you want to analyse
    :param finish_at: this defines the end portion of the ecg that you want to analyse
    :return: the bpm for the given sequence
    """
    upsampled = scipy.signal.resample(filtered, len(filtered) * 4)
    wd, m = hp.process(hp.scale_data(upsampled), sample_rate * 4)

    for measure in m.keys():
        if measure == 'bpm':
            return m[measure]


def get_tachycardia_level(age, bpm):
    """
    This function returns the level 0->1->2 where 2 is the maximum of tachycardia
    :param age: the age of the patient
    :param bpm: the registered bpm
    :return: the level of tachycardia
    """
    if age <= 45:
        if bpm > 180:
            return 2
        elif bpm > 153:
            return 1
        else:
            return 0
    elif age <= 50:
        if bpm > 175:
            return 2
        elif bpm > 149:
            return 1
        else:
            return 0
    elif age <= 55:
        if bpm > 170:
            return 2
        elif bpm > 145:
            return 1
        else:
            return 0
    elif age <= 60:
        if bpm > 165:
            return 2
        elif bpm > 140:
            return 1
        else:
            return 0
    elif age <= 65:
        if bpm > 160:
            return 2
        elif bpm > 136:
            return 1
        else:
            return 0
    elif age <= 70:
        if bpm > 155:
            return 2
        elif bpm > 132:
            return 1
        else:
            return 0
    elif age > 70:
        if bpm > 150:
            return 2
        elif bpm > 128:
            return 1
        else:
            return 0


def get_bradycardia_level(bpm):
    """
    Returns the bradycardia level for the corresponding bpm
    :param bpm: the revealed bpm
    :return: the level
    """
    if bpm > 60:
        return 0
    elif bpm > 50:
        return 1
    else:
        return 2


def split_overlapping(signal, freq=257, time=2, shift=0.5):
    """
    Splits the signal data into segments. Expects signal with dim-0 samples, dim-1 leads (12)
    :param signal: the signal
    :param freq: frequency rate of the signal
    :param time: time length of the segments
    :param shift: time shift in taking different section
    :return: list of signal segments
    """
    seglen = int(freq*time)
    shiftlen = int(shift*time)
    siglen = signal.shape[0]

    return [signal[i:i+seglen, :] for i in range(0, siglen-seglen, shiftlen)]
