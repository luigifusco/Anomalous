"""
Contains function to manipulate raw data
"""

import scipy.signal
import numpy as np
import heartpy as hp


def filter_signal(signal, sample_rate, n_samp):
    """
    Filters signals

    :param signal: the data to filter
    :param sample_rate: sample rate of the data
    :param n_samp: number of samples of the filter
    :return:
    """
    filt = scipy.signal.firwin(n_samp, cutoff=5, fs=sample_rate, pass_zero='highpass')
    padding = (n_samp // 2)

    return np.convolve(signal, filt)[padding:-padding]


def obtain_bpm(ecg_signal, sample_rate, start_at, finish_at):
    """
    calculate bpm filtering the signal and upsampling it for better results
    :param ecg_signal: 1 lead from an ecg
    :param sample_rate: the sample rate of the ecg
    :param start_at: this defines the start portion of the ecg that you want to analyse
    :param finish_at: this defines the end portion of the ecg that you want to analyse
    :return: the bpm for the given sequence
    """
    filtered = hp.filter_signal(ecg_signal[start_at:finish_at], cutoff=5, sample_rate=sample_rate,
                                filtertype='highpass')
    upsampled = scipy.signal.resample(filtered, len(filtered) * 4)
    wd, m = hp.process(hp.scale_data(upsampled), sample_rate * 4)

    for measure in m.keys():
        if measure == 'bpm':
            return m[measure]


def tachycardia_level(age, bpm):
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


def bradycardia_level(bpm):
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
