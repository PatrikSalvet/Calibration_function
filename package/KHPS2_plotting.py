    # Library import
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

    # KHPS2 plotting function
def KHPS2_plotting(x_tri, y_invar, ef, tri1, invar1, ef1, tri_k, invar_k, 
                   ef_k, specimen_data, plotting_options,tri_c):

    """
    Generates a 3D plot of the KHPS2 fracture locus and overlays experimental data.

    Function execution:
        KHPS2_plotting(x_tri, y_invar, ef, tri1, invar1, ef1, tri_k, invar_k, 
                    ef_k, specimen_data, plotting_options,tri_c):

    Function's input parameters:
        x_tri: 2D mesh grid for stress triaxiality (X-coordinates of the surface).
        y_invar: 2D mesh grid for normalized third invariant (Y-coordinates of the surface).
        ef: 2D array of fracture strain values (Z-coordinates of the surface),
                       with NaN values for regions outside the valid locus.
        tri1: 1D array of stress triaxiality values for the plane stress curve.
        invar1: 1D array of normalized third invariant values for the plane stress curve.
        ef1: 1D array of fracture strain values for the plane stress curve.
        tri_k: 1D array of stress triaxiality values for the calibration points.
        invar_k: 1D array of normalized third invariant values for the calibration points.
        ef_k: 1D array of fracture strain values for the calibration points.
        specimen_data: Original dictionary of specimen data, used for retrieving specimen names for labels.
            Format: {specimen_name: [list of values]}.
        tri_c: 2D array of cut-off stress triaxiality values, used for plotting the cut-off plane.
        plotting_options: A dictionary containing all configurable plotting parameters.
            Expected keys include:
            - 'figure_size', 'view_elev', 'view_azim', 'x_lim', 'y_lim', 'z_lim',
            - 'x_label', 'y_label', 'z_label', 'plot_title', 'labelpad_x', 'labelpad_y', 'labelpad_z',
            - 'title_y_position', 'label_font_size', 'title_font_size',
            - 'surface_alpha', 'surface_rgb_color',
            - 'plane_stress_line_color', 'plane_stress_line_width',
            - 'constant_invariant_line_color', 'constant_invariant_line_width',
            - 'marker_styles', 'marker_size_area', 'marker_face_colors', 'marker_edge_color', 'marker_edge_linewidth',
            - 'plot_cut_off_plane', 'cut_off_plane_color', 'cut_off_plane_alpha',
            - 'plot_plane_stress_curve', 'plot_approximated_points', 'plot_constant_invariant_curves'.

        Function's output:
            Displays a 3D plot based on the specified inputs. No value is returned by the function.
    """

    # Figure creation
    fig = plt.figure(figsize=plotting_options['figure_size'])
    ax = fig.add_subplot(111, projection='3d')

    # Graph limits
    ax.set_xlim(plotting_options['x_lim'])
    ax.set_ylim(plotting_options['y_lim'])
    ax.set_zlim(plotting_options['z_lim'])

    # Main surface plot
    surf = ax.plot_surface(x_tri, y_invar, ef, cmap='viridis', edgecolor='none', alpha=plotting_options['surface_alpha'])

    # Labels and title setting
    ax.set_xlabel(plotting_options['x_label'], fontsize=plotting_options['label_font_size'], fontweight='bold', labelpad=plotting_options['labelpad_x'])
    ax.set_ylabel(plotting_options['y_label'], fontsize=plotting_options['label_font_size'], fontweight='bold', labelpad=plotting_options['labelpad_y'])
    ax.set_zlabel(plotting_options['z_label'], fontsize=plotting_options['label_font_size'], fontweight='bold', labelpad=plotting_options['labelpad_z'])
    ax.set_title(plotting_options['plot_title'], fontsize=plotting_options['title_font_size'], fontweight='bold', y=plotting_options['title_y_position'])
    # Graph view rotation
    ax.view_init(elev=plotting_options['view_elev'], azim=plotting_options['view_azim'])

    # Main surface plot face color setting
    surf.set_facecolor(plotting_options['surface_rgb_color'])

    # Cut-off plane plot
    if plotting_options['plot_cut_off_plane']:
        cut_off_plane = ax.plot_surface(tri_c, y_invar, ef,
                                        color=plotting_options['cut_off_plane_color'],
                                        alpha=plotting_options['cut_off_plane_alpha'],
                                        edgecolor='none')

    # Plane stress curve plot
    if plotting_options['plot_plane_stress_curve']:
        ax.plot(tri1, invar1, ef1,
                color=plotting_options['plane_stress_line_color'],
                linewidth=plotting_options['plane_stress_line_width'])

    # Constant normalized third invariant value curves
    if plotting_options['plot_constant_invariant_curves']:
        middle_index = len(y_invar[:, 0]) // 2
        ax.plot(x_tri[-1, :], y_invar[-1, :], ef[-1, :],
                linewidth=plotting_options['constant_invariant_line_width'],
                color=plotting_options['constant_invariant_line_color'])
        ax.plot(x_tri[0, :], y_invar[0, :], ef[0, :],
                linewidth=plotting_options['constant_invariant_line_width'],
                color=plotting_options['constant_invariant_line_color'])
        ax.plot(x_tri[middle_index, :], y_invar[middle_index, :], ef[middle_index, :],
                linewidth=plotting_options['constant_invariant_line_width'],
                color=plotting_options['constant_invariant_line_color'])

    # Calibration point plot
    if plotting_options['plot_approximated_points']:
        specimen_names = list(specimen_data.keys())
        for i in range(len(specimen_data)):
            ax.scatter(tri_k[i], invar_k[i], ef_k[i],
                       marker=plotting_options['marker_styles'][i],
                       s=plotting_options['marker_size_area'],
                       edgecolor=plotting_options['marker_edge_color'],
                       linewidth=plotting_options['marker_edge_linewidth'],
                       facecolor=plotting_options['marker_face_colors'][i],
                       label=f'{specimen_names[i]}')

    # Display
    plt.show()