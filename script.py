
#%% Parameters to change 

# File path to where code is saved 
path_to_code        = '/home/wjux/projects/sysweld_plot'

# SYSWELD file parameters
path_to_results     = '/mnt/d/SYSWELD/wendy/waam/coarse_v29/coarse_iso/03_RESU' #Path to results file
results_file_name   = 'TG4_WELD_POST2000.erfh5' #title of results file
sysweld_app         = 'min_weld' 
                       # min_weld (POST1000,POST2000), weld (HVPOST1000,VPOST1000,VPOST2000), or assembly (from visual assembly)
pent_ele            = False # whether there are penta elements
state_no            = -1 # state number to plot results at

# save file parameters
path_to_save        = '/home/wjux/projects/waam/stress/316L/iso/' # folder to save results in

# variable parameters
variable            = 'stress' # variable to plot: fusion, phase, hardness, stress, peeq
resolution          = 0.15 # resolution of interpolation, lower for accuracy, higher for speed

# cross-section parameters
section_axes        = ['X','Y','Z'] # [horizontal, vertical, normal]
section_coord       = 100 # constant coordinate of cross section

# plot of cross-section parameters
outline_file        = '/home/wjux/projects/waam/outlines/outline_second_cut.xlsx' 
                       # title of outline file (optional); set to none to let code find outline
crop_min_x          = None # crop cross section 
crop_max_x          = None # crop cross section
xstep               = 20 # tick interval on x-axis
crop_min_y          = None # crop cross section 
crop_max_y          = 105  # crop cross section 
ystep               = 20 # tick interval on y-axis
xlabel              = 'X (mm)' # x-axis title
ylabel              = 'Y (mm)' # y-axis title
nodes_vis           = True # visibility of mesh nodes
section_file        = 'outline of cross section' # name of saved cros section plot

# colour bar parameters
cbar_vis            = True # visibility of colour bar
cbar_bottom_offset  = 0.07 # offset from the bottom of the plot (% of plot height)
cbar_height         = 0.02 # height of the colour bar (% of plot height)

# line parameters (optional)
plot_line           = True # whether to plot variable along line
line_axes           = ['X','Y','Z']  # [constant, varies, normal to section line is on]
line_coord          = 50 # constant coord of line
line_section_file   = 'line on cross section' # name of saved file of line on cross section plot

# line plot parameters (optional)
line_x_min          = 0 # axes limits
line_x_max          = 105 # axes limits
line_x_step         = 20 # tick interval on axes
line_y_min          = -300 # axes limits
line_y_max          = 300 # axes limits
line_y_step         = 100 # tick interval on axes
curve_colour        = ['black','red','green','royalblue','magenta','gold'] # colours of curves
line_plot_title     = 'Residual Stress Along Centreline' # plot title
line_xlabel         = 'Height from Substrate Bottom (mm)' # x axis label
line_ylabel         = 'Residual Stress (MPa)' # y axis label
line_file           = 'stress_centreline' # name of saved line plot 

# fusion zone map and colour bar parameters (POST1000/VPOST1000/HVPOST1000)
if variable == 'fusion': 
    min_data        = 0 # crop erroneous values in data
    max_data        = None # crop erroneous values in data
    plot_title      = ['Fusion Zone'] # title of plot
    cnorm           = False # set midpoint of colour bar to zero
    cticks_min      = 0 # min tick on colour bar
    cticks_max      = 1400 # max tick on colour bar
    cticks_no       = 8 # no of ticks on colour bar
    cbar_over_value = 1422 # value that colour bar is grey above
    cbar_min        = None # min colour bar level (None sets it to min tick)
    cbar_max        = None # max colour bar level (None sets it to max tick)
    cbar_levels_no   = 100 # no of colour bar levels
    cscheme         = 'jet' # colour bar scheme
    cbar_extend     = 'max' # colour bar extension
    cbar_title      = 'Temperature (C)' # colour bar title
    plot_file       = ['Fusion Zone'] # name of saved colour map file

# phase map and colour bar parameters (POST1000/VPOST1000/HVPOST1000)
if variable == 'phase': 
    min_data        = 0 # crop erroneous values in data
    max_data        = 1 # crop erroneous values in data
    plot_title      = ['Martensite','Fictive','Ferrite','Pearlite','Bainite','Austenite'] # title of plot
    cnorm           = False # set midpoint of colour bar to zero
    cticks_min      = 0 # min tick on colour bar
    cticks_max      = 1 # max tick on colour bar
    cticks_no       = 11 # no of ticks on colour bar
    cbar_over_value = None # value that colour bar is grey above
    cbar_min        = None # min colour bar level (None sets it to min tick)
    cbar_max        = None # max colour bar level (None sets it to max tick)
    cbar_levels_no   = 100 # no of colour bar levels
    cscheme         = 'jet' # colour bar scheme
    cbar_extend     = 'neither' # colour bar extension
    cbar_title      = 'Phase Fraction' # colour bar title
    plot_file       = ['Martensite','Fictive','Ferrite','Pearlite','Bainite','Austenite'] # name of saved colour map file
    variable_label = ['Martensite','Fictive','Ferrite','Pearlite','Bainite','Austenite'] # curve label for line

# hardness map and colour bar parameters (HVPOST1000)
if variable == 'hardness': 
    min_data        = None # crop erroneous values in data
    max_data        = None # crop erroneous values in data
    plot_title      = ['Hardness'] # title of plot
    cnorm           = False # set midpoint of colour bar to zero
    cticks_min      = 400 # min tick on colour bar
    cticks_max      = 800 # max tick on colour bar
    cticks_no       = 9 # no of ticks on colour bar
    cbar_over_value = None # value that colour bar is grey above
    cbar_min        = None # min colour bar level (None sets it to min tick)
    cbar_max        = None # max colour bar level (None sets it to max tick)
    cbar_levels_no   = 100 # no of colour bar levels
    cscheme         = 'jet' # colour bar scheme
    cbar_extend     = 'both' # colour bar extension
    cbar_title      = 'Hardness (HV)' # colour bar title
    plot_file       = ['Hardness'] # name of saved colour map file
    variable_label = ['hardness'] # curve label for line

# stress map and colour bar parameters (POST2000/VPOST2000)
if variable == 'stress': 
    min_data        = None # crop erroneous values in data
    max_data        = None # crop erroneous values in data
    plot_title      = ['$\sigma_{XX}$','$\sigma_{YY}$','$\sigma_{ZZ}$'] # title of plot
    cnorm           = True # set midpoint of colour bar to zero
    cticks_min      = -400 # min tick on colour bar
    cticks_max      = 400 # max tick on colour bar
    cticks_no       = 9 # no of ticks on colour bar
    cbar_over_value = None # value that colour bar is grey above
    cbar_min        = -450 # min colour bar level (None sets it to min tick)
    cbar_max        = 450 # max colour bar level (None sets it to max tick)
    cbar_levels_no   = 100 # no of colour bar levels
    cscheme         = 'seismic' # colour bar scheme
    cbar_extend     = 'both' # colour bar extension
    cbar_title      = 'Residual Stress (MPa)' # colour bar title
    plot_file       = ['stress_xx','stress_yy','stress_zz'] # name of saved colour map file
    variable_label = ['$\sigma_{XX}$','$\sigma_{YY}$','$\sigma_{ZZ}$'] # curve label for line

# peeq map and colour bar parameters (VPOST2000)
if variable == 'peeq': 
    min_data        = N0 # crop erroneous values in data
    max_data        = 1 # crop erroneous values in data
    plot_title      = ['Equivalent Plastic Strain'] # title of plot
    cnorm           = False # set midpoint of colour bar to zero
    cticks_min      = 0 # min tick on colour bar
    cticks_max      = 1 # max tick on colour bar
    cticks_no       = 11 # no of ticks on colour bar
    cbar_over_value = None # value that colour bar is grey above
    cbar_min        = None # min colour bar level (None sets it to min tick)
    cbar_max        = None # max colour bar level (None sets it to max tick)
    cbar_levels_no   = 100 # no of colour bar levels
    cscheme         = 'jet' # colour bar scheme
    cbar_extend     = 'neither' # colour bar extension
    cbar_title      = 'PEEQ' # colour bar title
    plot_file       = ['PEEQ'] # name of saved colour map file
    variable_label = ['PEEQ'] # curve label for line

#%% Import libraries and functions, and set variable column names from import_var
import sys
sys.path.append(path_to_code) # add path to look for where code is
from import_file import *
from import_coord import *
from import_var import *
from plot_section import *
from plot_variable import *
from plot_variable_on_line import *
from line_on_section import *

# name of columns containing variables (named in import_var)
if variable == 'fusion':
    variable_name = ['Temp']
if variable == 'phase':
    variable_name=['Phase 1','Phase 2','Phase 3','Phase 4','Phase 5','Phase 6']
if variable == 'hardness':
    variable_name=['HV']
if variable == 'stress':
    variable_name = ['XX','YY','ZZ'] 
if variable == 'peeq':
    variable_name = ['strain']
#%% Execute script

# import results file
file = import_file(path_to_results, results_file_name) 

# obtain coordinates of all nodes
coord_var = import_coord(file, sysweld_app) 

# plot cross-section outline and nodes
ind_sec, coord_sec, Xgrid, Ygrid, fig, ax, mask = plot_section(coord_var, section_axes = section_axes, section_coord = section_coord, resolution = resolution, outline_file = outline_file, nodes_vis = nodes_vis, xstep = xstep, ystep = ystep, crop_min_x = crop_min_x, crop_max_x = crop_max_x, crop_min_y = crop_min_y, crop_max_y = crop_max_y, xlabel = xlabel, ylabel = ylabel, folder = path_to_save, export_name = section_file)

# calculate variable values on cros section only
var_sec = import_var(file, sysweld_app, ind_sec, variable, state_no = state_no, pent_ele = pent_ele)

# plot variable values on cross section
for i in range(len(variable_name)):
    plot_variable(coord_sec, Xgrid, Ygrid, fig, ax, mask, section_axes = section_axes, parameter_sec = var_sec, variable = variable_name[i], min_data = min_data, max_data = max_data, figure_no = 0, title_vis = True, plot_title = plot_title[i] + ' Prediction', title_textsize = 18, cnorm = cnorm, cMin = cticks_min, cMax = cticks_max, cticks_no = cticks_no, cbar_over_value = cbar_over_value,clevelMin = cbar_min, clevelMax = cbar_max, clevels_no = cbar_levels_no, cscheme = cscheme, cbar = cbar_vis, cbar_extend = cbar_extend, cbar_bottom_offset = cbar_bottom_offset, cbar_height = cbar_height, cbar_extend_frac = 0.03, cbar_text = 18, cbar_length = 5, cbar_tick_width = 1, cbar_title = cbar_title, cbar_title_pad = 10, folder = path_to_save, export_name = plot_file[i] + ' Map')

# plot line on cross section and export variable values on line to csv (optional)
if plot_line == True:
    line_on_section(coord = coord_var, parameter_sec = var_sec, section_axes = section_axes, line_axes = line_axes, section_coord = section_coord, line_pos = line_coord, folder = path_to_save, export_name = line_section_file)
#%% Plot variable values on line (can rerun this section with parameters and libraries as csv already exported)
if plot_line == True:
    plot_variable_on_line(data_file = path_to_save + 'data_line.csv', x_data_title = line_axes[1], y_data_title = variable_name, plot_title = line_plot_title, x_label = line_xlabel, y_label = line_ylabel, plot_width = 5, plot_height = 5, curve_colour = curve_colour, curve_label = variable_label, curve_lw = 2, save_title = path_to_save + line_file, x_min = line_x_min, x_max = line_x_max, x_step = line_x_step, y_min = line_y_min, y_max = line_y_max, y_step = line_y_step, legend_fontsize = 12, plot_fontsize = 12, title_fontsize = 12)

# %%
