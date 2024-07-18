# Function to visualize the spectrogram for the second time window
def visualize_spectra_for_second_window(data, num_windows=3):
    """
    Visualize the frequency content of the signal over time by computing and visualizing the spectrogram for the second time window.
    Args:
    - data: NumPy array of the data
    - num_windows: number of time windows to split the data into
    """
    time_windows = np.array_split(data, num_windows, axis=1)
    
    # Select the second time window (index 1)
    if len(time_windows) > 1:
        second_window = time_windows[1]
    else:
        print("Not enough time windows to select the second one.")
        return

    # Compute spectrogram for the second time window
    f, t, Sxx = spectrogram(second_window.flatten(), fs=1.0)
    Sxx = 10 * np.log10(Sxx + np.finfo(float).eps)

    # Plot the spectrogram for the second time window
    plt.figure(figsize=(12, 10))
    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram for Time Window 2')
    plt.colorbar(label='Intensity [dB]')
    plt.show()

# Visualize the spectrogram for the second time window of the original image
print("Visualizing spectrogram for time window 2 of original image 1...")
visualize_spectra_for_second_window(image_array[0], num_windows=3)

# Visualize the spectrogram for the second time window of the reconstructed image
print("Visualizing spectrogram for time window 2 of reconstructed image 1...")
visualize_spectra_for_second_window(reconstructed[0, :, :, 0], num_windows=3)

