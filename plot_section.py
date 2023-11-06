#%% Import libraries
import numpy as np
import matplotlib.pyplot as plt
import alphashape
from shapely.geometry import Point, Polygon
from geopandas import GeoSeries
import pandas as pd
#%%
def plot_section(coord = None,section_axes = ['X','Y','Z'], section_coord = 0, fig_no = 0, resolution = 0.1,
                fig_width = 15, outline_width = 1, outline_file = None, nodes_vis = True, textsize = 18, plot_title = 'Outline and Nodes', 
                spines_off = ['top','bottom','left','right'],spine_xloc = None,spine_yloc = None,
                xticks_vis = True, yticks_vis = True, xstep = 10,ystep = 10, offset_ticks_x = 0, offset_ticks_y = 0, tick_width = 1,
                crop_min_x = None, crop_max_x = None, crop_min_y = None, crop_max_y = None, xlabel = None, ylabel = None,
                folder = None,export_name = 'outline of cross section'):

    """ 
    This script plots the outline and nodes of cross sections of a 3D model, and also creates a meshgrid and mask
    for plotting variables on the cross section.
    The outline can be plotted from a list of points or from the alpha shape of the nodes (automatically finds outline from given nodes).
    This outline will be used to mask data outside of the outline when plotting variables on the cross section. 
    The bottom of the script has examples of various alphashape parameters. 

    Arguments:
        Cross section:
            coord (dataframe):          coordinates of nodes of entire model
            section_axes (list):        list of three axes with plot on first two axes and normal to third axis, default: ['X','Y','Z']
            section_coord (float):      coordinate along third axis to plot cross section at, default: 0
            resolution (float):         spacing of meshgrid (smaller value gives a more accurate map, but takes longer), default 0.1
            fig_no (int):               figure number for cross section plot, default 0

        Outline and Nodes:
            fig_width (float):          width of figure in inches, default: 15
            outline_file (string):      name of excel file with list of points for outline
            outline_width (float):      width of line for outline, default: 1
            nodes_vis (bool):           plotting the nodes of cross section, default: True
            textsize (float):           font size for title and axis ticks, default: 18
            plot_title (string):        title of plot, default: 'Outline and Nodes'
        Spines:
            spines_off (list):          which axis spines are not visible in plot, default: ['top','right','bottom','left']
            spine_xloc (float):         vertical axis spine location, default: minimum horizontal axis value
            spine_yloc (float):         horizontal axis spine location, default: minimum vertical axis value
        Ticks:
            xticks_vis (bool):          horizontal axis ticks visibility, default: True
            yticks_vis (bool):          vertical axis ticks visibility, default: True
            xstep (float):              step size for horizontal axis, default: 10
            ystep (float):              step size for vertical axis, default: 10
            offset_ticks_x (float):     offset horizontal axis ticks by this value, default: 0
            offset_ticks_y (float):     offset vertical axis ticks by this value, default: 0
            tick_width (float):         width of axis ticks, default 1
        Axes:
            crop_min_x (float):         crop horizontal axis minimum value, default: min of original horizontal axis
            crop_max_x (float):         crop horizontal axis maximum value, default: max of original horizontal axis
            crop_min_y (float):         crop vertical axis minimum value, default: min of original vertical axis
            crop_max_y (float):         crop vertical axis maximum value, default: max of origina vertical axis
            xlabel (string):            horizontal axis label, default: no label 
            ylabel (string):            vertical axis label, default: no label 
        Save:
            folder (string):            folder path to save figure in
            export_name (string):       name of exported file, default: 'outline of cross section'
    Returns: 
        ind_sec (bool dataframe):       indices of nodes in cross section
        coord_sec (dataframe) :         coordinates of nodes cross section
        Xgrid,Ygrid:                    meshgrid to extrapolate data to
        fig,ax:                         figure and axes cross section are plotted on
        mask:                           coordinates of points inside outline (same dimension as Xgrid and Ygrid)
    """
    # Coordinates of nodes in cross section
    ind_sec = coord[section_axes[2]] == section_coord #indices of nodes in cross section 
    coord_sec = coord.loc[ind_sec] #coordinates of nodes in cross section

    # Create meshgrid for cross section
    x_max = coord_sec[section_axes[0]].max(); x_min=coord_sec[section_axes[0]].min() # max and min values of horizontal axis
    y_max=coord_sec[section_axes[1]].max(); y_min=coord_sec[section_axes[1]].min() # max and min values of vertical axis
    Xrange = np.arange(x_min,x_max + resolution, resolution) # range of values in horizontal values spaced by resolution
    Yrange = np.arange(y_min, y_max + resolution, resolution) # range of values in vertical axis spaced by resolution
    Xgrid, Ygrid = np.meshgrid(Xrange,Yrange) #create meshgrid

    # Find aspect ratio of cross section to size figure for cross section
    x_diff = x_max - x_min; y_diff = y_max - y_min # differences between max and min values of axes
    aspect_ratio = y_diff/x_diff #aspect ratio of cross section

    print('Meshgrid calculated for cross section')

    # Set up figure
    fig = plt.figure(fig_no, figsize=(fig_width, fig_width*aspect_ratio)) # figure size based on aspect ratio, set width of 15
    ax = plt.gca() # get current axes
    plt.title(plot_title, fontsize = textsize)
    plt.axis('equal') # equal scale for both axes
    plt.xlim(x_min,x_max); plt.ylim(y_min - 0.1,y_max + 0.1) # Limits for axes (extra margin to plot outline)

    # Find outline of cross section
    if outline_file != None: # outline taken from excel file
        outline = pd.read_excel(outline_file) # import list of points for outline from excel file
        outline = outline[[section_axes[0],section_axes[1]]] # only take columns for horizontal and vertical axes
        alpha_shape = Polygon(outline) # convert outline to shapely polygon
    else: # automatically find outline from nodes in cross section
        alpha_shape = alphashape.alphashape(coord_sec[[section_axes[0],section_axes[1]]],0.2) # more alphashape parameters at bottom of script

    # Make mask to not plot map outside of outline
    s = GeoSeries(map(Point,zip(Xgrid.flatten(),Ygrid.flatten()))) # create geoseries of points from meshgrid
    print('Converted meshgrid to Points')
    mask = alpha_shape.buffer(1e-2).contains(s) # mask for points inside the outline, buffer to include boundary
    print('Found points inside outline')
    mask=mask.values.reshape(Xgrid.shape) # reshape mask to match meshgrid size

    # Plot outline of cross section
    x_outline,y_outline = alpha_shape.exterior.xy # exterior of cross section
    plt.plot(x_outline,y_outline,linewidth=outline_width,color='black') # plot outline

    # Plot nodes of cross section
    if nodes_vis == True: 
        s = GeoSeries(map(Point,zip(coord_sec[section_axes[0]],coord_sec[section_axes[1]]))) # create geoseries of points from nodes
        mask_nodes = alpha_shape.buffer(1e-2).contains(s) # find nodes inside outline
        mask_nodes = mask_nodes.values # indices of nodes inside outline
        plt.plot(coord_sec[section_axes[0]][mask_nodes].values,coord_sec[section_axes[1]][mask_nodes].values,',k') # plot nodes inside outline

    # Format spines
    ax.spines[spines_off].set_visible(False) # turn off axes spines listed in spines_off
    if 'bottom' not in spines_off: # bottom spine is visible
        if spine_yloc == None: # if no value, set bottom spine to minimum value of vertical axis
            spine_yloc = y_min
        ax.spines['bottom'].set_position(('data',spine_yloc))
    if 'left' not in spines_off: # left spine is visible
        if spine_xloc == None: # if no value, plot vertical spine at minimum value of horizontal axis
            spine_xloc = x_min
        ax.spines['left'].set_position(('data',spine_xloc))

    # Format ticks
    if xticks_vis == True: # horizontal axis ticks are visible
        xticks = np.arange(x_min, x_max + xstep, xstep) # all horizontal axis values
        plt.xticks(xticks, map(lambda x: "%g" % x, xticks-offset_ticks_x),fontsize = textsize) #offset x axis ticks to start at zero             
    else: # horizontal axis ticks are not visible
        plt.tick_params(bottom = False, labelbottom = False)
    if yticks_vis == True: # vertical axis ticks are visible
        yticks = np.arange(y_min, y_max + ystep, ystep) # all vertical axis values
        plt.yticks(yticks, map(lambda y: "%g" % y, yticks-offset_ticks_y),fontsize = textsize) #offset x axis ticks to start at zero
    else: # vertical axis ticks are not visible
        plt.tick_params(left = False, labelleft = False)
    ax.tick_params(width = tick_width) # width of axis ticks

    # Optional crop of cross section 
    if crop_min_x != None or crop_max_x != None: #horizontal axis crop
        if crop_min_x == None: # default minimum horizontal axis value if none given
            crop_min_x = x_min
        if crop_max_x == None: # default maximum horizontal axis value if none given
            crop_max_x = x_max
        x_diff = crop_max_x - crop_min_x
        aspect_ratio = y_diff/x_diff # new aspect ratio for plot
        fig.set_size_inches(fig_width, fig_width*aspect_ratio) # resize figure
        plt.xlim(crop_min_x,crop_max_x) # crop axes
    if crop_min_y != None or crop_max_y != None: #horizontal axis crop
        if crop_min_y == None: # default minimum horizontal axis value if none given
            crop_min_y = y_min
        if crop_max_y == None: # default maximum horizontal axis value if none given
            crop_max_y = y_max
        y_diff = crop_max_y - crop_min_y
        aspect_ratio = y_diff/x_diff # new aspect ratio for plot
        fig.set_size_inches(fig_width, fig_width*aspect_ratio) # resize figure
        plt.ylim(crop_min_y - 0.1,crop_max_y + 0.1) # crop axes
    
    # Axes labels
    if xlabel != None: # horizontal axis label
        plt.xlabel(xlabel,fontsize = textsize)
    if ylabel != None: # vertical axis label
        plt.ylabel(ylabel,fontsize = textsize)

    print('Plotted cross section outline')

    plt.savefig(folder + export_name, bbox_inches='tight', dpi=300) # save outline of cross section, high resolution

    return ind_sec,coord_sec,Xgrid,Ygrid,fig,ax,mask
#%% Alpha shape parameters
# coord_array = np.array(coord_sec[[section_axes[0],section_axes[1]]]) #Convert coordinates to numpy arrays
# alphashape_param: parameter for alphashape that gives rough outline (can be constant or varying with coordinates):
#     constant value: 0.2    
#     varying for one condition: lambda ind, r: 0.2+4.5*any(coord_array[ind][:,1]>0.1)
#     varying for multiple conditions: lambda ind, r: 0.2 + 0.8*np.logical_and(any(coord_array[ind][:,1]>0),any(coord_array[ind][:,1]<0.3))
