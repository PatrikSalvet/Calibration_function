    # Library import
import numpy as np

def locus_calculation(G_params, tri_values, invar_values, denominator_epsilon=1e-6):
    """
    Calculates the cut-off stress triaxiality (tri_c) and fracture strain (ef)
    for the KHPS2 fracture criterion.

    Function inputs:
        G_params: Array of material parameters [G1, G2, G3, G4, G5, G6].
        tri_values: Array of stress triaxiality values.
        invar_values: Array of normalized third invariant values.
        denominator_epsilon: A small value to prevent division by zero or near-zero.

    Function outputs:
        (tri_c, ef)     <- tuple of cut-off plane stress triaxiality, fracture strain
    """
    # KHPS2_function.py results - calibrated parameters
    G1, G2, G3, G4, G5, G6 = G_params

    # Cut-off plane stress triaxiality calculation
    tri_c = -(G3 + (G1 - G3) / 2 - G2) * invar_values**2 - ((G1 - G3) / 2) * invar_values - G2

    # Denominator filtering for numerical stability
    denominator_raw = tri_values - tri_c
    denominator_filtered = np.where(np.abs(denominator_raw) < denominator_epsilon, np.nan, denominator_raw)

    # Fracture strain calculation
    ef = ((1/2) * (G4 / denominator_filtered + G5 / denominator_filtered) - (G6 / denominator_filtered)) * invar_values**2 + \
         ((1/2) * (G4 / denominator_filtered - G5 / denominator_filtered)) * invar_values + G6 / denominator_filtered

    # Functions outputs - Cut-off plane stress triaxiality, fracture strain
    return tri_c, ef