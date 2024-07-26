import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter
from PIL import Image

# Function to read HDF5 file
def read_hdf5_file(file_path):
    with h5py.File(file_path, 'r') as f:
        print("Reading data from HDF5 file...")
        data = f['velocity/data'][:]  # Use 'velocity/data' as the dataset name
        print("Data successfully read from HDF5 file.")
    return data

# Function to extract and save the amplitude spectrum for time window 1 using FFT
def extract_amplitude_spectrum_for_time_window(data, window_index=0, max_samples=50, sampling_rate=100, start_channel=100, end_channel=375):
    print(f"Extracting amplitude spectrum for time window {window_index + 1}...")
    time_windows = np.array_split(data, 3, axis=1)  # Assuming 3 time windows for simplicity
    
    if window_index >= len(time_windows):
        print(f"Time window {window_index + 1} is out of range.")
        return
    
    window = time_windows[window_index]
    
    # Reduce the size of the data for FFT computation
    if window.shape[0] > max_samples:
        print(f"Reducing data size to {max_samples} samples for FFT computation...")
        window = window[:max_samples, :]
    
    # Extract the specified channel range
    if end_channel >= window.shape[1]:
        end_channel = window.shape[1] - 1
    
    window = window[:, start_channel:end_channel+1]

    print("Computing FFT...")
    # Compute FFT for the specified time window
    try:
        spect = np.fft.fft(window, axis=0)
        nFrqBins = int(spect.shape[0] / 2)  # number of frequency bins 
        amplitudeSpec = np.abs(spect[:nFrqBins, :])
        print("FFT computation complete.")
    except Exception as e:
        print(f"Error during FFT computation: {e}")
        return
    
    # Normalize the amplitude spectrum to the range [0, 1] using robust normalization
    vmin, vmax = np.percentile(amplitudeSpec, [1, 99])
    print(f"vmin: {vmin}, vmax: {vmax}")
    amplitudeSpec = np.clip((amplitudeSpec - vmin) / (vmax - vmin), 0, 1)
    
    # Flip the amplitude spectrum vertically
    amplitudeSpec = np.flipud(amplitudeSpec)
    
    # Create time and frequency arrays
    channels = np.arange(start_channel, end_channel + 1)
    frequencies = np.linspace(0, sampling_rate / 2, nFrqBins)  # Properly scaled frequency array
    
    # Plot and save the amplitude spectrum for the specified time window
    plt.figure(figsize=(12, 10))
    plt.pcolormesh(channels, frequencies, amplitudeSpec, shading='gouraud', cmap='viridis')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Channels')
    plt.title(f'Amplitude Spectrum for Time Window {window_index + 1}')
    plt.colorbar(label='Amplitude')
    plt.xticks(ticks=np.linspace(start_channel, end_channel, 6), labels=np.linspace(start_channel, end_channel, 6).astype(int))
    plt.savefig(f'time_window_{window_index + 1}_amplitude_spectrum.png')
    plt.show()
    print(f"Amplitude spectrum for time window {window_index + 1} saved as 'time_window_{window_index + 1}_amplitude_spectrum.png'.")

# Function to calculate strain rate from velocity data
def calculate_strain_rate(velocity_data, gauge_length, distance_step):
    print("Calculating strain rate from velocity data...")
    gauge_samples = int(round(gauge_length / distance_step))
    strain_rate = (velocity_data[:, gauge_samples:] - velocity_data[:, :-gauge_samples]) / gauge_length
    print("Strain rate calculation complete.")
    return strain_rate

# Set parameters for preprocessing the data
distance_step = 0.1  # Example value, adjust as necessary
gauge_length = distance_step * 2
start_channel = 100
end_channel = 375
min_freq = 0
sampling_rate = 100  # Example value, adjust as necessary
max_freq = 0.9 * 0.5 * sampling_rate
time_window = 2  # sec
time_overlap = 1  # sec

# Define the path to the local HDF5 file and the image
file_path = os.path.expanduser('/Users/melisaunlu/data/velocity_UTC-YMD20220529-HMS220021.198_seq_00000006116.hdf5')

# Read the data from the HDF5 file
data = read_hdf5_file(file_path)

# Calculate strain rate from velocity data
strain_rate_data = calculate_strain_rate(data, gauge_length, distance_step)

# Extract and save the amplitude spectrum for time window 1
extract_amplitude_spectrum_for_time_window(strain_rate_data, window_index=0, sampling_rate=sampling_rate, start_channel=start_channel, end_channel=end_channel)
