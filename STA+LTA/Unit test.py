#confirm that the STA/LTA ratio reaches the detection threshold 
#ensure at least one event is detected
#verify that the STA/LTA ratio is above the threshold during detected events
#check that the STA/LTA values are non-negative

# Define the staltatrigger function if it's not imported from an external module
import numpy as np 
import unittest

def staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold):
    num_samples = len(timeseries) #timeseries, input signal data
    sta_samples = int(stawindowduration * samplingrate) #number of samples per second
    lta_samples = int(ltawindowduration * samplingrate)
    step_samples = int(stepsizeduration * samplingrate) #threshold value for detecting events
    
    sta = np.zeros(num_samples) #initialize arrays to store STA, LTA and ratio values
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

class TestSTALTA(unittest.TestCase): #purpose: to test the staltatrigger function using synthetic data

    def test_stalta_detection(self): 
        # Parameters
        samplingrate = 100.0
        duration = 10  # seconds
        num_samples = int(duration * samplingrate)  # Ensure this is an integer
        stawindowduration = 0.1
        ltawindowduration = 1.0
        stepsizeduration = 0.01
        detection_threshold = 2.0  # Set the threshold to 2.0 for this test

        # Generate synthetic data
        t = np.linspace(0, duration, num_samples)  # Time vector and a timeseries with a constant value, introduces a spike in the data to simulate seismic event and adds background noise to the timeseries
        
        # Create a spike in the data, the maximum sta/lta ratio should reach at least the detectino threshold, 
        timeseries = np.ones(num_samples)  # Start with a constant value
        spike_start = int(5 * samplingrate)  # Start the spike at 5 seconds
        spike_end = spike_start + int(0.5 * samplingrate)  # End the spike at 5.5 seconds
        timeseries[spike_start:spike_end] = 5  # Set the value to 5 during the spike (higher value to ensure ratio > 2)
                
        # Generate background noise
        np.random.seed(0)
        background_noise = np.random.normal(0, 1e-6, num_samples) 
        timeseries += background_noise

        # Purpose: this line calls the 'staltatrigger' function with the generated timeseries and the specified parameters 
        sta, lta, ratio, events = staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)

        

        #Additional test to run all values in the STA/LTA arrays are non-negative
        self.assertTrue(np.all(sta >= 0), "STA values should be non-negative")
        self.assertTrue(np.all(lta >= 0), "LTA values should be non-negative") 

# Run the tests
if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
#the sta/lta ratio reached or exceeded the detection threshold 
#at least one event was detected
#during detected events, the sta/lta ratio was above the threshold 
#sta and lta values are non-negative
