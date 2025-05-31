    # Library import
import numpy as np
    # Custom package import
from .KHPS2_calculation import KHPS2_calculation
from .KHPS2_plotting import KHPS2_plotting

    # Calculation and plotting return function wrapper
def run_khps2_analysis(specimen_data, initial_G, lower_bounds, upper_bounds,
                       optimization_options, denominator_epsilon, z_lim,
                       plotting_options):
    """
    Orchestrates the entire KHPS2 fracture criterion analysis pipeline.

    Performs the material parameter calibration, calculates the fracture
    locus, evaluates calibration errors, and generates a 3D visualization
    of the results. returns key analysis results.

    Function execution:
        results = run_khps2_analysis(specimen_data, initial_G, lower_bounds, upper_bounds,
                                     optimization_options, denominator_epsilon, z_lim,
                                     plotting_options)

    Function's input parameters:
        specimen_data: A dictionary containing experimental specimen data.
            Format: {specimen_name: [Fracture strain, Stress triaxiality, Normalized third invariant]}.
        initial_G: A 1D NumPy array representing the initial estimated
            material parameters [G1, G2, G3, G4, G5, G6] of the KHPS2 model.
        lower_bounds: A 1D NumPy array defining the lower bounds for
            each of the 6 material parameters (G1,... G6) during optimization.
        upper_bounds: A 1D NumPy array defining the upper bounds for
            each of the 6 material parameters (G1,... G6) during optimization.
        optimization_options: A dictionary of options to be passed to
            'scipy.optimize.least_squares' (e.g., 'ftol', 'xtol', 'max_nfev', 'verbose').
        denominator_epsilon: A small floating-point value used to prevent division
            by zero or near-zero in fracture strain calculations, ensuring numerical stability
        z_lim: A list [min_z, max_z] defining the lower and upper limits for the Z-axis 
            (Fracture strain) in figures.
        plotting_options: A dictionary containing all configurable plotting parameters.
            Expected keys are detailed in the 'KHPS2_plotting' function's docstring.

    Function's returned value:
        A dictionary containing key results from the analysis:
            - 'final_G_params': The optimized 1D NumPy array of material
              parameters [G1, G2, G3, G4, G5, G6].
            - 'total_abs_difference': The sum of the absolute values of residuals
            - 'p_calibration_error': A 1D NumPy array of percentage errors
              for each calibration point.
            - 'pt_calibration_error': The total sum of 'p_calibration_error'
              values, representing the total percentage calibration error.
            - 'ef_r' (np.array): A 1D NumPy array representing the residuals (differences)
              between measured and predicted fracture strains for each calibration point.
    """

    # Calculations using the KHPS2_calculation package function
        # Returns calibrated parameters and other datas
    (final_G_params, x_tri, y_invar, ef, tri1, invar1, ef1,
     tri_k, invar_k, ef_k, ef_r, total_abs_difference, p_calibration_error,
     pt_calibration_error, tri_c) = \
        KHPS2_calculation(specimen_data, initial_G, lower_bounds, upper_bounds,
                          optimization_options, denominator_epsilon, z_lim)

    # Plot generation using the KHPS2_plotting package function
        # Displays the plot
    KHPS2_plotting(x_tri, y_invar, ef, tri1, invar1, ef1,
                   tri_k, invar_k, ef_k, specimen_data, plotting_options, tri_c)

    # Return relevant results
    return {
        'final_G_params': final_G_params,                   # Calibrated material parameters
        'total_abs_difference': total_abs_difference,       # Total calibration error (Sum of calibration errors)
        'p_calibration_error': p_calibration_error,         # Calibration error in percentages for each specimen
        'pt_calibration_error': pt_calibration_error,       # Total (Sum) calibration error in percentages
        'ef_r': ef_r}                                       # Calibration error - difference between calibration points and the calibrated locus