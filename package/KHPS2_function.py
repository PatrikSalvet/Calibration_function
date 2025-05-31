    # Library and package import
import numpy as np
from .Locus_calculation import locus_calculation

    # Definition of the ductile fracture criterion (mathematical function definition)
        # specimen[0] = Fracture strain   specimen[1] = Stress triaxiality   specimen[2] = Normalized third invariant
        # G[0] - G[5] = Investigated parameters (constants) G1, G2,... G6
def KHPS2_function(G, specimen_data, denominator_epsilon = 1e-6):
        """
        Calculates the residuals for the KHPS2 ductile fracture criterion.

        This function takes a set of material parameters (G) and experimental
        specimen data, then calculates the difference between the measured fracture
        strain and the fracture strain predicted by the KHPS2 model for each specimen.
        These differences (residuals) are then used by an optimization algorithm
        (like scipy.optimize.least_squares) to find the optimal G parameters.
        
        Input parameters:          KHPS2_function(G, specimen_data, denominator_epsilon)
        ------------------
        G:
            A 1D array of 6 material parameters (unknown constants) for the KHPS2 model:
        specimen_data:
            A dictionary where keys are specimen names (e.g., "specimen1") and
            values are lists representing the measured data for each specimen.
            Each list must be in the format of:
                [Fracture strain, Stress triaxiality, Normalized third invariant]
            - specimen[0]: Measured Fracture strain
            - specimen[1]: Measured Stress triaxiality
            - specimen[2]: Measured Normalized third invariant of deviatoric stress tensor
        denominator_epsilon:
            A small value to prevent division by zero, ensuring numerical stability.
            float with default value of 1e-6
        ------------------

        The function returns a 1D array of residuals. Each element represents the difference
        between the measured fracture strain and the predicted fracture strain for 
        the corresponding specimen. The goal of the optimization is to minimize the sum of
        squares of these residuals.

        The function leverages Locus_calculation.py function to perform the core fracture locus
        prediction in a vectorized manner.
        """
    # Initial material parameter inputs unpacking
        G1, G2, G3, G4, G5, G6 = G

    # Extraction of the measured datas into NumPy arrays,    specimens_np_array contains aproximation points
            # [Fracture strain, Stress triaxiality, Normalized third invariant]
        specimens_np_array = np.array(list(specimen_data.values()))

    # Extraction of all fracture strains, stress triaxialities, and normalized third invariants.
        # Optimized numpy syntax replacing extraction by for loop
        ef_k = specimens_np_array[:, 0]
        tri_k = specimens_np_array[:, 1]
        invar_k = specimens_np_array[:, 2]

    # Calculation of the locus fracture strain for the current specimen
        _, ef_kal = locus_calculation(
            G_params=G,                    # List of initial material parameters
            ri_values=tri_k,               # All triaxiality values as an array
            invar_values=invar_k,          # All invariant values as an array
            denominator_epsilon = denominator_epsilon)   # Numerical stability constant

    # Residual calculation: difference between ideal (measured) fracture strain and calculated fracture strain value
        residuals = ef_k - ef_kal
        return residuals