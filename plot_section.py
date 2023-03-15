
#%% Import libraries
import numpy as np
import matplotlib.pyplot as plt
import alphashape
from shapely.geometry import Point, Polygon
from geopandas import GeoSeries
#%%Define function to plot outline of cross section
def plot_section(coord=None,section_axes=None,section_coord=None,fig_no=0,resolution=0.1,outline_width=1,nodes_vis=True,
    spines_off=None,spine_xloc=None,spine_yloc=None,xlabel=None,ylabel=None,
    min_x=None,max_x=None,min_y=None,max_y=None,xstep=5,ystep=2,
    xticks_vis=True,yticks_vis=True,offset_ticks_x=False,offset_ticks_y=False,textsize=18,tick_width=1,
    plot_add=None,folder=None,export_name=None):

    """ This script plots cross sections of a 3D model, with the option to plot an outline and dimensions of the cross section.
    The script uses the alphashape library to create an outline of the cross section, which is then used to mask the data.
    See bottom of script for various alphashape parameters.

    Required arguments:
        coord: coordinates of entire cross section
        section_axes: axes of cross section, e.g. ['X','Y','Z']
        section_coord: location of cross section (coordinate along third axis of section_axes), e.g. 5
        fig_no: figure number to plot cross section on, default 0
        resolution: spacing of meshgrid (smaller value gives contour closer to outline, but takes longer), default 0.1
    Optional arguments:
        Outline:
            outline_width: width of line for outline, default: 1
            nodes_vis: plotting the nodes, default: True
        Spines:
            spines_off: which axes spines are not visible in plot, e.g. ['top','right','bottom','left']
            spine_xloc: vertical axes spine location, default: None
            spine_yloc: horizontal axes spine location, default: None
            xlabel,ylabel: axis title, default: None
        Axes:
            min_x,max_x: minimum/maximum value for x axis, default: None
            min_y,max_y: minimum/maximum value for y axis, default: None
            xstep: step size for horizontal axis, default: 5
            ystep: step size for vertical axis, default: 2
        Ticks:
            xticks_vis,yticks_vis: turn ticks on and off, default: True
            offset_ticks_x: offset horizontal axis ticks to start at zero, default: False
            offset_ticks_y: offset vertical axis ticks to start at zero, default: False
            textsize: font size for title and axis ticks, default: 18
            tick_width: width of axis ticks, default 1
        Additional Plotting:
            plot_add: additional plotting function, default: None
        Save:
            folder: folder to save figure in, default: None
            export_name: name of exported file, default: None
    Returns: 
        ind_sec: indices of nodes in cross section
        coord_sec: coordinates of cross section
        Xgrid,Ygrid: meshgrid to extrapolate data to
        fig,ax: figure and axes cross section are plotted on
        mask: coordinates of points inside outline (same dimension as Xgrid and Ygrid)
    """
    #Coordinates of nodes in cross section
    ind_sec=coord[section_axes[2]]==section_coord #indices of nodes in cross section at section_coord
    coord_sec=coord.loc[ind_sec]; #coordinates of cross section

    #Create meshgrid for cross section
    x_max=coord_sec[section_axes[0]].max(); x_min=coord_sec[section_axes[0]].min() #max and min values of horizontal axis
    y_max=coord_sec[section_axes[1]].max(); y_min=coord_sec[section_axes[1]].min() #max and min values of vertical axis
    Xrange = np.arange(x_min,x_max + resolution, resolution) # range of values in horizontal axis
    Yrange = np.arange(y_min, y_max + resolution, resolution) # range of values in vertical axis
    Xgrid, Ygrid = np.meshgrid(Xrange,Yrange) #create meshgrid
    x_diff=x_max-x_min; y_diff=y_max-y_min #differences between max and min values of axes
    aspect_ratio=y_diff/x_diff #aspect ratio for plot

    print('Meshgrid for required cross section')

    #Set up plot on figure 0 (one cross section plot)
    fig=plt.figure(fig_no,figsize=(15, 15*aspect_ratio)) #Figure size based on aspect ratio, set width of 15
    ax=plt.gca() #Get current axes
    plt.axis('equal') #Equal scale for both axes
    plt.xlim(x_min,x_max); plt.ylim(y_min-0.1,y_max+0.1) #Limits for axes (extra margin to plot outline)
    plt.title('Outline of Cross Section', fontsize = textsize) #Title of plot

    #Plot nodes and outline of cross section
    coord_array=np.array(coord_sec[[section_axes[0],section_axes[1]]]) #Convert coordinates to numpy arrays
    # alphashape_param=lambda ind, r: 0.2 + 0.8*np.logical_and(any(coord_array[ind][:,1]>6),any(coord_array[ind][:,1]<10))
    alphashape_param=lambda ind, r: 0.2+4.5*any(coord_array[ind][:,1]>0.1)
    alpha_shape = alphashape.alphashape(coord_sec[[section_axes[0],section_axes[1]]],alphashape_param) #Outline around nodes

    #Remove data outside of outline
    s=GeoSeries(map(Point,zip(Xgrid.flatten(),Ygrid.flatten()))) #create geoseries of points from meshgrid
    print('Converted meshgrid to Points')
    mask = alpha_shape.buffer(1e-2).contains(s) #Mask for points inside the outline, buffer to include boundary
    print('Found points inside outline')
    mask=mask.values.reshape(Xgrid.shape) #Reshape mask to match meshgrid size

    x_outline,y_outline = alpha_shape.exterior.xy #outline of cross section
    plt.plot(x_outline,y_outline,linewidth=outline_width,color='black') #plot outline of cross section

    if nodes_vis == True:
        plt.plot(coord_sec[section_axes[0]],coord_sec[section_axes[1]],',k') #plot nodes

    if spines_off!=None:
            ax.spines[spines_off].set_visible(False) #turn off axes spines listed in spines_off
    
    if spine_xloc==None: #if no value, set spine_xmin to minimum value of horizontal axis
        spine_xloc=x_min
    if spine_yloc==None: #if no value, set spine_ymin to minimum value of vertical axis
        spine_yloc=y_min

    ax.spines['left'].set_position(('data',spine_xloc)) ; ax.spines['bottom'].set_position(('data',spine_yloc)) #set left and bottom axes at locations

    if xticks_vis==True:
        xticks=np.arange(x_min, x_max+xstep*0.01, xstep); 
        if offset_ticks_x==False:
            plt.xticks(xticks,fontsize=18) #original axes ticks
        elif offset_ticks_x==True:
            plt.xticks(xticks, map(lambda x: "%g" % x, xticks-x_min),fontsize=textsize) #offset x axis ticks to start at zero
        else:
            plt.xticks(xticks, map(lambda x: "%g" % x, xticks-offset_ticks_x),fontsize=textsize) #offset x axis ticks to start at zero
    else: #turn off ticks
        xticks=[]
        plt.xticks(xticks)

    if yticks_vis==True:
        yticks=np.arange(y_min, y_max+ystep*0.01, ystep) #axes ticks
        if offset_ticks_y==False:
            plt.yticks(yticks,fontsize=18) #original axes ticks
        else:
            plt.yticks(yticks, map(lambda y: "%g" % y, yticks-y_min),fontsize=textsize) #offset x axis ticks to start at zero
    else: #turn off ticks
        yticks=[]
        plt.yticks(yticks)

    ax = plt.gca()
    ax.tick_params(width=tick_width)

    #if axes limit specified, set axes limits
    if min_x!=None and max_x!=None:
        x_diff=max_x-min_x
        aspect_ratio=y_diff/x_diff #aspect ratio for plot
        fig.set_size_inches(15, 15*aspect_ratio)
        plt.xlim(min_x,max_x)

    if min_y!=None and max_y!=None:
        y_diff=max_y-min_y
        aspect_ratio=y_diff/x_diff #aspect ratio for plot
        fig.set_size_inches(15, 15*aspect_ratio)
        plt.ylim(min_y,max_y)
    
    if xlabel!=None:
        plt.xlabel(xlabel,fontsize=textsize)
    if ylabel!=None:
        plt.ylabel(ylabel,fontsize=textsize)

    print('Plotted cross section outline')

    if plot_add=='fatigue': #if plot_add is fatigue, plot additional data on top of plot
        import pandas as pd
        from math import pi
        ellipse_data=['output_pass2','output_pass13'] #name of fatigue ellipse data
        x_offset=[1.5442,9.9592] #x offset for fatigue ellipses 
        colour=['black','black'] #colour of fatigue ellipses
        ellipse_cycle=30 #number of fatigue ellipses to plot

        ellipse_crop=3 #crop ellipse to show only part of ellipse, this crop is distance from centre to edge of ellipse
        mask_1=Polygon([[1.5442-ellipse_crop,0.3],[1.5442-ellipse_crop,-8],[1.5442+ellipse_crop,-8],[1.5442+ellipse_crop,0.3]]) #create polygon for ellipse crop
        mask_2=Polygon([[9.9592-ellipse_crop,0.3],[9.9592-ellipse_crop,-8],[9.9592+ellipse_crop,-8],[9.9592+ellipse_crop,0.3]]) 
        masks=[mask_1,mask_2]

        for j in range(len(ellipse_data)):
            ellipse_fatigue=pd.read_csv('V150/Fatigue/'+ellipse_data[j]+'.csv') #read in fatigue ellipse data
            ellipse_number=len(ellipse_fatigue)//ellipse_cycle #number of fatigue ellipses 
            ellipse_range = np.linspace(0,-pi, 2000) #range of angles for ellipse
            for i in range(ellipse_number): #loop through fatigue ellipse data every l00 rows
                ellipse_x_coord=x_offset[j]+ellipse_fatigue.iloc[i*ellipse_cycle,1]*1000*np.cos(ellipse_range) #x coordinates for ellipse
                ellipse_y_coord=0.2808+(ellipse_fatigue.iloc[i*ellipse_cycle,0]*1000)*np.sin(ellipse_range) #y coordinates for ellipse
                mask_ellipse_outline = alpha_shape.buffer(-1e-2).contains(GeoSeries(map(Point,zip(ellipse_x_coord,ellipse_y_coord)))) #Mask for points inside the outline
                mask_ellipse_crop = masks[j].contains(GeoSeries(map(Point,zip(ellipse_x_coord,ellipse_y_coord)))) #Mask for points inside the outline
                ellipse_x_coord = np.ma.masked_where(~(mask_ellipse_outline & mask_ellipse_crop), ellipse_x_coord) #mask ellipse x coord outside of outline
                ellipse_y_coord = np.ma.masked_where(~(mask_ellipse_outline & mask_ellipse_crop), ellipse_y_coord) #mask ellipse y coord outside of outline
                plt.plot(ellipse_x_coord,ellipse_y_coord,color=colour[j],linewidth=1.5) #plot ellipse

    plt.savefig(folder+export_name, bbox_inches='tight', dpi=300) #save outline of cross section

    return ind_sec,coord_sec,Xgrid,Ygrid,fig,ax,mask
#%% Alpha shape parameters
# alphashape_param: parameter for alphashape that gives rough outline (can be constant or varying with coordinates):
#     constant value: 0.2    
#     varying for one condition: lambda ind, r: 0.2+4.5*any(coord_array[ind][:,1]>0.1)
#     varying for multiple conditions: lambda ind, r: 0.2 + 0.8*np.logical_and(any(coord_array[ind][:,1]>0),any(coord_array[ind][:,1]<0.3))