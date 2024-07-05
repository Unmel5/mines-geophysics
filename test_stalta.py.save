import numpy as np
import unittest

def staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold):
    num_samples = len(timeseries)
    sta_samples = int(stawindowduration * samplingrate)
    lta_samples = int(ltawindowduration * samplingrate)
    step_samples = int(stepsizeduration * samplingrate)
    
    sta = np.zeros(num_samples)
    lta = np.zeros(num_samples)
    ratio = np.zeros(num_samples)
    
    for i in range(lta_samples, num_samples, step_samples):
        sta[i] = np.mean(timeseries[i-sta_samples:i])
        lta[i] = np.mean(timeseries[i-lta_samples:i])
        if lta[i] > 0:
            ratio[i] = sta[i] / lta[i]
    
    events = []
    event_start = None
    for i in range(num_samples):
        if ratio[i] >= detection_threshold and event_start is None:
            event_start = i
        elif ratio[i] < detection_threshold and event_start is not None:
            events.append((event_start, i))
            event_start = None
    
    return sta, lta, ratio, events

class TestSTALTA(unittest.TestCase):

    def test_stalta_detection(self):
        # Parameters
        samplingrate = 100.0
        duration = 10  # seconds
        num_samples = int(duration * samplingrate)
        stawindowduration = 0.1
        ltawindowduration = 1.0
        stepsizeduration = 0.01
        detection_threshold = 2.0

        # Generate synthetic data
        t = np.linspace(0, duration, num_samples)
        timeseries = np.ones(num_samples)
        spike_start = int(5 * samplingrate)
        spike_end = spike_start + int(0.5 * samplingrate)
        timeseries[spike_start:spike_end] = 5
        
        # Generate background noise
        np.random.seed(0)
        background_noise = np.random.normal(0, 1e-6, num_samples)
        timeseries += background_noise

        sta, lta, ratio, events = staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)

        # Test that the STA/LTA ratio reached or exceeded the detection threshold
        self.assertTrue(np.any(ratio >= detection_threshold), "STA/LTA ratio did not reach the detection threshold")

        # Test that at least one event was detected
        self.assertTrue(len(events) > 0, "No events were detected")

        # Test that the STA/LTA ratio was above the threshold during detected events
        for event in events:
            event_ratios = ratio[event[0]:event[1]]
            self.assertTrue(np.all(event_ratios >= detection_threshold), "STA/LTA ratio was not above the threshold during detected events")

        # Additional test to run all values in the STA/LTA arrays are non-negative
        self.assertTrue(np.all(sta >= 0), "STA values should be non-negative")
        self.assertTrue(np.all(lta >= 0), "LTA values should be non-negative")

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
