import numpy as np
import matplotlib.pyplot as plt
import time #measuring the execution time 
import psutil #monitoring system resource usage (e.g. memory usage) 
import pandas as pd #handling and analyzing data  

def compute_sta(timeseries, samplingrate, stawindowduration): #compute the STA and LTA of the time series data 
    stawindowlength = int(stawindowduration * samplingrate)
    stavalues = np.array([np.mean(np.abs(timeseries[i:i+stawindowlength])) 
                          for i in range(len(timeseries) - stawindowlength)])
    return stavalues

def compute_lta(timeseries, samplingrate, ltawindowduration):
    ltawindowlength = int(ltawindowduration * samplingrate)
    ltavalues = np.array([np.mean(np.abs(timeseries[i:i+ltawindowlength])) 
                          for i in range(len(timeseries) - ltawindowlength)])
    return ltavalues

def compute_ratio(stavalues, ltavalues):
    min_length = min(len(stavalues), len(ltavalues))
    stavalues = stavalues[:min_length]
    ltavalues = ltavalues[:min_length]
    ratio = np.maximum(stavalues / ltavalues, 1)  # Ensure ratio doesn't go below 1
    return ratio

def detect_events(ratio, detection_threshold, samplingrate): #iterates through the STA/LTA ratio values and identifies periods where teh ratio exceeds teh detection threshold, marking the start and end of potential events. 
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
    stavalues = compute_sta(timeseries, samplingrate, stawindowduration)
    ltavalues = compute_lta(timeseries, samplingrate, ltawindowduration)
    ratio = compute_ratio(stavalues, ltavalues)
    events = detect_events(ratio, detection_threshold, samplingrate)
    return stavalues, ltavalues, ratio, events

 #executes the scalability test that measures teh execution time and memory usage for different durations of time series data
samplingrate = 100.0  # Hz
durations = [60, 600, 3600, 36000]  # 1 minute, 10 minutes, 1 hour, 10 hours
stawindowduration = 0.03
ltawindowduration = 0.1
stepsizeduration = 0.01
detection_threshold = 2.0



#run the sta/lta algorithm on synthetic data for different durations,measuring the execution time and memory usage
#steps: generate a time vector ('t') for each duration 
#add a background noise and synthetic seismic events to the time series
# measure the execution time of the STA/LTA algorithm 
#measure memory usage using psutil 
#collect results(duration, execution time and memory usage) in a list of dictionaries
def execute_scalability_test(durations, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold):
    results = [] 

    for duration in durations:
        t = np.linspace(0, duration, int(duration * samplingrate))
        np.random.seed(0)
        background_noise = np.random.normal(0, 1e-6, len(t))
        timeseries = background_noise.copy()

        # Add synthetic seismic events
        event_indices = [(2000, 2050), (2070, 2080), (2200, 2230), (2270, 2280), (2330, 2340), (2350, 2360)]
        event_frequencies = [20, 30, 40, 50, 20, 30]
        event_amplitudes = [10e-6, 15e-6, 10e-6, 15e-6, 10e-6, 15e-6]

        for (start, end), freq, amp in zip(event_indices, event_frequencies, event_amplitudes):
            start_idx = int(start * samplingrate)
            end_idx = int(end * samplingrate)
            event_time = t[start_idx:end_idx]
            timeseries[start_idx:end_idx] += amp * np.sin(2 * np.pi * freq * event_time)

        # Measure execution time and resource usage
        start_time = time.time()
        sta, lta, ratio, events = staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)
        end_time = time.time()
        execution_time = end_time - start_time

        # Capture memory usage
        process = psutil.Process() #provides an easy way to monitor system resource usage. Here, psuit measures the memory consumption of the process running the STA/LTA algorithm. 
        memory_info = process.memory_info() #understanding how memory usage scales with input size
        memory_usage = memory_info.rss / (1024 ** 2)  # in MB, used to convert memory usage from bytes to megabytes. 

        results.append({ #during execution, each result is collected in a list of dictionaries. each dictionary contains teh duration, execution time and memory usage 
            'duration': duration,
            'execution_time': execution_time,
            'memory_usage': memory_usage
        })

    return pd.DataFrame(results) #the dataframe is used to plot the results, showing how execution time and memory usage scale with duration of the time series. 

# Execute the scalability test. Results_df is a pandas.DataFrame object that provides a convenient way to store and manipulate data. It also allows you to organize the results in a structures format
results_df = execute_scalability_test(durations, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)

# Plot the scalability results, 
plt.figure(figsize=(10, 6))
plt.plot(results_df['duration'], results_df['execution_time'], marker='o', label='Execution Time')
plt.plot(results_df['duration'], results_df['memory_usage'], marker='x', label='Memory Usage (MB)')
plt.title('Scalability Testing of STA/LTA Algorithm')
plt.xlabel('Duration of Time Series (seconds)')
plt.ylabel('Metric Value')
plt.xscale('log')
plt.yscale('log')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.show()

