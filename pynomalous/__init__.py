"""
Pynomalous is a tool for the automatic analysis of ECG signals, developed as a project for
the "Progetto di Ingegneria Informatica" exam

This is the main module, containing the object interface to all functionalities
"""

from pynomalous.learning.predicting import load_trained_net
from pynomalous.signals.processing import get_filter, filter_signal, get_bpm, split_overlapping, get_bradycardia_level, get_tachycardia_level
from pynomalous.miscellaneous import get_notes


class Pynomalous:
    """
    Main class used as an interface to the whole system. It is used by the GUI
    """
    def __init__(self):
        self.notes = get_notes()
        self.nets = {n: load_trained_net(n) for n in self.notes}
        self.filt = get_filter()

    def predict_segments(self, segments, note):
        """
        Gets a list of segments and returns a list of predictions for each segment
        :param segments: list of numpy arrays
        :param note: anomaly to find
        :return: list of predictions
        """
        return self.nets[note].predict_classes(segments)

    def analyze_signal(self, signal, age, freq=257):
        analysis = {"bpm": {}, "anomalies": {}}
        signal = filter_signal(signal, self.filt, freq)
        bpm = get_bpm(signal[:, 0])
        analysis["bpm"] = {
            "value": bpm,
            "tachycardia": get_tachycardia_level(bpm, age),
            "bradychardia": get_bradycardia_level(bpm)
        }
        segments, times = split_overlapping(signal)
        for note in self.notes:
            predictions = self.predict_segments(segments, note)
            analysis["anomalies"][note] = {
                "rateo": predictions.count(note) / len(predictions),
                "positions": [t for t, p in zip(times, predictions) if p == note]
            }

        return analysis
