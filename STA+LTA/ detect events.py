import dascore as dc
import numpy as np
import matplotlib.pyplot as plt
from dascore.utils.downloader import fetch

# Define STA/LTA related functions
def compute_sta(timeseries, samplingrate, stawindowduration):
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
    ratio = np.ones_like(stavalues)
    ratio[ltavalues > 0] = stavalues[ltavalues > 0] / ltavalues[ltavalues > 0]
    return ratio

def detect_events(ratio, detection_threshold, samplingrate):
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

def staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, detection_threshold):
    stavalues = compute_sta(timeseries, samplingrate, stawindowduration)
    ltavalues = compute_lta(timeseries, samplingrate, ltawindowduration)
    ratio = compute_ratio(stavalues, ltavalues)
    events = detect_events(ratio, detection_threshold, samplingrate)
    return stavalues, ltavalues, ratio, events

# Download and prepare the data
directory_path = fetch('example_dasdae_event_1.h5').parent
spool = dc.spool(directory_path)

# Extract first patch in the spool.
patch = spool[0]

# Iterate patches in spool.
for patch in spool:
    ...

# Check if the spool is empty
if len(spool) == 0:
    print("No patches found in the spool.")
else:
    # Load the first patch of data
    patch = next(iter(spool))
    print("Patch loaded:", patch)

    # Print patch details
    print("Patch Details:")
    print(f"Dimensions: {patch.dims}")
    print(f"Coordinates: {patch.coords}")
    print(f"Attributes: {patch.attrs}")

    # Decimate, detrend, and filter the patch
    out = (
        patch.decimate(time=8)
        .detrend(dim='distance')
        .pass_filter(time=(0.1, 10))  # Adjusted filter bounds
    )

    # Use a single channel from the patch data for STA/LTA
    timeseries = out.data[:, 0]  # Assuming the first channel for simplicity
    time = out.coords.get_array('time')

    # Convert time to seconds for sampling rate calculation
    time_seconds = (time - time[0]).astype('timedelta64[ns]').astype(float) * 1e-9
    samplingrate = 1 / np.median(np.diff(time_seconds))

    # Parameters for STA/LTA
    samplingrate = 200
    stawindowduration = 0.05  # 30 ms window for STA
    ltawindowduration = 1.0   # 2 seconds window for LTA
    detection_threshold = 2.0  # Detection threshold

    # Run the STA/LTA trigger
    sta, lta, ratio, events = staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, detection_threshold)

    # Print STA, LTA, and ratio values for debugging
    print("STA values (first 10):", sta[:10])
    print("LTA values (first 10):", lta[:10])
    print("Ratio values (first 10):", ratio[:10])
    print("Detected events:", events)

    # Adjust lengths of the time arrays
    ltawindowlength = int(ltawindowduration * samplingrate)
    time_stalta = time_seconds[ltawindowlength:ltawindowlength + len(ratio)]

    # Ensure the lengths match for plotting
    min_length = min(len(time_stalta), len(sta), len(lta), len(ratio))
    time_stalta = time_stalta[:min_length]
    sta = sta[:min_length]
    lta = lta[:min_length]
    ratio = ratio[:min_length]

    # Plot the results
    plt.figure(figsize=(14, 12))

    # Plot the original timeseries
    plt.subplot(4, 1, 1)
    plt.plot(time_seconds[:len(timeseries)], timeseries[:len(time_seconds)], label='Original Time Series', color='blue', linewidth=0.5)
    plt.title('Original Time Series')
    plt.xlabel('Time (sec)')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    # Plot STA and LTA values
    plt.subplot(4, 1, 2)
    plt.plot(time_stalta, sta, label='STA', color='orange', linewidth=0.5)
    plt.plot(time_stalta, lta, label='LTA', color='green', linewidth=0.5)
    plt.title('STA and LTA Values')
    plt.xlabel('Time (sec)')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    # Plot STA/LTA ratio and detected events
    plt.subplot(4, 1, 3)
    plt.plot(time_stalta, ratio, label='STA/LTA Ratio', color='purple', linewidth=0.5)
    plt.axhline(y=detection_threshold, color='red', linestyle='--', linewidth=2)  # Add detection threshold line
    plt.title('STA/LTA Ratio and Detected Events')
    plt.xlabel('Time (sec)')
    plt.ylabel('STA/LTA Ratio')
    if len(ratio) > 0:
        plt.ylim(0, max(3, np.max(ratio)))
    else:
        plt.ylim(0, 3)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    # Mark detected events
    for i, event in enumerate(events):
        event_start_time = time_stalta[event[0]]
        event_end_time = time_stalta[event[1]]
        plt.axvspan(event_start_time, event_end_time, color='green', alpha=0.3, label=f'Event {i+1}' if i == 0 else "")

        event_duration = event_end_time - event_start_time
        print(f"Event {i+1}: Start Time = {event_start_time:.2f} sec, End Time = {event_end_time:.2f} sec, Duration = {event_duration:.2f} sec")

    plt.show()

    print("Detected events:", events)
