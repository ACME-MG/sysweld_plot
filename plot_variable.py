#%% Import libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata 
import matplotlib.colors as colors
#%% Plot variable on cross section figure
#Function to plot variable on cross section figure
def plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=None,
    parameter_sec=None,variable=None,title=None,figure_no=None,
    title_text=18,unit=None,
    max_data=None,min_data=None,
    cMin=0,cMax=100,cticks_no=11,clevels_no=100,cbar_over_value=None,cscheme='jet',cbar_extend='both',cnorm=None,
    cbar_text=18,cbar_length=5,cbar_width=1, 
    cbar_bottom_offset=0.4,cbar_height=0.12,
    folder=None): 
    """
    Required Arguments:
        coord_sec: coordinates of cross section
        Xgrid,Ygrid: meshgrid to extrapolate data to
        fig,ax: figure and axes cross section are plotted on
        mask: coordinates of points inside outline (same dimension as Xgrid and Ygrid)
        section_axes: axes of cross section, e.g. ['X','Y','Z']
    Optional Arguments:
        Plot:
            paramater: dataframe name, default: None
            variable: column name in dataframe, e.g. 'XX'
            title: title for the plot, e.g. 'Transverse Stress'
            figure_no: figure number to be plotted on, e.g. 0
        Title/Axes:
        title_text: fontsize of title, default: 18
        unit: unit of the variable, e.g. 'MPa'
        Data:
            max_data: maximum value data can have (remove errors from extrapolating above max_data)
            min_data: minimum value data can have (remove errors from extrapolating below min_data)
        Colour Bar:
            cMin: minimum value for the colour bar, default: 0
            cMax: maximum value for the colour bar, default: 100
            cticks_no: number of ticks on the colour bar, default: 11
            clevels_no: number of levels on the colour bar, default: 100
            cbar_over_value: value to change colour bar to grey, default: None
            cscheme: colour scheme of colour bar, default: jet
            cnorm: normalisation of colour bar, default: None
            cbar_extend: colourbar ends, default: 'both', takes arguments of: 'neither', 'both', 'min', 'max'
            cbar_text: fontsize of colour bar ticks, default: 18
            cbar_length: length of colour bar ticks, default: 5
            cbar_width: width of colour bar ticks, default: 1
        Colour Bar Position:
            cbar_bottom_offset: offset of the colour bar from the bottom of the plot (% of height of plot), default: 0.4
            cbar_height: height of the colour bar (% of height of plot), default: 0.12
        Save:
            folder: folder to save plot to, default: None
    """
    Zgrid = griddata(coord_sec[[section_axes[0], section_axes[1]]], parameter_sec[variable], (Xgrid, Ygrid), method='cubic') #extrapolate variable values to meshgrid

    if min_data!=None or max_data!=None: #if max_data or min_data has a value, clip Zgrid to those values
        Zgrid=np.clip(Zgrid,min_data,max_data)

    print('Extrapolated '+variable+' values to meshgrid')

    Zgrid = np.ma.masked_where(~mask, Zgrid) #mask data outside of outline

    #Plot variable
    plt.figure(figure_no) #Plot on figure 0
    if unit==None:
        plt.title(title+' Prediction', fontsize = title_text)
    else:
        plt.title(title+' Prediction ['+unit+']', fontsize = title_text) #Title of plot
    
    
    class MidpointNormalize(colors.Normalize): #normalise levels for colour bar
        def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
            self.midpoint = midpoint
            colors.Normalize.__init__(self, vmin, vmax, clip)

        def __call__(self, value, clip=None):
            x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
            return np.ma.masked_array(np.interp(value, x, y))

    if cnorm!=None: #if cnorm has a value, normalise to eor midpoint
        cnorm=MidpointNormalize(vmin=cMin,vmax=cMax,midpoint=0)
        
    cticks=np.linspace(cMin,cMax,cticks_no) #Colour bar ticks
    
    if cbar_over_value!=None: #if cbar_over_value is not None, add cbar_over_value to colour bar ticks
        cticks=np.append(cticks,cbar_over_value)
        cMax=cbar_over_value #set cMax to cbar_over_value
        cscheme=plt.get_cmap('jet').copy() #copy colour scheme
        cscheme.set_over('grey') #set colour bar over cbar_over_value to grey

    levels = np.linspace(cMin, cMax, clevels_no) #Colour bar levels
    im=plt.contourf(Xgrid, Ygrid, Zgrid, levels, vmin=cMin, vmax=cMax, cmap=cscheme,extend=cbar_extend,norm=cnorm) #Plot variable

    #colour bar in new axes
    left, bottom, width, height = ax.get_position().bounds #position of plot
    cax = fig.add_axes([left, bottom-cbar_bottom_offset, width, height * cbar_height]) #position and size of new plot
    
    cbar=plt.colorbar(im, norm=cnorm,orientation='horizontal', cax=cax,ticks=cticks,extend=cbar_extend,extendfrac=0.03) #fraction of colour bar for extend arrows
 
    cbar.ax.tick_params(labelsize=cbar_text,length=cbar_length,width=cbar_width) #colour bar tick size

    plt.savefig(folder+title+' Map', bbox_inches='tight', dpi=300)

    cbar.remove() #Remove plot and colourbar for next plot

    print('Plotted map for '+title)