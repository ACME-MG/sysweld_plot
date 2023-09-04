#%% Import functions
from import_file import *
from import_coord import *
from import_var import *
from plot_section import *
from plot_variable import *
import time
#%% Time how long code takes
t0=time.time()
#%% parameters to change
path='/mnt/d/SYSWELD/wendy' #Path to results file
file_name='TJOINT-1_V_POST1000.erfh5' #title of results file
sysweld_app='weld' #min_weld (POST1000,POST2000), weld (VPOST100,VPOST2000), or assembly (from visual assembly)
axes=['X','Y','Z'] #axes to plot section on (plot on first two axes, third axis is normal to cross section)
save_folder='V27/' #folder to save results into 

parameter = 'phase' #parameter to plot (fusion, phase, hardness, stress, peeq)
#%% Plot outline of cross section
file=import_file(path,file_name) #import results file
coord_var=import_coord(file,sysweld_app) #obtain coordinates of all nodes

# plot figure with outline and nodes
ind_sec,coord_sec,Xgrid,Ygrid,fig,ax,mask=\
plot_section(coord_var,section_axes = axes, section_coord = 0, fig_no = 0, resolution = 0.15,
fig_width = 15, outline_width = 3.5, outline_file = 'outline_t_section.xlsx', nodes_vis = True, textsize = 18, plot_title = 'Outline and Nodes',
spines_off = ['top','bottom','left','right'],spine_xloc = -100, spine_yloc = None,
xticks_vis = True, yticks_vis = True, xstep = 5,ystep = 5, offset_ticks_x = 0, offset_ticks_y = 0, tick_width = 1,
crop_min_x = -20, crop_max_x = 20, crop_min_y = None, crop_max_y = 20, xlabel = ' X [mm]', ylabel = 'Y [mm]',
folder = save_folder,export_name = 'outline of cross section')
#%%POST1000/VPOST1000: plot fusion zone, phases
if parameter == 'fusion':
    var_sec = import_var(file,sysweld_app, ind_sec, parameter)
    plot_variable(coord_sec, Xgrid, Ygrid, fig, ax, mask, section_axes = axes,
    parameter_sec = var_sec, variable = 'Temp', min_data = 0, max_data = None,
    figure_no = 0, title_vis = True, plot_title = 'Fusion Zone', title_textsize = 18,
    cnorm = False, cMin = 0, cMax = 1200, cticks_no = 7, cbar_over_value = 1300, clevelMin = None, clevelMax = None, clevels_no = 100, cscheme = 'jet',
    cbar = True, cbar_extend = 'max', cbar_bottom_offset = 0.12, cbar_height = 0.03, cbar_extend_frac = 0.03,
    cbar_text = 18, cbar_length = 5, cbar_tick_width = 1, cbar_title = 'Temperature [C]', cbar_title_pad = 10,
    folder = save_folder, export_name = 'Fusion Zone Map')

if parameter == 'phase':
    phase_name=['Phase 1','Phase 2','Phase 3','Phase 4','Phase 5','Phase 6']
    phase_title=['Martensite','Fictive','Ferrite','Pearlite','Bainite','Austenite']

    var_sec = import_var(file,sysweld_app, ind_sec, parameter, state_no = -1, pent_ele = True)

    for i in range(len(phase_name)):
        plot_variable(coord_sec, Xgrid, Ygrid, fig, ax, mask, section_axes = axes,
        parameter_sec = var_sec, variable = phase_name[i], min_data = 0, max_data = 1,
        figure_no = 0, title_vis = True, plot_title = phase_title[i]+' Prediction', title_textsize = 18,
        cnorm = False, cMin = 0, cMax = 1, cticks_no = 11, cbar_over_value = None, clevelMin = None, clevelMax = None, clevels_no = 100, cscheme = 'jet',
        cbar = True, cbar_extend = 'neither', cbar_bottom_offset = 0.12, cbar_height = 0.03, cbar_extend_frac = 0.03,
        cbar_text = 18, cbar_length = 5, cbar_tick_width = 1, cbar_title = 'Phase Fraction', cbar_title_pad = 10,
        folder = save_folder, export_name = phase_name[i] + ' Map')
#%%HVPOST1000: plot hardness 
if parameter == 'hardness':
    var_sec = import_var(file, sysweld_app, ind_sec, parameter, state_no = -1, pent_ele = True)
    plot_variable(coord_sec, Xgrid, Ygrid, fig, ax, mask, section_axes = axes,
    parameter_sec = var_sec, variable = phase_name[i], min_data = None, max_data = None,
    figure_no = 0, title_vis = True, plot_title = 'Hardness Prediction', title_textsize = 18,
    cnorm = False, cMin = 400, cMax = 800, cticks_no = 9, cbar_over_value = None, clevelMin = None, clevelMax = None, clevels_no = 100, cscheme = 'jet',
    cbar = True, cbar_extend = 'both', cbar_bottom_offset = 0.12, cbar_height = 0.03, cbar_extend_frac = 0.03,
    cbar_text = 18, cbar_length = 5, cbar_tick_width = 1, cbar_title = 'Hardness [HV]', cbar_title_pad = 10,
    folder = save_folder, export_name = 'Hardness Map')
#%%POST2000/VPOST2000: plot stressess and equivalent plastic strain
if parameter == 'stress':
    stress_name=['XX','YY','ZZ']
    stress_title=['$\sigma_{XX}$','$\sigma_{YY}$','$\sigma_{ZZ}$'] #loop through variables

    var_sec = import_var(file, sysweld_app, ind_sec, parameter, state_no = -1, pent_ele = True)

    for i in range(len(stress_name)):
        plot_variable(coord_sec, Xgrid, Ygrid, fig, ax, mask, section_axes = axes,
        parameter_sec = var_sec, variable = stress_name[i], min_data = None, max_data = None,
        figure_no = 0, title_vis = True, plot_title = stress_title[i]+' Prediction', title_textsize = 18,
        cnorm = True, cMin = -400, cMax = 400, cticks_no = 9, cbar_over_value = None, clevelMin = -425, clevelMax = 425, clevels_no = 100, cscheme = 'seismic',
        cbar = True, cbar_extend = 'both', cbar_bottom_offset = 0.12, cbar_height = 0.03, cbar_extend_frac = 0.03,
        cbar_text = 18, cbar_length = 5, cbar_tick_width = 2, cbar_title = 'Residual Stress [MPa]', cbar_title_pad = 10,
        folder = save_folder, export_name = 'Stress' +stress_name[i] + ' Map')

if parameter == 'peeq':
    var_sec = import_var(file, sysweld_app, ind_sec, parameter, state_no = -1, pent_ele = True)   
    plot_variable(coord_sec, Xgrid, Ygrid, fig, ax, mask, section_axes = axes,
    parameter_sec = var_sec, variable = 'strain', min_data = 0, max_data = None,
    figure_no = 0, title_vis = True, plot_title = 'Equivalent Plastic Strain Prediction', title_textsize = 18,
    cnorm = False, cMin = 0, cMax = 1, cticks_no = 11, cbar_over_value = None, clevelMin = None, clevelMax = None, clevels_no = 100, cscheme = 'jet',
    cbar = True, cbar_extend = 'max', cbar_bottom_offset = 0.12, cbar_height = 0.03, cbar_extend_frac = 0.03,
    cbar_text = 18, cbar_length = 5, cbar_tick_width = 2, cbar_title = 'PEEQ', cbar_title_pad = 10,
    folder = save_folder, export_name = 'PEEQ Map')
# %% Time how long code takes
t1=time.time()
total=t1-t0
print(str(total)+'s to run')
