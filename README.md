# Seismic STA/LTA and Autoencoder Testing and Scalability

This repository contains Python scripts for STA/LTA using DASCore and applying an autoencoder for seismic event detection. These scripts show how to do these analyses, add several unit tests, and carry out serial scalability testing. The scripts include loading and preprocessing seismic data, carrying out event detection (either using STA/LTA or using a pre-trained autoencoder to detect anomalies), visualizing original and reconstructed spectra (a key step to understand the use of the autoencoder), and performing scalability testing to time the STA/LTA and the autoencoder.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Version Control](#version-control)
4. [Testing](#testing)
5. [License](#license)
6. [Contact](#contact)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Unmel5/mines-geophysics.git
    cd mines-geophysics
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
## STA/LTA Code Use

**Melissa, please add directions similar to the directions below for the autoencoder showing how to run the unit tests and the timing/scalability tests for the STA/LTA method**

## Autoencoder Code Use

To load and preprocess seismic DAS data, apply the autoencoder to seismic data, visualize the original and reconstructed spectra, and perform scalability testing on the autoencoder:

```python
from src.data_processing import load_psd_image
from src.autoencoder import apply_autoencoder_to_data
from src.visualization import visualize_spectra
from src.scalability_test import execute_scalability_test, plot_scalability_test_results

# Load and preprocess seismic images
image_path = "path/to/your/image.png"
image_array = load_psd_image(image_path)

# Apply the autoencoder to seismic data
image_paths = ["path/to/your/image.png"]
autoencoder_path = "path/to/your/autoencoder.h5"
original_images, reconstructed_images = apply_autoencoder_to_data(autoencoder_path, image_paths)

# Visualize the original and reconstructed spectra
visualize_spectra(original_images[0], reconstructed_images[0])

# Perform scalability testing on the autoencoder
# Example parameters
durations = [30, 60, 90]  # Example durations
samplingrate = 200.0
stawindowduration = 0.1
ltawindowduration = 0.5
stepsizeduration = 0.01
detection_threshold = 1.5

results_df = execute_scalability_test(durations, samplingrate, stawindowduration, ltawindowduration, stepsizeduration, detection_threshold)
plot_scalability_test_results(results_df)

## Notes on Use of Version Control
1. Initialize Git:
  git init
2. Add files to the repository:
  git add.
3. Commit the changes:
  git commit -m "Initial commit"

##Testing - QUESTION: Isn't the unit testing all focused on the STA/LTA part of the code? Consider moving this up.
python -m unittest discover -s tests

