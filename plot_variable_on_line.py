# import librariers
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# define function
def plot_variable_on_line(data_file = None, x_data_title = None, y_data_title = None, plot_title = None, x_label = None, y_label = None, plot_width = 5, plot_height = 5, curve_colour = None, curve_label = None, curve_lw = 2, save_title = None, x_min = None, x_max = None, x_step = 5, y_min = None, y_max = None, y_step = 5, legend_fontsize = 12, plot_fontsize = 12, title_fontsize = 20):
    """Make plot of variable along a line

    Parameters
    ----------
    data_file : str
        The name of the csv file containing the coordinates and variable values along the line
    x_data_title: str
        The title of the column containing the x data
    y_data_title : list of str
        The titles of the columns containing the y data
    plot_title, x_label, y_label : str
        The title of the whole plot, and the x and y axis labels
    plot_width, plot_height : float, default 5
        The width and height of the plot in inches
    curve_colour, curve_label : list of str
        The colours and legend labels of the curves
    curve_lw : float, default 2
        The linewidth of the curves
    save_title : str
        The name of the file the plot is saved as
    x_min, x_max, y_min, y_max: float
        The minimum and maximum of the x and y axes, which default to plot all the data if not specified
    x_step, y_step: float, default 5
        The interval of the ticks on the x and y axes
    legend_fontsize, plot_fontsize : float, default 12
        The font sizes of the legend and plot (axes and ticks)
    title_fontsize : float, default 20
        The font size of the title of the whole plot, and the subplot titles

    """    
    # import data
    data_line = pd.read_csv(data_file)

    # set up the figure
    fig = plt.figure(figsize = (plot_width, plot_height))

    # plot data
    for i in range(len(y_data_title)):
        plt.plot(data_line[x_data_title].values, data_line[y_data_title[i]].values, color = curve_colour[i], linewidth = curve_lw, label = curve_label[i])

    # add x-axis
    plt.axhline(y = 0, color = 'k', linewidth = 1)

    # tick parameters
    if x_min != None or x_max != None:
        plt.xticks(np.arange(x_min, x_max + x_step, x_step))
        plt.xlim(x_min, x_max) # limit after setting ticks
    if y_min != None or y_max != None:
        plt.yticks(np.arange(y_min, y_max + y_step, y_step))
        plt.ylim(y_min, y_max)
    plt.tick_params(labelsize = plot_fontsize, direction = 'in')

    # grid
    plt.grid(linestyle = ':', linewidth = 1, color = 'SlateGrey')

    # legend
    plt.legend(fontsize = legend_fontsize)

    # titles
    plt.title(plot_title, fontsize = title_fontsize)
    plt.xlabel(x_label, fontsize = plot_fontsize)
    plt.ylabel(y_label, fontsize = plot_fontsize)
   
    plt.tight_layout() # reduce extra space around the plots
    plt.savefig(save_title, dpi = 300)

    




