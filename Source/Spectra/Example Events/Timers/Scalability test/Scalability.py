# Load and preprocess images to be compatible with the autoencoder
def load_psd_image(image_path):
    image = Image.open(image_path)
    image_rgb = image.convert("RGB")
    image_array = np.array(image_rgb)
    return image_array

# Load an image from a specified file path
image_path = "/Users/melisaunlu/velocity_UTC-YMD20220607-HMS230923.213_seq_00000001848_246-248sec.png"
image_array = load_psd_image(image_path)

# Display the original image
plt.figure(figsize=(10, 6))
plt.imshow(image_array)
plt.title("Original Seismic Data")
plt.axis('off')
plt.show()

# Load the autoencoder model
autoencoder_path = "/Users/melisaunlu/model_256.h5"
model = load_model(autoencoder_path)

# Preprocess the image for the autoencoder model
image_resized = Image.fromarray(image_array).resize((256, 256))
image_array = np.array(image_resized) / 255.0
image_array = np.expand_dims(image_array, axis=0)

# Reconstruct the spectra using the autoencoder model
reconstructed = model.predict(image_array)

# Scale the reconstructed spectra to the range [0, 255] and cast to uint8
reconstructed_scaled = (reconstructed[0, :, :, 0] * 255).astype(np.uint8)

# Visualize the reconstructed spectra
plt.figure(figsize=(10, 6))
plt.imshow(reconstructed_scaled, aspect='auto', cmap='jet')
plt.title("Reconstructed AE Spectra")
plt.colorbar()
plt.axis('off')
plt.show()

# Function to visualize the spectrogram for the second time window
def visualize_spectra_for_second_window(data, num_windows=3):
    time_windows = np.array_split(data, num_windows, axis=1)
    if len(time_windows) > 1:
        second_window = time_windows[1]
    else:
        print("Not enough time windows to select the second one.")
        return

    f, t, Sxx = spectrogram(second_window.flatten(), fs=1.0)
    Sxx = 10 * np.log10(Sxx + np.finfo(float).eps)
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

# Function to plot significant events in the data
def visualize_example_events(data, num_events=5):
    event_indices = np.linspace(0, data.shape[1] - 1, num_events, dtype=int)
    plt.figure(figsize=(12, 6))
    for i, idx in enumerate(event_indices):
        plt.subplot(num_events, 1, i + 1)
        plt.plot(data[:, idx])
        plt.title(f'Event at Index {idx}')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.show()

def apply_autoencoder_to_data(autoencoder_path, image_paths):
    start_time = time.time()
    load_data_time = time.time()
    images = [load_psd_image(path) for path in image_paths]
    images = np.stack(images, axis=0)
    load_data_time = time.time() - load_data_time

    load_model_time = time.time()
    autoencoder = load_model(autoencoder_path)
    load_model_time = time.time() - load_model_time

    ae_application_time = time.time()
    reconstructed_images = autoencoder.predict(images)
    ae_application_time = time.time() - ae_application_time

    total_time = time.time() - start_time

    print(f"Time to load and process images: {load_data_time:.2f} seconds")
    print(f"Time to load autoencoder: {load_model_time:.2f} seconds")
    print(f"Time to apply autoencoder: {ae_application_time:.2f} seconds")
    print(f"Total time: {total_time:.2f} seconds")

    return images, reconstructed_images, load_data_time, load_model_time, ae_application_time, total_time

#this is evaluating how well a system (the autoencoder model) handles increasing amounts of work, such as larger image sizes or greater number of images 
#define image sizes and number of images
#load base image and resize it to different target sizes
#iterate over image sizes and numbers: for each combination of image size and number of images, 
    #resize image 
    #create image array: an array of the resized images is created, repeating the resized image the specified number of times
    #apply autoencoder to the image array
    #measure and record times taken for loading and processing the images, loading th emodel and applyign the autoencoder 

# Function to perform scalability testing and plot the results
def scalability_testing(autoencoder_path, base_image_path, image_sizes, num_images_list):
    base_image = load_psd_image(base_image_path)
    results = []

    for target_size in image_sizes:
        resized_image = Image.fromarray(base_image).resize(target_size)
        resized_image_array = np.array(resized_image) / 255.0
        resized_image_array = np.expand_dims(resized_image_array, axis=0)
        for num_images in num_images_list:
            image_arrays = np.vstack([resized_image_array] * num_images)
            print(f"\nTesting with image size: {target_size}, Number of images: {num_images}")
            _, _, load_data_time, load_model_time, ae_application_time, total_time = apply_autoencoder_to_data(autoencoder_path, [base_image_path] * num_images)
            results.append((target_size, num_images, load_data_time, load_model_time, ae_application_time, total_time))
    
    return results

# Perform scalability testing
image_sizes = [(256, 256), (512, 512), (1024, 1024)]  # Different image sizes for testing
num_images_list = [1, 10, 50, 100]  # Different numbers of images for testing
results = scalability_testing(autoencoder_path, image_path, image_sizes, num_images_list)

# Plot the scalability test results
def plot_scalability_test_results(results):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Scalability Test Results')

    for target_size, num_images, load_data_time, load_model_time, ae_application_time, total_time in results:
        axs[0, 0].scatter(num_images, load_data_time, label=f'Size: {target_size}', s=50)
        axs[0, 1].scatter(num_images, load_model_time, label=f'Size: {target_size}', s=50)
        axs[1, 0].scatter(num_images, ae_application_time, label=f'Size: {target_size}', s=50)
        axs[1, 1].scatter(num_images, total_time, label=f'Size: {target_size}', s=50)
    
    axs[0, 0].set_title('Load Data Time')
    axs[0, 1].set_title('Load Model Time')
    axs[1, 0].set_title('Autoencoder Application Time')
    axs[1, 1].set_title('Total Time')

    for ax in axs.flat:
        ax.set_xlabel('Number of Images')
        ax.set_ylabel('Time (seconds)')
        ax.legend()

    plt.tight_layout()
    plt.show()

plot_scalability_test_results(results)
