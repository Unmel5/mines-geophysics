
# Generate synthetic seismic data
samplingrate = 100.0
duration = 10  # seconds
num_samples = int(duration * samplingrate)  # Ensure this is an integer
t = np.linspace(0, duration, num_samples)  # Time vector

# Function to generate step function values
def stepfunction(timeseries): #timeseries: an array representing the time points or the input signal data
    return np.where(timeseries > 5, 2, 1) #outputting 2 for tiimes greater than 5 seconds and 1 otherwise

# Generate background noise
np.random.seed(0)  
background_noise = np.random.normal(0, 1e-6, num_samples)  #normally distributed noise added to timeseries to simulate random seismic background activity
step_values = stepfunction(t)
timeseries = background_noise + step_values #combination of background noise and step function values 

# Plot the step function
plt.figure(figsize=(10, 6)) 
plt.plot(t, step_values, label='Step Function', drawstyle='steps-post') 
plt.title('Step Function') 
plt.xlabel('Time [s]') 
plt.ylabel('Amplitude') 
plt.ylim(-0.1, 3.3) 
plt.grid(True) 
plt.legend()
plt.show()

# Parameters for STA/LTA
stawindowduration = 0.03
ltawindowduration = 0.1
stepsizeduration = 0.01
detection_threshold = 2.0

# Compute STA/LTA and detect events based on the ratio exceeding the threshold 
sta, lta, ratio, events = staltatrigger(timeseries, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)

# Plot the timeseries and detected events
plt.figure(figsize=(10, 6))
plt.plot(t, timeseries, label='Timeseries')
for start, end in events:
    plt.axvspan(t[start], t[end], color='red', alpha=0.3, label='Detected Event' if start == events[0][0] else "")
plt.title('Synthetic Seismic Data with Detected Events')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()
