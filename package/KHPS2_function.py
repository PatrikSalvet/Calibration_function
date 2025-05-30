    # Library import
import numpy as np

    # Definition of the ductile fracture criterion (mathematical function definition)
        # specimen[0] = Fracture strain   specimen[1] = Stress triaxiality   specimen[2] = Normalized third invariant
        # G[0] - G[5] = Investigated parameters (constants) G1, G2,... G6
def KHPS2_function(G, specimen_data):
        """Calculates the residuals for the KHPS2 ductile fracture criterion.

        This function takes a set of material parameters (G) and experimental
        specimen data, then calculates the difference between the measured fracture
        strain and the fracture strain predicted by the KHPS2 model for each specimen.
        These differences (residuals) are then used by an optimization algorithm
        (like scipy.optimize.least_squares) to find the optimal G parameters.
        
        Input parameters:
        ------------------
        G:
            A 1D array of 6 material parameters (constants) for the KHPS2 model:
        specimen_data :
            A dictionary where keys are specimen names (e.g., "specimen1") and
            values are lists representing the measured data for each specimen.
            Each list must be in the format of:
                [Fracture strain, Stress triaxiality, Normalized third invariant]
            - specimen[0]: Measured Fracture strain
            - specimen[1]: Measured Stress triaxiality
            - specimen[2]: Measured Normalized third invariant of deviatoric stress tensor
        ------------------

        The function returns a 1D array of residuals. Each element represents the difference
        between the measured fracture strain and the predicted fracture strain for 
        the corresponding specimen. The goal of the optimization is to minimize the sum of
        squares of these residuals.

        The function calculates two main components:
        1.  Cut-off plane values: An constant calculated for each specimen based on G1, 
            G2, G3, and the specimen's normalized third invariant. This value acts as
            an input to the fracture locus function.
        2.  Fracture locus prediction: The equivalent fracture strain predicted
            by the KHPS2 criterion for each specimen, using G4, G5, G6, specimen's
            stress triaxiality, and the calculated cut-off plane value.
        """
    
    # Convertion into list for better iteration,   specimens_list contains aproximation points
        specimens_list = list(specimen_data.values())
        cutoff_plane_values = []
    
    # cutoff_plane = Cut off stress triaxiality (calculated constant for each specimen. Input for the fracture locus function)
    # Calculated for each specimen (approximation point separately)
        for specimen in specimens_list:
            cutoff_plane = (G[2] + (G[0] - G[2]) / 2 - G[1]) * (specimen[2])**2 + (G[0] - G[2]) * specimen[2] / 2 + G[1]
    # list of calculated cut-off stress triaxiality values for each specimen
            cutoff_plane_values.append(cutoff_plane)   

    # Minimized (residual) variable place holder
        residuals = []
    # Calculation of the fracture strain and residuals for each individual specimen (aproximation point)
        for i, specimen in enumerate(specimens_list):
    # Cut-off plane value of the currently calculated specimen
            current_cutoff_plane = cutoff_plane_values[i]
    # Equivalent fracture strain calculation of the currently calculated specimen
            fracture_locus_prediction = ((1/2) * (G[3] / (specimen[1] + current_cutoff_plane) + G[4] / (specimen[1] + current_cutoff_plane)) - \
                                     G[5] / (specimen[1] + current_cutoff_plane)) * specimen[2]**2 + \
                                    (1/2) * (G[3] / (specimen[1] + current_cutoff_plane) - G[4] / (specimen[1] + current_cutoff_plane)) * specimen[2] + \
                                    G[5] / (specimen[1] + current_cutoff_plane)
            
    # Residual calculation,... difference between ideal (measured - specimen) fracture strain and calculated fracture strain value
            residual_val = specimen[0] - fracture_locus_prediction
            residuals.append(residual_val)

    # Functions output: residuals - The goal is to minimize this value
        return np.array(residuals)