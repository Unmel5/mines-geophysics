import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib 
import unittest
from unittest.mock import patch
import dascore as dc
from dascore.utils.downloader import fetch
def compute_sta(timeseries, samplingrate, stawindowduration): #short term average of the signal over a window duration
    stawindowlength = int(stawindowduration * samplingrate)
    stavalues = np.array([np.mean(np.abs(timeseries[i:i+stawindowlength])) 
                          for i in range(len(timeseries) - stawindowlength)])
    return stavalues

def compute_lta(timeseries, samplingrate, ltawindowduration): #long term average of the signal over a window duration 
    ltawindowlength = int(ltawindowduration * samplingrate)
    ltavalues = np.array([np.mean(np.abs(timeseries[i:i+ltawindowlength])) 
                          for i in range(len(timeseries) - ltawindowlength)])
    return ltavalues

def compute_ratio(stavalues, ltavalues): #the ratio of STA to LTA values to identify events
    min_length = min(len(stavalues), len(ltavalues))
    stavalues = stavalues[:min_length]
    ltavalues = ltavalues[:min_length]
    ratio = np.maximum(stavalues / ltavalues, 1)    
    return ratio

def detect_events(ratio, detection_threshold, samplingrate): #identifies events based on STA/LTA ratio exceeding a detection threshold 
    min_event_duration_samples = int(0.05 * samplingrate)
    min_event_separation_samples = int(0.5 * samplingrate)
    events = []
    event_active = False
    event_start = None

    for i in range(len(ratio)):
        if ratio[i] > detection_threshold:
            if not event_active:
                event_start = i
                event_active = True
        else:
            if event_active:
                event_end = i
                event_active = False
                if event_end - event_start >= min_event_duration_samples:
                    if len(events) == 0 or event_start - events[-1][1] >= min_event_separation_samples:
                        events.append((event_start, event_end))

    return events

def staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold):
    ltawindowlength = int(ltawindowduration * samplingrate)  # convert the window durations from seconds to samples
    stavalues = compute_sta(timeseries, samplingrate, stawindowduration)
    ltavalues = compute_lta(timeseries, samplingrate, ltawindowduration)
    ratio = compute_ratio(stavalues, ltavalues)
    events = detect_events(ratio, detection_threshold, samplingrate)
    return stavalues, ltavalues, ratio, events
samplingrate = 100.0
duration = 3600  # seconds
t = np.linspace(0, duration, int(duration * samplingrate)) #time vector t that spans from 0 to 3600 seconds with a total of int(duration * samplingrate) points. linsapce creates a llinearly spaced array of time spoints. this array is used to simulate the axis for synthetic data to ensure that each sample has a timestamp
np.random.seed(0) 
background_noise = np.random.normal(0, 1e-6, len(t)) #background noise as a normal (gaussian) distribution with a mean of 0 and a sd of 1 * 10^-6 with the same length as the time vector 't'
timeseries = background_noise.copy() #timeseries variable will be used as the main input for the STA/LTA algorithm. 

# Add synthetic seismic events added to the timeseries at specific indices with varying frequencies and amplitudes to simulate seismic events 
event_indices = [(2000, 2050), (2070, 2080), (2200, 2230), (2270, 2280), (2330, 2340), (2350, 2360)]
event_frequencies = [20, 30, 40, 50, 20, 30]
event_amplitudes = [10e-6, 15e-6, 10e-6, 15e-6, 10e-6, 15e-6]

for (start, end), freq, amp in zip(event_indices, event_frequencies, event_amplitudes):
    start_idx = int(start * samplingrate)
    end_idx = int(end * samplingrate)
    event_time = t[start_idx:end_idx]
    timeseries[start_idx:end_idx] += amp * np.sin(2 * np.pi * freq * event_time)

# Run the STA/LTA trigger, staltatrigger function is called with the generated timeseries and parameters such as STA and LTA window durations, step size durations and detection threshold 
stawindowduration = 0.03
ltawindowduration = 0.1
stepsizeduration = 0.01
detection_threshold = 2.0
sta, lta, ratio, events = staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)

# Adjust lengths of the time arrays
ltawindowlength = int(ltawindowduration * samplingrate)
time_stalta = t[ltawindowlength:ltawindowlength + len(ratio)]

# Plot the results
plt.figure(figsize=(14, 12))

# Plot the original timeseries
plt.subplot(3, 1, 1)
plt.plot(t, timeseries, label='Original Time Series', color='blue', linewidth=0.5)
plt.axhline(y=5e-6, color='r', linestyle='--')
plt.axhline(y=-5e-6, color='r', linestyle='--')
plt.title('Original Time Series')
plt.xlabel('Time (sec)')
plt.ylabel('Amplitude')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

# Plot STA and LTA values
plt.subplot(3, 1, 2)
plt.plot(time_stalta, sta[:len(time_stalta)], label='STA', color='orange', linewidth=0.5)
plt.plot(time_stalta, lta[:len(time_stalta)], label='LTA', color='green', linewidth=0.5)
plt.title('STA and LTA Values')
plt.xlabel('Time (sec)')
plt.ylabel('Amplitude')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

# Plot STA/LTA ratio and detected events
plt.subplot(3, 1, 3)
plt.plot(time_stalta, ratio, label='STA/LTA Ratio', color='purple', linewidth=0.5)
plt.axhline(y=detection_threshold, color='red', linestyle='--', linewidth=2)  # Add detection threshold line
plt.title('STA/LTA Ratio and Detected Events')
plt.xlabel('Time (sec)')
plt.ylabel('STA/LTA Ratio')
plt.ylim(0, 3)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

# Mark detected events
for event in events:
    plt.axvspan(time_stalta[event[0]], time_stalta[event[1]], color='green', alpha=0.3)

plt.show()
