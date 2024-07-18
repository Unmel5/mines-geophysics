def load_psd_image(image_path):
    image = Image.open(image_path)
    image_rgb = image.convert("RGB")  # Convert to RGB to ensure 3 channels
    image_array = np.array(image_rgb)
    return image_array

# This code loads an image from a specified file path, converts it to RGB to ensure it has three channels, and then converts it to NumPy
image_path = "/Users/melisaunlu/velocity_UTC-YMD20220607-HMS230923.213_seq_00000001848_246-248sec.png"
image_array = load_psd_image(image_path)

# Display the original image
# Purpose: This code visualizes the loaded image to verify that it has been correctly loaded and converted to RGB format 
plt.figure(figsize=(10, 6))
plt.imshow(image_array)
plt.title("Original Seismic Data")
plt.axis('off')
plt.show()

# Load the autoencoder model
model_path = "/Users/melisaunlu/model_256.h5"
model = load_model(model_path)

# Preprocess the image for the autoencoder model
image_resized = Image.fromarray(image_array).resize((256, 256))  # Resize the image to match model input
image_array = np.array(image_resized) / 255.0  # Normalize the image
image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

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
