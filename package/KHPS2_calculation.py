    # Standard library import
import numpy as np
from scipy.optimize import least_squares

    # Custom package import
from .KHPS2_function import KHPS2_function
from .Locus_calculation import locus_calculation

    # KHPS2 calculation function
def KHPS2_calculation(specimen_data, initial_G, lower_bounds, upper_bounds,
                      optimization_options, denominator_epsilon, z_lim):
    """
    Performs the full KHPS2 fracture criterion calculation and optimization pipeline.

    This function orchestrates the material parameter calibration using least squares
    optimization, calculates the 3D fracture locus surface, plane stress curve,
    and assesses the calibration error against experimental specimen data.

    Function execution:
        KHPS2_calculation(specimen_data, initial_G, lower_bounds, upper_bounds,
                        optimization_options, denominator_epsilon, z_lim):

    Function's input args:
        specimen_data: A dictionary containing experimental specimen data.
            Format: {specimen_name: [Fracture strain, Stress triaxiality, Normalized third invariant]}.
        initial_G: A 1D NumPy array representing the initial estimated
            material parameters [G1, G2, G3, G4, G5, G6] of the KHPS2 model.
        lower_bounds: A 1D NumPy array defining the lower bounds for
            each of the 6 material parameters (G1,... G6) during optimization.
        upper_bounds: A 1D NumPy array defining the upper bounds for
            each of the 6  (G1,... G6) material parameters during optimization.
        optimization_options: A dictionary of options to be passed to
            'scipy.optimize.least_squares' (e.g., 'ftol', 'xtol', 'max_nfev', 'verbose').
        denominator_epsilon: A small floating-point value used to prevent
            division by zero or near-zero in fracture strain calculations, ensuring
            numerical stability.
        z_lim: A list [min_z, max_z] defining the lower and upper limits
            for the Z-axis (Fracture strain) in figures. The 'max_z' value is
            also used to clip calculated fracture strain values.

    Function's return args:
        A tuple containing the following results:
            - final_G_params: A 1D NumPy array of calibrated material parameters
              [G1, G2, G3, G4, G5, G6].
            - x_tri: A 2D NumPy array (meshgrid) representing stress triaxiality
              values for the main locus surface.
            - y_invar: A 2D NumPy array (meshgrid) representing normalized third
              invariant values for the main locus surface.
            - ef: A 2D NumPy array of calculated fracture strain values corresponding
              to 'x_tri' and 'y_invar' for the main locus surface, with values
              outside limits or behind the cut-off plane set to NaN.
            - tri1: A 1D NumPy array of stress triaxiality values for the plane
              stress curve.
            - invar1: A 1D NumPy array of normalized third invariant values for the
              plane stress curve.
            - ef1: A 1D NumPy array of calculated fracture strain values for the
              plane stress curve, with values outside limits set to NaN.
            - tri_k: A 1D NumPy array of measured stress triaxiality values for
              the calibration points.
            - invar_k: A 1D NumPy array of measured normalized third invariant 
              values for the calibration points.
            - ef_k: A 1D NumPy array of measured fracture strain values for the
              calibration points.
            - ef_r: A 1D NumPy array representing the residuals (differences)
              between measured ('ef_k') and predicted ('ef_kal') fracture strains for
              each calibration point.
            - total_abs_difference: The sum of the absolute values of 'ef_r',
              ignoring any NaN values.
            - p_calibration_error: A 1D NumPy array of percentage errors for each 
              calibration point, handling division by zero.
            - pt_calibration_error: The total sum of 'p_calibration_error' values, 
              representing the total percentage calibration error.
            - tri_c: A 2D NumPy array of cut-off stress triaxiality values calculated 
              for the main locus surface, used for plotting the cut-off plane.
    """

    # The least squares optimization method run function - Minimizes residuals and returns material parameters G1,... G6
    result = least_squares(lambda G_params: KHPS2_function(G_params, specimen_data, denominator_epsilon),
                           initial_G, bounds=(lower_bounds, upper_bounds), **optimization_options)
    
    # Final LSM results (Material parameters - KHPS2_function's unknown values)
    G1, G2, G3, G4, G5, G6 = result.x    # Definition for easier individual access
    final_G_params = result.x

    # Mesh matrix creation (Stress triaxiality - Normalized third invariant)
    Y_invar = np.linspace(-1, 1, 999)                   # Normalized third invariant - y coordinate
    X_tri = np.linspace(-3, 3, 999)                     # Stress triaxiality - x coordinate
    x_tri, y_invar = np.meshgrid(X_tri, Y_invar)        # Grid mesh creation

    # Locus cut-off plane stress triaxiality and fracture stain calculation
    tri_c, ef = locus_calculation(final_G_params, x_tri, y_invar, denominator_epsilon)
    ef[x_tri < tri_c] = np.nan              # Fracture strain suppression behind cut-off plane
    ef[ef < 0] = np.nan                     # Fracture strain suppression below 0 Z-coordinate
    ef[ef > z_lim[1]] = np.nan              # Fracture strain suppression above Z axis limit (using z_lim[1] for consistency)

    # Calculation of the plane stress curve
    tri1 = np.linspace(-2/3, 2/3, 999)              # Plane stress state - triaxiality
    invar1 = -27/2. * tri1 * (tri1**2 - 1/3)        # Plane stress state - normalized third invariant

    # Plane stress cut-off plane stress triaxiality and fracture stain calculation
    tri_c1, ef1 = locus_calculation(final_G_params, tri1, invar1, denominator_epsilon)
    ef1[ef1 < 0] = np.nan                     # Fracture strain suppression below 0 Z-coordinate
    ef1[ef1 > z_lim[1]] = np.nan              # Fracture strain suppression above Z axis limit

    # Measured specimens value assignment for marker plotting
    specimens_np_array = np.array(list(specimen_data.values()))      # Numpy array extraction
    ef_k = specimens_np_array[:, 0]       # Fracture strain of the measured specimens
    tri_k = specimens_np_array[:, 1]      # Stress triaxiality of the measured specimens
    invar_k = specimens_np_array[:, 2]    # Normalized third invariant of the measured specimens

    # Cut-off plane stress triaxiality and fracture stain of the locus for the same stress state as the calibration points
    tri_c_kal, ef_kal = locus_calculation(final_G_params, tri_k, invar_k, denominator_epsilon)

    # Calibration error evaluation
    ef_r = ef_k - ef_kal        # Difference between calibration points and the calibrated locus

    # Total calibration error (Sum of ef_r absolute differences, ignoring NaNs)
        # Same, but more robust functionality as:     abs(ef_r[0]) + abs(ef_r[1]) + abs(ef_r[2])...
    total_abs_difference = np.sum(np.abs(ef_r[~np.isnan(ef_r)]))

    # Calibration error in percentages for each specimen (Robustly handling division by zero)
        # Same, but more robust functionality as:       abs((ef_k - ef_kal) / ef_k) * 100
    p_calibration_error = np.abs((ef_k - ef_kal) / (ef_k + np.finfo(float).eps)) * 100

    # Replace any NaNs (e.g., from 0/0 scenarios) with 0 for summation
    p_calibration_error[np.isnan(p_calibration_error)] = 0

    # Total calibration error in percentages
    pt_calibration_error = np.sum(p_calibration_error)

    # Returned calculated values of Stress triaxiality, Normalized third invariant, Fracture strain of the main surface,
    # cut-off plane, plane stress curve, etc...         Also returns material parameters G1,... G6 and calibration errors
    return (final_G_params, x_tri, y_invar, ef, tri1, invar1, ef1,
                tri_k, invar_k, ef_k, ef_r, total_abs_difference, p_calibration_error, pt_calibration_error, tri_c)