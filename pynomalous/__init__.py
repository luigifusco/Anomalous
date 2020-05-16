from pynomalous.learning.predicting import load_trained_net
from pynomalous.signals.processing import get_filter, filter_signal, get_bpm, split_overlapping


class Pynomalous:
    def __init__(self, notes):
        self.notes = notes
        self.nets = {n: load_trained_net(n) for n in notes}
        self.filt = get_filter()

    def predict_segments(self, segments, note):
        """
        Gets a list of segments and returns a list of predictions for each segment
        :param segments: list of numpy arrays
        :return: list of predictions
        """
        return self.nets[note].predict_classes(segments)

    def analyze_signal(self, signal, freq=257):
        analysis = {"anomalies": {}}
        signal = filter_signal(signal, self.filt, freq)
        analysis["bpm"] = get_bpm(signal[:,0])
        segments = split_overlapping(signal)
        for note in self.notes:
            analysis["anomalies"][note] = self.predict_segments(segments, note)

        return analysis
