import heartpy as hp
from scipy.signal import resample


# ecg_signal is an array containing the mesurments
def obtain_bpm(ecg_signal, sample_rate, start_at, finish_at):
    filtered = hp.filter_signal(ecg_signal[start_at:finish_at], cutoff=5, sample_rate=sample_rate, filtertype='highpass')
    upsampled = resample(filtered, len(filtered) * 4)
    wd, m = hp.process(hp.scale_data(upsampled), sample_rate * 4)

    for measure in m.keys():
        if measure == 'bpm':
            return m[measure]