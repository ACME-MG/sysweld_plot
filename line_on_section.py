#%% Import libraries
import numpy as np
import matplotlib.pyplot as plt
import alphashape
from shapely.geometry import Point, Polygon
from geopandas import GeoSeries
import pandas as pd
#%%
def line_on_section(coord = None, parameter_sec = None, line_axes = ['X','Y','Z'], section_coord = 0.0, line_pos = 0.0,
            fig_no = 0, textsize = 18, plot_title = 'Line on Cross Section',
            folder = None, export_name = 'line on cross section'):

    """ 
    This script plots the required line on the cross section.

    Arguments:
        Line:
            coord (dataframe):          coordinates of nodes of entire model
            parameter_sec (dataframe):  parameter values of nodes of the cross section
            line_axes (list):           first axis is what line is constant for, second axis is what line varies on, third axis is normal to cross section default: ['X','Y','Z']
            section_coord (float):      coordinate along third axis to plot cross section at, default: 0
            line_pos (float):           coordinate which line is constant for, default: 0
        Plot:
            fig_no (int):               figure number to plot on, default 0
            textsize (float):           font size for title and axis ticks, default: 18
            plot_title (string):        title of plot, default: Line on Cross Section'
        Save:
            folder (string):            folder path to save figure in
            export_name (string):       name of exported file, default: 'line on cross section'
    Returns: 
        ind_line (bool dataframe):      indices of nodes on line
        coord_line (dataframe) :        coordinates of nodes on line
    """
    # Coordinates of nodes on line
    ind_line = (coord[line_axes[0]] == line_pos) & (coord[line_axes[2]] == section_coord) #indices of nodes on line
    coord_line = coord.loc[ind_line] #coordinates of nodes on line

    # export variable values along line to csv
    var_line = parameter_sec.loc[ind_line] # variable values along line
    data_line = pd.concat([coord_line, var_line], axis = 1) # coordinates and variable values along line
    data_line = data_line.sort_values(by = line_axes[1]) # sort by varying axis along line
    data_line.to_csv(folder + 'data_line.csv') # export data to csv

    # plot on figure
    plt.figure(fig_no) # same figure from cross section outline
    plt.title(plot_title, fontsize = textsize)
    im = plt.plot(data_line[line_axes[0]].values, data_line[line_axes[1]].values, '-' ,color = 'red') # plot line on cross section

    # save figure
    plt.savefig(folder + export_name, bbox_inches = 'tight', dpi = 300) # save plot, high resolution

    for handle in im: # remove plotted line from cross section
        handle.remove()


    print('Exported data on line')