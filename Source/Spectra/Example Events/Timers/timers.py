def apply_autoencoder_to_data(autoencoder_path, image_paths):
    """
    Manage the entire process of loading the autoencoder model, applying it to data, and measuring the execution time for each step.
    Args:
    - autoencoder_path: path to the autoencoder model file
    - image_paths: list of paths to image files
    Returns:
    - Original images and reconstructed images as NumPy arrays
    """
    start_time = time.time()
    # Adding timers into code 
    # Load and preprocess PSD images
    load_data_time = time.time()
    images = [load_psd_image(path) for path in image_paths]
    images = np.stack(images, axis=0)
    load_data_time = time.time() - load_data_time

    # Load the pre-trained autoencoder
    load_model_time = time.time()
    autoencoder = load_model(autoencoder_path)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    load_model_time = time.time() - load_model_time

    # Apply the autoencoder
    ae_application_time = time.time()
    reconstructed_images = autoencoder.predict(images)  # Use predict method directly
    ae_application_time = time.time() - ae_application_time

    # Total time
    total_time = time.time() - start_time

    # Print timing information for each step
    print(f"Time to load and process images: {load_data_time:.2f} seconds")
    print(f"Time to load and compile autoencoder: {load_model_time:.2f} seconds")
    print(f"Time to apply autoencoder: {ae_application_time:.2f} seconds")
    print(f"Total time: {total_time:.2f} seconds")

    return images, reconstructed_images


# Example usage
image_paths = [
    "/Users/melisaunlu/velocity_UTC-YMD20220607-HMS230923.213_seq_00000001848_246-248sec.png"
]
autoencoder_path = "/Users/melisaunlu/model_256.h5"

# Apply the autoencoder to the PSD images
original_images, reconstructed_images = apply_autoencoder_to_data(autoencoder_path, image_paths)

