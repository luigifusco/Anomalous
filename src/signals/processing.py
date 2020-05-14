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


    :param ecg_signal:
    :param sample_rate:
    :param start_at:
    :param finish_at:
    :return:
    """
    filtered = hp.filter_signal(ecg_signal[start_at:finish_at], cutoff=5, sample_rate=sample_rate, filtertype='highpass')
    upsampled = scipy.signal.resample(filtered, len(filtered) * 4)
    wd, m = hp.process(hp.scale_data(upsampled), sample_rate * 4)

    for measure in m.keys():
        if measure == 'bpm':
            return m[measure]
