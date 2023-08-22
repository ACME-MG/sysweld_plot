#%% Import libraries
import numpy as np
import pandas as pd
#%%
def import_var(file,sysweld_app, ind_sec, parameter, state_no = -1, pent_ele = False):
    """
    This script imports the values for the parameter on the specified cross section.

    Arguments:
        file (HDF5 group):          imported results file 
        sysweld_app (string):       application used to generate results file ('min_weld' for minimum results file from visual weld, 
                                                                        'weld' for normal results file from visual weld, or 
                                                                        'assembly' for results file from visual assembly)
        ind_sec (bool dataframe):   indices of nodes in cross section
        parameter:                  variable to import (stress, strain, hardness, phase, fusion, peeq, thermal_strain)
        state_no (int):             state number to plot, default: -1 (last state)
        pent_ele (bool):            whether model includes penta elements, default: False

    Returns:
        var_sec (dataframe):        parameter values for each node on the cross section at the state number
    """
    # app branch is 'SYSWELD' for min_weld and weld; 'CSMIMPL' for assembly
    if sysweld_app == 'min_weld' or sysweld_app == 'weld':
        app_branch = 'SYSWELD'
    elif sysweld_app == 'assembly':
        app_branch = 'CSMIMPL'

    # geo branch is 'NODE' for weld and temp for min_weld; 'HEXA8' for min_weld and assembly, unless pent_ele is True, then 'SOLID'
    if sysweld_app == 'weld' or (sysweld_app == 'min_weld' and parameter == 'fusion'):
        geo_branch = 'NODE'
    else:
        if pent_ele == True:
            geo_branch = 'SOLID'
        else:
            geo_branch = 'HEXA8'

    # path to results for parameter
    states = file[app_branch]['singlestate'].keys() # list of states
    states = list(states) # convert dict_keys to list
    plot_state = states[state_no] # state number to be plotted
    node_path = file[app_branch]['singlestate'][plot_state]['entityresults'][geo_branch] # path to node results for final states

    # nodal results for normal results from visual weld, and minimum temperature results from visual weld
    if sysweld_app == 'weld' or (sysweld_app == 'min_weld' and parameter == 'fusion'):

        def find_var(var_branch,col_name): # function to get values of parameter on cross section
            var=node_path[var_branch]['ZONE1_set1']['erfblock']['res'] # values of parameter
            var=pd.DataFrame(var) # convert to dataframe
            var_sec=var.loc[ind_sec] # values on cross section
            for i in range(len(col_name)): # name columns of cros section
                var_sec=var_sec.rename(columns={i:col_name[i]})
            return var_sec
        
        # different parameters
        if parameter=='hardness': #Hardness of nodes
            var_sec=find_var('HARDNESS_NOD',['HV'])
        elif parameter=='phase': #Fusion of nodes
            var_sec=find_var('PHASE_PROPORTIONS_NOD',['Phase 1','Phase 2','Phase 3','Phase 4','Phase 5','Phase 6'])
        elif parameter=='stress': #Stresses of nodes
            var_sec=find_var('STRESSES_NOD',['XX','YY','ZZ','XY','XZ','YZ'])
            var_sec['von'] = (1/2**0.5)*np.sqrt((var['XX']-var['YY'])**2+(var['YY']-var['ZZ'])**2+(var['ZZ']-var['XX'])**2+6*(var['XY']**2+var['XZ']**2+var['YZ']**2))
        elif parameter=='strain': #Strains of nodes
            var_sec=find_var('STRAINS_NOD',['XX','YY','ZZ','XY','XZ','YZ'])
            var_sec['EQV']=(2**0.5/3)*np.sqrt((var['XX']-var['YY'])**2+(var['YY']-var['ZZ'])**2+(var['ZZ']-var['XX'])**2+6*(var['XY']**2+var['XZ']**2+var['YZ']**2))
        elif parameter == 'fusion':
            count = 0
            for i in states: #find maximum fusion value for all states
                node_path=file[app_branch]['singlestate'][i]['entityresults'][geo_branch]
                var=node_path['TEMPERATURE_NOD']['ZONE1_set0']['erfblock']['res']
                var=pd.DataFrame(var) #Convert to dataframe
                var=var.loc[ind_sec] #variable values of cross section
                if i==states[0]: #first iteration
                    var_max=var #set var_max to initial temps
                else: #add other temps to var_max as columns
                    var_max=pd.concat([var_max,var],axis=1) 
                count+=1
                if count%1000==0:
                    print(str(count) + ' states out of ' + str(len(states)) + ' states completed')
            var_max=var_max.max(axis=1) #find max temp for each node
            var_max=pd.DataFrame(var_max) #Convert to dataframe
            var_max=var_max.rename(columns={0:'Temp'}) #rename column Temp
            var_sec=var_max

    # elemtnal results for minimum results from visual weld (except temp), and results from visual assembly
    if (sysweld_app == 'min_weld' and parameter != 'fusion') or sysweld_app == 'assembly':
        #Node IDs for each element and element IDs for hex elements
        node_id_hex=file[app_branch]['constant']['connectivities']['HEXA8']['erfblock']['ic'] #node IDs for each element
        node_id_hex=pd.DataFrame(node_id_hex) #Convert to dataframe
        ele_id_hex=file[app_branch]['constant']['connectivities']['HEXA8']['erfblock']['idele'] #element IDs
        ele_id_hex=pd.DataFrame(ele_id_hex) #Convert to dataframe
        ele_node_id_hex=pd.concat([ele_id_hex,node_id_hex],axis=1,ignore_index=True)#combine node IDs and element IDs
        if pent_ele == True:
            #Node IDs for each element and element IDs for penta elements
            node_id_penta=file[app_branch]['constant']['connectivities']['PENTA6']['erfblock']['ic']
            node_id_penta=pd.DataFrame(node_id_penta)
            ele_id_penta=file[app_branch]['constant']['connectivities']['PENTA6']['erfblock']['idele']
            ele_id_penta=pd.DataFrame(ele_id_penta)
            ele_node_id_penta=pd.concat([ele_id_penta,node_id_penta],axis=1,ignore_index=True)#combine node IDs and element IDs
            #Combine hex and penta element and node IDs 
            ele_node_id=pd.concat([ele_node_id_hex,ele_node_id_penta],axis=0,ignore_index=True)
        else:
            ele_node_id=ele_node_id_hex

        # All node IDs
        node_id=file[app_branch]['constant']['entityresults']['NODE']['COORDINATE']['ZONE1_set0']['erfblock']['entid']
        node_id=pd.DataFrame(node_id)
        node_id=node_id.rename(columns={0:'id'})

        # Node IDs on cross section
        node_id_sec=node_id.loc[ind_sec]
        node_id_sec=node_id_sec.rename(columns={0:'id'})

        def find_ele_node_id_param(col_names,param_name): #function to find parameter values for each element
            #Parameter element ids
            param_entid=node_path[param_name]['ZONE1_set0']['erfblock']['entid']
            param_entid=pd.DataFrame(param_entid)
            param_entid=param_entid.rename(columns={0:'id'})
            #Parameter results
            param_res=node_path[param_name]['ZONE1_set0']['erfblock']['res']
            param_res=pd.DataFrame(param_res)
            param_res=param_res.rename(columns=col_names) #rename columns
            #combine parameter element ids and stress results
            param_entid_res=pd.concat([param_entid,param_res],axis=1,ignore_index=True)
            #combine element node ids and stress element ids and results based on element id
            ele_node_id_param=pd.merge(ele_node_id,param_entid_res,left_on=0,right_on=0,how='left')
            return ele_node_id_param
        
        # different parameters
        if parameter == 'stress' and sysweld_app == 'min_weld': 
            ele_node_id_param = find_ele_node_id_param({0:'XX',1:'YY',2:'ZZ',3:'XY',4:'XZ',5:'YZ'},'STRESSES_ELE')
        if parameter == 'stress' and sysweld_app == 'assembly': 
            ele_node_id_param = find_ele_node_id_param({0:'XX',1:'YY',2:'ZZ',3:'XY',4:'XZ',5:'YZ'},'Stress3D')
        if parameter == 'strain' and sysweld_app == 'min_weld': 
            ele_node_id_param = find_ele_node_id_param({0:'strain'},'STRAINS_ELE')
        if parameter == 'peeq' and sysweld_app == 'assembly': 
            ele_node_id_param = find_ele_node_id_param({0:'strain'},'EPLE')
        if parameter == 'thermal_strain' and sysweld_app == 'assembly': 
            ele_node_id_param = find_ele_node_id_param({0:'strain'},'EPTH')

        def find_var_ele(sum_col_name,var_col_name): # function to average element values for each node
            """
            Arguments:
                sum_col_name (list):    list of column names for columns that hold sum of node values for each element
                var_col_name (list):    list of column names for columns that hold average of node values for each element
            """
            for i in range(len(sum_col_name)): #for each row in ele_node_id
                node_id_sec[sum_col_name[i]]=0 #add column to node_id_sec for sum of parameter values
                node_id_sec[var_col_name[i]]=0 #add column to node_id_sec for average of parameter values
            node_id_sec['count']=0 #add column to node_id_sec for number of nodes

            #for each element, if a node is in the cross section, add the parameter value of that element to the node id sum and add 1 to the count
            for i in range(len(ele_node_id_param)): #for each row in ele_node_id
                for j in range(1,9): #for each value in ele_node_id row (only in node id columns)
                    if ele_node_id_param.iloc[i,j] in node_id_sec['id'].values: #if node id is in node id's on cross section
                        for k in range(len(sum_col_name)):
                            node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],sum_col_name[k]]+= ele_node_id_param.iloc[i,k+9]
                        node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],'count']+=1 #add 1 to count
                if i%10000==0: #print progress every 10000 elements
                    print(str(i)+' elements done' )
            for i in range(len(sum_col_name)): # average element values
                node_id_sec[var_col_name[i]]=node_id_sec[sum_col_name[i]]/node_id_sec['count']
            return node_id_sec

        # different parameters
        if parameter == 'stress':
            var_sec = find_var_ele(['sum_xx','sum_yy','sum_zz'],['XX','YY','ZZ'])
        elif parameter == 'strain':
            var_sec = find_var_ele(['sum'],['strain'])

    print('Imported variables')
    
    return var_sec
