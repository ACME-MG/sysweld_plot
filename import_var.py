
#%%
import numpy as np
import pandas as pd
#%%
def import_var(file,parameter,ind_sec):
    """
    This script imports the values for the required variables on the specified cross section.

    Required arguments:
        file: imported file
        parameter: variable to import
        ind_sec: indices for required cross section
    Returns:
        var_sec: required variable's values
    """

    states=file['SYSWELD']['singlestate'].keys() #List of states
    states=list(states) #Convert dict_keys to list
    final_state=states[-1] #Final state

    #Path to node results for final states (not actually tested yet)
    node_path_final=file['SYSWELD']['singlestate'][final_state]['entityresults']['NODE']

    if parameter=='fusion': #Fusion of nodes
        for i in states: #find maximum fusion value for all states
            node_path=file['SYSWELD']['singlestate'][i]['entityresults']['NODE']
            var=node_path['TEMPERATURE_NOD']['ZONE1_set0']['erfblock']['res']
            var=pd.DataFrame(var) #Convert to dataframe
            var=var.loc[ind_sec] #variable values of cross section
            if i==states[0]: #first iteration
                var_max=var #set var_max to initial temps
            else: #add other temps to var_max as columns
                var_max=pd.concat([var_max,var],axis=1) 
        var_max=var_max.max(axis=1) #find max temp for each node
        var_max=pd.DataFrame(var_max) #Convert to dataframe
        var_max=var_max.rename(columns={0:'Temp'}) #rename column Temp
        var_sec=var_max
    
    if parameter=='hardness': #Hardness of nodes
        var=node_path_final['HARDNESS_NOD']['ZONE1_set1']['erfblock']['res']
        var=pd.DataFrame(var) #Convert to dataframe
        var=var.rename(columns={0:'HV'}) #rename column HV
        var_sec=var.loc[ind_sec] #variable values of cross section

    if parameter=='phase_final': #Phase proportions of nodes
        var=node_path_final['PHASE_PROPORTIONS_NOD']['ZONE1_set1']['erfblock']['res']
        var=pd.DataFrame(var) #Convert to dataframe
        var=var.rename(columns={0:'Phase 1',1:'Phase 2',2:'Phase 3',3:'Phase 4',4:'Phase 5',5:'Phase 6'}) #rename columns
        var_sec=var.loc[ind_sec]

    if parameter=='stress_final': #Stresses of nodes
        var=node_path_final['STRESSES_NOD']['ZONE1_set1']['erfblock']['res']
        var=pd.DataFrame(var) #Convert to dataframe
        var=var.rename(columns={0:'XX',1:'YY',2:'ZZ',3:'XY',4:'XZ',5:'YZ'}) #rename columns
        var_sec=var.loc[ind_sec]

    if parameter=='plast_equiv_final': #Plastic strains of nodes
        var=node_path_final['TOTAL_PLAST_STRAINS_NOD']['ZONE1_set1']['erfblock']['res']
        var=pd.DataFrame(var) #Convert to dataframe
        var=var.rename(columns={0:'XX',1:'YY',2:'ZZ',3:'XY',4:'XZ',5:'YZ'}) #rename columns
        var=var.loc[ind_sec] #variable values of cross section
        #Equivalent plastic strain (add new colum to existing plast dataframe)
        var['EQV']=(2**0.5/3)*np.sqrt((var['XX']-var['YY'])**2+(var['YY']-var['ZZ'])**2+(var['ZZ']-var['XX'])**2+6*(var['XY']**2+var['XZ']**2+var['YZ']**2))
        var_sec=var

    print('Imported variables')
    
    return var_sec