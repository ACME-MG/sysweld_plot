#%% Import functions
from import_file import *
from import_coord import *
from import_var import *
from plot_section import *
from plot_variable import *
import time
#%% Time how long code takes
t0=time.time()
#%% Plot colour maps of variables from results file
# path='/mnt/d/SYSWELD/wendy/Multi_pass/V18_Calibration/V150/03_RESU' #Path to file
# folder='V150/' #Folder to save results into
# file_name='MULTIPASS_HV_POST1000.erfh5' #title of results file, comment out whichever results aren't needed
# sysweld_app='weld'

path='/mnt/d/SYSWELD/wendy/Multi_pass/Inherent/300M_V4/Joining' #Path to file
folder='assembly_code/' #Folder to save results into
file_name='V8_Complex_Inherent_Joining-STAGE1_RESULT.erfh5'#title of results file, comment out whichever results aren't needed
sysweld_app='assembly'

file=import_file(path,file_name) #import results file
coord_var=import_coord(file,sysweld_app) #coordinates of all nodes

axes=['X','Y','Z'] #axes to plot section on (plot on first two axes)

#Plot nodes, outline around nodes, and which points of meshgrid are inside the outline (go to function to change alpha shape)
ind_sec,coord_sec,Xgrid,Ygrid,fig,ax,mask=plot_section(coord_var,section_axes=axes,section_coord=10,fig_no=0,resolution=0.05,
                                        spines_off=['top','bottom','left','right'],
                                        xstep=5,ystep=2,
                                        offset_ticks_x=True,offset_ticks_y=True,textsize=18,tick_width=1,
                                        folder='V150/Outlines/',export_name='outline of cross section for inherent')
#%% Plot results from V_POST2000
# #Plot equivalent plastic strain
# var_sec=import_var(file,sysweld_app,'plast_equiv_final',ind_sec) #values for required variable at required cross section
# plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                 parameter_sec=var_sec,variable='EQV',plot_title='Equivalent Total Plastic Strain Prediction',figure_no=0,
#                 min_data=0,
#                 cMin=0,cMax=0.1,cticks_no=11,cbar_extend='max',
#                 cbar_bottom_offset=0.4,cbar_height=0.12,
#                 folder='V150/Plastic Strain/',export_name='Equivalent Total Plastic Strain Prediction')

# #Plot stress_xx,stress_yy,stress_zz
# stress_name=['XX','YY','ZZ']; stress_title=['$\sigma_{XX}$','$\sigma_{YY}$','$\sigma_{ZZ}$'] #loop through variables
# var_sec=import_var(file,sysweld_app,'stress_final',ind_sec) #values for required variable at required cross section
# for i in range(len(stress_name)):
#     plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                     parameter_sec=var_sec,variable=stress_name[i],plot_title=stress_title[i]+' Prediction [MPa]',figure_no=0,
#                     cMin=-750,cMax=1500,cticks_no=10,cscheme='seismic',cnorm=True,
#                     cbar_bottom_offset=0.4,cbar_height=0.12,
#                     folder='V150/Stresses/',export_name=stress_title[i]+' Prediction')
#%% Plot results from HV_POST_1000
# #Plot hardness
# var_sec=import_var(file,sysweld_app,'hardness',ind_sec) #values for required variable at required cross section
# plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                 parameter_sec=var_sec,variable='HV',plot_title='Hardness Prediction [HV]',figure_no=0,
#                 cMin=400,cMax=800,cticks_no=9,
#                 cbar_bottom_offset=0.15,cbar_height=0.05,
#                 folder='V150/Fatigue/',export_name='Hardness Prediction')

# #Plot phases
# phase_name=['Phase 1','Phase 2','Phase 3','Phase 4','Phase 5','Phase 6']; phase_title=['Martensite','Fictive','Tempered Bainite','Tempered Martensite','Bainite','Austenite']
# var_sec=import_var(file,sysweld_app,'phase_final',ind_sec) #values for required variable at required cross section
# for i in range(len(phase_name)):
#     plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                 parameter_sec=var_sec,variable=phase_name[i],plot_title=phase_title[i]+' Prediction',figure_no=0,
#                 min_data=0,max_data=1,
#                 cMin=0,cMax=1,cticks_no=11,cbar_extend='neither',
#                 cbar_bottom_offset=0.4,cbar_height=0.12,
#                 folder='V150/Phases/',export_name=phase_title[i]+' Prediction')

#%% Plot results from V_POST_1000
##Plot fusion
# var_sec=import_var(file,sysweld_app,'fusion',ind_sec) #values for required variable at required cross section
# plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                 parameter_sec=var_sec,variable='Temp',plot_title='Fusion Zone Prediction [C]',figure_no=0,
#                 cMin=0,cMax=1200,cticks_no=7,cbar_over_value=1422,cbar_extend='max',
#                 cbar_bottom_offset=0.4,cbar_height=0.12,
#                 folder='V150/Fusion/',export_name='Fusion Zone Prediction')
#%% Plot results from assembly
# #Plot stress_xx,stress_yy,stress_zz
# stress_name=['XX','YY','ZZ']; stress_title=['$\sigma_{XX}$','$\sigma_{YY}$','$\sigma_{ZZ}$'];export_title=['Stress_XX','Stress_YY','Stress_ZZ'] #loop through variables
# var_sec=import_var(file,sysweld_app,'inherent_stress_final',ind_sec) #values for required variable at required cross section
# for i in range(len(stress_name)):
#     plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                     parameter_sec=var_sec,variable=stress_name[i],plot_title=stress_title[i]+' Prediction [MPa]',figure_no=0,
#                     cMin=-750,cMax=1500,cticks_no=10,cscheme='seismic',cnorm=True,
#                     cbar_bottom_offset=0.4,cbar_height=0.12,
#                     folder='assembly_code/',export_name=export_title[i]+' Map')
# #plot equivalent plastic strain
# var_sec=import_var(file,sysweld_app,'inherent_equiv_plas_strain_final',ind_sec) #values for required variable at required cross section
# plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
#                 parameter_sec=var_sec,variable='strain',plot_title='Equivalent Plastic Strain Prediction',figure_no=0,
#                 min_data=0,
#                 cMin=0,cMax=0.1,cticks_no=11,
#                 cbar_bottom_offset=0.4,cbar_height=0.12,cbar_extend='max',
#                 folder='assembly_code/',export_name='Equivalent Plastic Strain Map')

#plot thermal strain
var_sec=import_var(file,sysweld_app,'inherent_thermal_strain_final',ind_sec) #values for required variable at required cross section
plot_variable(coord_sec,Xgrid,Ygrid,fig,ax,mask,section_axes=axes,
                parameter_sec=var_sec,variable='strain',plot_title='Thermal Strain Prediction',figure_no=0,
                max_data=0,
                cMin=-0.03,cMax=0,cticks_no=7,
                cbar_bottom_offset=0.4,cbar_height=0.12,
                folder='assembly_code/',export_name='Thermal Strain Map')
# %% Time how long code takes
t1=time.time()
total=t1-t0
print(str(total)+' to run')