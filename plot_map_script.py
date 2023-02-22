#%% Import functions
from import_file import *
from import_coord import *
from import_var import *
from plot_section import *
from plot_variable import *
#%% Plot colour maps of variables from results file
path='/mnt/d/SYSWELD/wendy/Multi_pass/V18_Calibration/V150/03_RESU' #Path to file
folder='V150/' #Folder to save results into
file_name='MULTIPASS_HV_POST1000.erfh5' #title of results file, comment out whichever results aren't needed
# state='state000000000355' #state number (reading from results file for now)

file=import_file(path,file_name) #import results file
coord_var=import_coord(file) #coordinates of all nodes

axes=['X','Y','Z'] #axes to plot section on (plot on first two axes)

#Plot nodes, outline around nodes, and which points of meshgrid are inside the outline (go to function to change alpha shape)
ind_sec,coord_sec,Xgrid,Ygrid,fig,ax,mask=plot_section(coord_var,section_axes=axes,section_coord=10,fig_no=0,resolution=0.05,outline_width=1,
                                                        spines_off=['top','bottom','left','right'],
                                                        xstep=5,ystep=2,
                                                        offset_ticks_x=True,offset_ticks_y=True,textsize=18,
                                                        folder='V150/Outlines/',name='Multipass')
#%% Plot results from V_POST2000
# #Plot equivalent plastic strain
# var_sec=import_var(file,'plast_equiv_final',ind_sec) #values for required variable at required cross section
# plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                 parameter_sec=var_sec,variable='EQV',title='Equivalent Total Plastic Strain',figure_no=0,
#                 min_data=0,
#                 cMin=0,cMax=0.1,cticks_no=11,cbar_extend='max',
#                 cbar_bottom_offset=0.4,cbar_height=0.12,
#                 folder='V150/Plastic Strain/')

# #Plot stress_xx,stress_yy,stress_zz
# stress_name=['XX','YY','ZZ']; stress_title=['Stress_XX','Stress_YY','Stress_ZZ'] #loop through variables
# var_sec=import_var(file,'stress_final',ind_sec) #values for required variable at required cross section
# for i in range(len(stress_name)):
#     plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                     parameter_sec=var_sec,variable=stress_name[i],title=stress_title[i],figure_no=0,
#                     unit='MPa',
#                     cMin=-750,cMax=1500,cticks_no=10,cscheme='seismic',cnorm=True,
#                     cbar_bottom_offset=0.4,cbar_height=0.12,
#                     folder='V150/Stresses/')
#%% Plot results from HV_POST_1000
#Plot hardness
var_sec=import_var(file,'hardness',ind_sec) #values for required variable at required cross section
plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
                parameter_sec=var_sec,variable='HV',title='Hardness',figure_no=0,
                unit='HV',
                cMin=400,cMax=800,cticks_no=9,
                cbar_bottom_offset=0.4,cbar_height=0.12,
                folder='V150/Hardness/')

#Plot phases
phase_name=['Phase 1','Phase 2','Phase 3','Phase 4','Phase 5','Phase 6']; phase_title=['Martensite','Fictive','Tempered Bainite','Tempered Martensite','Bainite','Austenite']
var_sec=import_var(file,'phase_final',ind_sec) #values for required variable at required cross section
for i in range(len(phase_name)):
    plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
                parameter_sec=var_sec,variable=phase_name[i],title=phase_title[i],figure_no=0,
                min_data=0,max_data=1,
                cMin=0,cMax=1,cticks_no=11,cbar_extend='neither',
                cbar_bottom_offset=0.4,cbar_height=0.12,
                folder='V150/Phases/')

#%% Plot results from V_POST_1000
##Plot fusion
# var_sec=import_var(file,'fusion',ind_sec) #values for required variable at required cross section
# plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                 parameter_sec=var_sec,variable='Temp',title='Fusion Zone',figure_no=0,
#                 unit='C',
#                 cMin=0,cMax=1200,cticks_no=7,cbar_over_value=1422,cbar_extend='max',
#                 cbar_bottom_offset=0.4,cbar_height=0.12,
#                 folder='V150/Fusion/')