#Seismic Autoencoder 
Python scripts for STA/LTA testing from dascore and implementing an autoencoder for seismic analysis and scalability testing. 
Autoencoder 
  Loading and preprocessing seismic images 
  Using a pre-trained autoencoder to reconstruct images 
  Visualizing original and reconstructed spectra 
  performing scalability testing on the autoencoder 

installation
1. clone the repository
2. cd mines-geophysics 
3. pip install -r requirements.txt

#usage: loading and preprocessing images 
from src.data_processing import load_psd_image
image_path = "path/to/your/image.png"
image_array = load_psd_image(image_path)

#using the autoencoder 
from src.autoencoder import apply_autoencoder_to_data
image_paths = ["path/to/your/image.png"]
autoencoder_path = "path/to/your/autoencoder.h5"
original_images, reconstructed_images = apply_autoencoder_to_data(autoencoder_path, image_paths)

visualizing spectra 
from src.visualization import visualize_spectra
visualize_spectra(original_images[0], reconstructed_images[0])

scalability testing 
from src.scalability_test import execute_scalability_test, plot_scalability_test_results
results_df = execute_scalability_test(durations, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)
plot_scalability_test_results(results_df)

version control 
git init 
git add . 
git commit -m "Initial commit" 

#testing 
python -m unittest discover -s tests


