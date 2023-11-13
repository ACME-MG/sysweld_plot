#%% Seeing structure of file
# View structure of h5 file in VScode
import nexusformat.nexus as nx
import os
import pandas as pd

# #View structure of h5 file in visual studios
home_path=os.getcwd() #get current path
# os.chdir('/mnt/e/wendy_storage/Multi_pass/V18_Calibration/V150/03_RESU') #change to path to results file
# f=nx.nxload('MULTIPASS_POST2000.erfh5') #Load file
os.chdir('/mnt/d/SYSWELD/wendy/waam/coarse_v29/coarse_comb/03_RESU') #change to path to results file
f=nx.nxload('TG4_WELD_POST1000.erfh5') #Load file

f.tree #structure of file (put breakpoint here then debug in visual studio)
os.chdir(home_path) #change to original path

# # Export tree as txt file (takes a while)
# home_path=os.getcwd()
# os.chdir('/mnt/d/SYSWELD/wendy/waam/first_16_passes_v27')
# f=nx.nxload('TG4_WELD_POST2000.erfh5')
# with open('output','w') as output_file:
#     output_file.write(str(f.tree))
# os.chdir(home_path)