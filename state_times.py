#%% Import
import nexusformat.nexus as nx
import os
import pandas as pd


home_path=os.getcwd() #get current path
os.chdir('/mnt/d/SYSWELD/wendy/waam/coarse_comb_alt/03_RESU') #change to path to results file
f=nx.nxload('TG4_WELD_POST1000.erfh5') #Load file
os.chdir(home_path) #change back to original path

# %% save to csv file list of state times
state_results=f['SYSWELD']['singlestate']
states=state_results.keys() #List of states
states=list(states) #Convert dict_keys to list

# make vector of all times
state_times =pd.DataFrame(columns=['time'])

for i in range(len(states)):
    state_time = state_results[states[i]]['entityresults']['NODE']['TEMPERATURE_NOD']['ZONE1_set0']['erfblock']['indexval']
    # state_time = pd.DataFrame(state_time)
    # state_time = state_time.iloc[0,0]
    state_times.loc[i] = state_time
    if i%1000==0:
        print(i, 'out of', len(states))

state_times.to_csv('time/coarse_comb_alt.csv')
