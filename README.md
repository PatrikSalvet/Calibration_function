# KHPS2 Ductile Fracture Criterion Calibration and Visualization

This repository provides a Python-based tool for calibrating material parameters for the **KHPS2 ductile fracture criterion** and visualizing the resulting 3D fracture locus. It leverages experimentaly measured or numerically simulated data (fracture strain, stress triaxiality, and normalized third invariant) to calibrate the six unknown material parameters of the mathematical KHPS2 model and generates a comprehensive representation of the material's fracture behavior.

## Table of Contents

  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Running the analysis](#running-the-analysis)
    - [Input Parameters](#input-parameters)
    - [Output Results](#output-results)
  - [Project Structure](#project-structure)
  - [Mathematical Formulation of KHPS2](#mathematical-formulation-of-khps2)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Introduction

The KHPS2 ductile fracture criterion is a material model used to predict the initiation of fracture in ductile materials under various stress states. This project offers a robust and easy-to-use framework to:

1.  **Calibrate** the six material parameters ($G_1$ to $G_6$) of the KHPS2 model using experimental data.
2.  **Calculate** the 3D fracture locus surface and the plane stress curve.
3.  **Evaluate** the calibration error against experimental data.
4.  **Visualize** the calibrated fracture locus and experimental points in an interactive 3D plot.

## Features

* **Parameter Calibration:** Employs `scipy.optimize.least_squares` for efficient and accurate optimization of KHPS2 material parameters.
* **3D Fracture Locus Generation:** Calculates and visualizes the complex 3D fracture surface defined by the KHPS2 criterion.
* **Plane Stress Curve:** Generates and plots the plane stress fracture curve as a subset of the 3D locus.
* **Calibration Error Analysis:** Provides detailed metrics on the accuracy of the calibrated model, including individual and total percentage calibration errors.
* **Customizable Plotting:** Offers various options to tailor the appearance of the 3D fracture locus plot, including markers, colors, and line styles.
* **Modular Design:** Cleanly separated functions for calculations, optimization, and plotting, promoting maintainability and extensibility.

## Installation

To get started with this project, clone the repository and install the necessary dependencies:
```bash
git clone https://github.com/PatrikSalvet/Calibration_function.git
cd your-repository-name
pip install -r requirements.txt
```
## Usage
The primary way to interact with this project is through the `Main_Run_Function.ipynb` in Jupyter Notebook. It provides a guided workflow for setting up inputs, running the analysis, and visualizing results.

### Running the analysis
1. Open the `Main_Run_Function.ipynb` script in Jupyter Notebook.
2. Specify `INPUTS` and `CONFIGURATION` sections within the notebook.
   * `INPUTS`: Define `specimen_data`, `initial_G` parameters, and set `lower_bounds` and `upper_bounds` for the optimization.
   * `CONFIGURATION`: Adjust parameters for the optimization process (`optimization_options`) and customize the appearance of the plots (`figure_settings`, `surface_setting`, etc.).
3. Execute the cells within the notebook once the inputs and configurations are set.
   * The notebook will perform the parameter calibration, calculate the fracture locus, evaluate calibration errors, and generate a 3D plot.
   * A summary of the calibrated material parameters and calibration errors will be printed in the output.

### Input Parameters
All input parameters and configuration settings are defined within the `Main_Run_Function.ipynb` notebook. Users can modify these values directly to suit their specific experimental data and visualization preferences.

#### Input Section
* `specimen_data` (dict): Defines the experimental approximation points.
  * **Format:** `{specimen_name: [Fracture strain, Stress triaxiality, Normalized third invariant]}`
* `initial_G` (numpy.ndarray): A 1D NumPy array representing the initial estimated material parameters $[G_1, G_2, G_3, G_4, G_5, G_6]$ of the KHPS2 model. These values serve as the starting point for the optimization algorithm.
* `lower_bounds` (numpy.ndarray): A 1D NumPy array specifying the lower boundaries for each of the 6 material parameters during the optimization process. Ensures that the calibrated parameters stay within a realistic range.
* `upper_bounds` (numpy.ndarray): A 1D NumPy array specifying the upper boundaries for each of the 6 material parameters during the optimization process.

#### Configuration Section
* `optimization_options` (dict): Contains parameters for the `scipy.optimize.least_squares` function, controlling the optimization behavior.
  * `ftol` (float): Tolerance for the change in the sum of squares of residuals.
  * `xtol` (float): Tolerance for the change in the optimization variables (G parameters).
  * `max_nfev` (int): Maximum number of function evaluations.
  * `verbose` (int): Level of verbosity for the optimizer's output (0: silent, 1: final report, 2: each iteration). It is recommended to set this to 0 when running the full notebook for clean output
* `denominator_epsilon` (float): A small numerical constant (e.g., 1e-6) used to prevent division by zero or near-zero in the mathematical calculations of fracture strain.
* **Figure Settings:** A collection of variables defining the general properties of the 3D plot.
  * `figure_size`(tuple): Dimensions (width, height) of the plot figure.
  * `view_elev` (int/float): Vertical rotation angle (elevation) for the 3D view.
  * `view_azim` (int/float): Horizontal rotation angle (azimuth) for the 3D view.
  * `x_lim`, `y_lim`, `z_lim` (lists): Axis limits for stress triaxiality, normalized third invariant, and fracture strain, respectively. Each is a list `[min_value, max_value]`.
  * `x_label`, `y_label`, `z_label`, `plot_title` (str): Text labels for the X, Y, Z axes, and the plot title.
  * `labelpad_x`, `labelpad_y`, `labelpad_z` (int/float): Padding (space) between axis labels and the axis itself.
  * `title_y_position` (int/float): Vertical position of the plot title relative to the top of the axes.
  * `label_font_size` (int): Font size for axis labels.
  * `title_font_size` (int): Font size for the plot title.
* **Main Surface Setting:** Defines the appearance of the 3D fracture locus surface.
  * `surface_alpha` (float): Defineds transparency of the main surface.
  * `surface_rgb_color` (numpy.ndarray): RGB color values for the main surface.
* **Plane Stress Curve Setting:** Controls the appearance of the plane stress fracture curve.
  * `plot_plane_stress_curve` (bool): True to display the plane stress curve, False otherwise.
  * `plane_stress_line_color` (str): Color of the plane stress curve.
  * `plane_stress_line_width` (int/float): Line width of the plane stress curve.
* **Constant Invariant Curve Setting:** Controls the appearance of additional curves at constant third invariant values.
  * `plot_constant_invariant_curves` (bool): True to display, False otherwise.
  * `constant_invariant_line_color` (str): Color of the constant invariant curves.
  * `constant_invariant_line_width` (int/float): Line width of the constant invariant curves.
* **Approximated Point Setting:** Defines how the experimental data points are displayed on the plot.
  * `plot_approximated_points` (bool): True to display the experimental data points, False otherwise.
  * `marker_styles` (list): A list of Matplotlib marker style strings (e.g., 'o', 's', 'd') to be used for each specimen.
  * `marker_size_area` (int/float): The area of the marker in points squared.
  * `marker_face_colors` (list): A list of RGB color arrays for the face color of each marker.
  * `marker_edge_color` (str): Color of the marker edges.
  * `marker_edge_linewidth` (int/float): Line width of the marker edges.
* **Cut-off Plane Setting:** Defines the visualization of the fracture locus cut-off plane.
  * `plot_cut_off_plane` (bool): True to display the cut-off plane, False otherwise.
  * `cut_off_plane_color` (numpy.ndarray): RGB color values for the cut-off plane.
  * `cut_off_plane_alpha` (float): Transparency of the cut-off plane.

### Output Results
After execution, the notebook will display a summary of the analysis results in the output cells, including:
  * **Calibrated material parameters ($G_1$ to $G_6$):** The optimized values found by the least-squares method.
  * **Fracture strain difference ($e_{f,r}$):** A NumPy array showing the residual error between the measured fracture strain and the fracture strain predicted by the calibrated model for each specimen.
  * **Percentage calibration errors for each specimen:** The individual percentage difference for each experimental data point, calculated as $|(\epsilon_{f,measured} - \epsilon_{f,predicted}) / \epsilon_{f,measured}| \times 100%$.
  * **Total percentage error:** The sum of all individual percentage errors, providing an overall measure of the model's fit.
  * **A 3D visualization** of the calibrated KHPS2 fracture locus, overlaid with experimental points, plane stress curve, and constant invariant curves, as configured in the `plotting_options`.

## Project Structure
```.
├── package/
│   ├── __init__.py
│   ├── KHPS2_calculation.py
│   ├── KHPS2_function.py
│   ├── KHPS2_plotting.py
│   ├── Main_workflow.py
│   └── Locus_calculation.py
└── Main_Run_Function.ipynb
```

* `package/`: This contains the core Python modules.
  * `KHPS2_calculation.py`: Orchestrates the overall KHPS2 calculation and optimization pipeline, calling other functions as needed.
  * `KHPS2_function.py`: Defines the residual function for the KHPS2 criterion, used by the optimization algorithm.
  * `KHPS2_plotting.py`: Handles the 3D visualization of the fracture locus and experimental data.
  * `Locus_calculation.py`: Implements the mathematical formulas for calculating the cut-off stress triaxiality and fracture strain based on the KHPS2 criterion.
  * `Main_workflow.py`: Contains the `run_khps2_analysis` function which acts as a wrapper to execute the entire analysis pipeline, integrating calculations and plotting.
* `Main_Run_Function.ipynb`:  The central control script for the entire analysis workflow. This Jupyter Notebook defines all input parameters and configuration settings, orchestrates the execution of the calibration and plotting functions from the package, and displays the final results.
Call help() for more detailed information on any of the functions.

## Mathematical Formulation of KHPS2
The KHPS2 ductile fracture criterion is defined by the following equation for the equivalent plastic strain at fracture ($\epsilon_f$):

$$
\epsilon_f = G_1 e^{-G_2 \eta} \left( \frac{1}{2} + \frac{1}{2} \cos\left(\frac{\pi I_3^*}{G_3}\right) \right) + G_4 \eta + G_5 I_3^* + G_6

$$where:

$\eta$ is the stress triaxiality.
$I_3^*$ is the normalized third invariant of the deviatoric stress.
$G_1, G_2, G_3, G_4, G_5, G_6$ are the material-dependent parameters that are calibrated by this tool.

A cut-off stress triaxiality ($\eta_c$) is also part of the criterion, defining a lower bound for triaxiality below which fracture may not be predicted or is not of interest:

$$\eta_c = -\left( G_3 + \frac{G_1 - G_3}{2} - G_2 \right) (I_3^*)^2 - \left( \frac{G_1 - G_3}{2} \right) I_3^* - G_2
$$When $\eta &lt; \eta_c$, the material is considered to be in a stress state where fracture is less likely or not predicted by this criterion. Fracture strain values in this region are typically masked or set to NaN for visualization purposes.


![KHPS2 Fracture Locus and Calibration Points](my_output_image.png)
![Widget image03](test_files/Images_Readme/Widget_GUI_Example_3.png "Widget result image 2")

## References
Refer to the following papers for more information and use case about the material calibration and the KHPS2 ductile fracture criterion.
[Research Paper](Projects_use_case_papers/Projects_use_case_1.pdf)
[Diploma thesis](Projects_use_case_papers/Projects_use_case_2.pdf)

