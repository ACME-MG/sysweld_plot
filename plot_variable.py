#%% Import libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata 
import matplotlib.colors as colors
#%% Plot variable on cross section figure
#Function to plot variable on cross section figure
def plot_variable(coord_sec, Xgrid, Ygrid, fig, ax, mask, section_axes = None,
    parameter_sec = None, variable = None, min_data = None, max_data = None,
    figure_no = 0, title_vis = True, plot_title = 'Title of Plot', title_textsize = 18,
    cnorm = False, cMin = 0, cMax = 100, cticks_no = 11, cbar_over_value = None,clevelMin = None, clevelMax = None, clevels_no = 100,cscheme = 'jet',
    cbar = True, cbar_extend = 'both', cbar_bottom_offset = 0.1, cbar_height = 0.05, cbar_extend_frac = 0.03,
    cbar_text = 18, cbar_length = 5, cbar_tick_width = 1, cbar_title = 'Colour Bar Title', cbar_title_pad = 10,
    folder = None, export_name = 'Colour Map of Cross Section'): 
    """
    Arguments:

        coord_sec (dataframe) :         coordinates of nodes cross section
        Xgrid,Ygrid:                    meshgrid to extrapolate data to
        fig,ax:                         figure and axes cross section are plotted on
        mask:                           coordinates of points inside outline (same dimension as Xgrid and Ygrid)
        section_axes (list):            list of three axes with plot on first two axes and normal to third axis, default: ['X','Y','Z']
        
        Data:
            parameter_sec (dataframe):  parameter values at each node
            variable (string):          column name in dataframe ('HV', 'XX', 'YY', 'ZZ', 'Phase 1', 'Phase 2', etc., 'Temp', 'strain')
            min_data (float):           minimum value data can have (remove errors from extrapolating below min_data), default: None
            max_data (float):           maximum value data can have (remove errors from extrapolating above max_data), default: None
        Plot:
            figure_no (int):            figure number for cross section plot, default 0
            title_vis (bool):           whether to plot title, default: True
            plot_title (string):        title for the plot, default: 'Title of Plot'
            title_textsize:             fontsize of title, default: 18
        Colour Map:
            cnorm (bool):               setting midpoint of colour bar to zero, default: False
            cMin (float):               minimum value for the colour bar ticks, default: 0
            cMax (float):               maximum value for the colour bar ticks, default: 100
            cticks_no (float):          number of ticks on the colour bar, default: 11
            cbar_over_value (float):    maximum value before colour bar changes to grey, default: None
            clevelMin (float):          minimum value for the colour map levels, default: cMin
            clevelMax (float):          maximum value for the colour map levels, default: cMax
            clevels_no (float):         number of levels for the colour map, default: 100
            cscheme (string):           colour scheme of colour bar, default: jet
        Colour Bar:
            cbar (bool):                whether to plot colour bar, default: True
            cbar_extend (string):       colourbar ends, default: 'both', takes arguments of: 'neither', 'both', 'min', 'max'
            cbar_bottom_offset (float:  offset of the colour bar from the bottom of the plot (% of height of plot), default: 0.1
            cbar_height (float):        height of the colour bar (% of height of plot), default: 0.05
            cbar_extend_frac (float):   fraction of colour bar to extend for arrows, default: 0.03
        Colour Bar Text/Ticks
            cbar_text (float):          fontsize of colour bar ticks, default: 18
            cbar_length (float):        length of colour bar ticks, default: 5
            cbar_width (float):         width of colour bar ticks, default: 1
            cbar_title (string):        title of colour bar, default: 'Colour Bar Title'
            cbar_title_pad (float):     padding between colour bar title and colour bar, default: 10
        Save:
            folder (string):            path to folder to save plot to, default: None
            export_name (string):       name of exported file, default: 'Colour Map of Cross Section'
    """
    # Extrapolate parameter values on cross section
    nan_ind = parameter_sec[variable].isnull() # indices of nodes where there are nan values
    Zgrid=griddata((coord_sec.loc[~nan_ind,section_axes[0]],coord_sec.loc[~nan_ind,section_axes[1]]),\
                   parameter_sec.loc[~nan_ind,variable], (Xgrid, Ygrid), method='cubic') # extrapolate non-nan parameter values to meshgrid
    if min_data != None or max_data != None: #if max_data or min_data has a value, remove any errors in extrapolation outside that range
        Zgrid=np.clip(Zgrid,min_data,max_data)
    Zgrid = np.ma.masked_where(~mask, Zgrid) #mask data outside of outline
    print('Extrapolated '+variable+' values to meshgrid')

    # Figure to plot on
    plt.figure(figure_no) # plot on figure no
    if title_vis == True: # plot title visiblity
        plt.title(plot_title, fontsize = title_textsize) 

    # Colour bar
    class MidpointNormalize(colors.Normalize): # class for setting midpoint value of colour bar
        def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
            self.midpoint = midpoint
            colors.Normalize.__init__(self, vmin, vmax, clip)

        def __call__(self, value, clip=None):
            x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
            return np.ma.masked_array(np.interp(value, x, y))
        
    if cnorm == True: # normalise to zero midpoint
        cnorm = MidpointNormalize(vmin=cMin,vmax=cMax,midpoint=0)
    elif cnorm == False: # no normalisation
        cnorm = None

    cticks = np.linspace(cMin,cMax,cticks_no) # colour bar ticks

    if cbar_over_value != None: # colour bar is grey over this value
        cticks=np.append(cticks,cbar_over_value) # add value to colour bar ticks
        cMax=cbar_over_value #set cMax to cbar_over_value
        cscheme=plt.get_cmap('jet').copy() #copy colour scheme
        cscheme.set_over('grey') #set colour bar over cbar_over_value to grey

    if clevelMin == None: # set minimum colour bar level to tick minimum value
        clevelMin = cMin
    if clevelMax == None: # set maximum colour bar level to tick maximum value
        clevelMax = cMax

    levels = np.linspace(clevelMin, clevelMax, clevels_no) # colour bar levels do not need to match ticks
    im = plt.contourf(Xgrid, Ygrid, Zgrid, levels, vmin = cMin, vmax = cMax, cmap = cscheme,extend = cbar_extend,norm = cnorm) # plot colour map

    # Add colour bar in axes below the plot of cross section
    if cbar == True:
        left, bottom, width, height = ax.get_position().bounds # position of cross section plot
        cax = fig.add_axes([left, bottom-cbar_bottom_offset, width, height * cbar_height]) # position and size of new plot for colour bar
        cbar = plt.colorbar(im, norm = cnorm, orientation = 'horizontal', cax = cax,ticks = cticks,
                          extend = cbar_extend, extendfrac = cbar_extend_frac) # plot colour bar
        cbar.ax.tick_params(labelsize = cbar_text, length = cbar_length, width = cbar_tick_width) # format colour bar ticks 
        if cbar_title != None: # colourbar title visibility
            cbar.ax.set_xlabel(cbar_title, fontsize = cbar_text, labelpad = cbar_title_pad) # colourbar title
        plt.savefig(folder + export_name, bbox_inches = 'tight', dpi = 300) # save figure
        cbar.remove() # remove colourbar for next plot
    else:
        plt.savefig(folder+export_name+' Map', bbox_inches='tight', dpi=300)
        cbar.remove() # remove colourbar for next plot
    
    print('Plotted map')
