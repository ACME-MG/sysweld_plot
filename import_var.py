
#%%
import numpy as np
import pandas as pd
#%%
def import_var(file,sysweld_app,parameter,ind_sec):
    """
    This script imports the values for the required variables on the specified cross section.

    Required arguments:
        file: imported file
        sysweld_app: application used to generate results file
        parameter: variable to import
        ind_sec: indices for required cross section
    Returns:
        var_sec: required variable's values
    """

    if sysweld_app=='weld':
        states=file['SYSWELD']['singlestate'].keys() #List of states
        states=list(states) #Convert dict_keys to list
        final_state=states[-1] #Final state
        node_path_final=file['SYSWELD']['singlestate'][final_state]['entityresults']['NODE'] #Path to node results for final states 

    elif sysweld_app=='assembly':

        states=file['CSMIMPL']['singlestate'].keys() #List of states
        states=list(states) #Convert dict_keys to list
        final_state=states[-1] #Final state
        node_path_final=file['CSMIMPL']['singlestate'][final_state]['entityresults']['SOLID'] #Path to element results for final states

        #Node IDs for each element and element IDs for hex elements
        node_id_hex=file['CSMIMPL']['constant']['connectivities']['HEXA8']['erfblock']['ic'] #node IDs for each element
        node_id_hex=pd.DataFrame(node_id_hex) #Convert to dataframe
        ele_id_hex=file['CSMIMPL']['constant']['connectivities']['HEXA8']['erfblock']['idele'] #element IDs
        ele_id_hex=pd.DataFrame(ele_id_hex) #Convert to dataframe
        ele_node_id_hex=pd.concat([ele_id_hex,node_id_hex],axis=1,ignore_index=True)#combine node IDs and element IDs

        #Node IDs for each element and element IDs for penta elements
        node_id_penta=file['CSMIMPL']['constant']['connectivities']['PENTA6']['erfblock']['ic']
        node_id_penta=pd.DataFrame(node_id_penta)
        ele_id_penta=file['CSMIMPL']['constant']['connectivities']['PENTA6']['erfblock']['idele']
        ele_id_penta=pd.DataFrame(ele_id_penta)
        ele_node_id_penta=pd.concat([ele_id_penta,node_id_penta],axis=1,ignore_index=True)#combine node IDs and element IDs

        #Combine hex and penta element and node IDs 
        ele_node_id=pd.concat([ele_node_id_hex,ele_node_id_penta],axis=0,ignore_index=True)

        #All node IDs
        node_id=file['CSMIMPL']['constant']['entityresults']['NODE']['COORDINATE']['ZONE1_set0']['erfblock']['entid']
        node_id=pd.DataFrame(node_id)
        node_id=node_id.rename(columns={0:'id'})

        # Node IDs on z=10
        node_id_sec=node_id.loc[ind_sec]; #only node IDs in cross section
        node_id_sec=node_id_sec.rename(columns={0:'id'})
        
        if parameter == 'inherent_stress_final': #change parameter and column names based on given parameter
            param_name = 'Stress3D'; col_names={0:'XX',1:'YY',2:'ZZ',3:'XY',4:'XZ',5:'YZ'}
        elif parameter == 'inherent_equiv_plas_strain_final':
            param_name= 'EPLE'; col_names={0:'strain'}
        elif parameter == 'inherent_thermal_strain_final':
            param_name= 'EPTH'; col_names={0:'strain'}
        else: 
            print('Please give parameter of inherent_stress_final or inherent_equiv_plas_strain_final')

        #Parameter element ids
        param_entid=node_path_final[param_name]['ZONE1_set1']['erfblock']['entid']
        param_entid=pd.DataFrame(param_entid)
        param_entid=param_entid.rename(columns={0:'id'})
        #Parameter results
        param_res=node_path_final[param_name]['ZONE1_set1']['erfblock']['res']
        param_res=pd.DataFrame(param_res)
        param_res=param_res.rename(columns=col_names) #rename columns
        #combine parameter element ids and stress results
        param_entid_res=pd.concat([param_entid,param_res],axis=1,ignore_index=True)
        #combine element node ids and stress element ids and results based on element id
        ele_node_id_param=pd.merge(ele_node_id,param_entid_res,left_on=0,right_on=0,how='left')

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
        var=var.loc[ind_sec]
        var['von']=(1/2**0.5)*np.sqrt((var['XX']-var['YY'])**2+(var['YY']-var['ZZ'])**2+(var['ZZ']-var['XX'])**2+6*(var['XY']**2+var['XZ']**2+var['YZ']**2))
        var_sec=var
    
    if parameter=='plast_equiv_final': #Plastic strains of nodes
        var=node_path_final['TOTAL_PLAST_STRAINS_NOD']['ZONE1_set1']['erfblock']['res']
        var=pd.DataFrame(var) #Convert to dataframe
        var=var.rename(columns={0:'XX',1:'YY',2:'ZZ',3:'XY',4:'XZ',5:'YZ'}) #rename columns
        var=var.loc[ind_sec] #variable values of cross section
        #Equivalent plastic strain (add new colum to existing plast dataframe)
        var['EQV']=(2**0.5/3)*np.sqrt((var['XX']-var['YY'])**2+(var['YY']-var['ZZ'])**2+(var['ZZ']-var['XX'])**2+6*(var['XY']**2+var['XZ']**2+var['YZ']**2))
        var_sec=var

    if parameter=='inherent_stress_final': #inherent stress
        #add 3 zero columns to node_id_sec
        node_id_sec['sum_xx']=0; node_id_sec['sum_yy']=0; node_id_sec['sum_zz']=0; #sum of stresses
        node_id_sec['count']=0 #number of nodes
        node_id_sec['XX']=0; node_id_sec['YY']=0; node_id_sec['ZZ']=0; #average of stresses

        #for each element, if a node is in the cross section, add the stress value of the element to the node id sum and add 1 to the count
        for i in range(len(ele_node_id_param)): #for each row in ele_node_id
            for j in range(1,9): #for each value in ele_node_id row (only in node id columns)
                if ele_node_id_param.iloc[i,j] in node_id_sec['id'].values: #if node id is in node id's on cross section
                    node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],'sum_xx']+= ele_node_id_param.iloc[i,9] #add XX stress for corresponding element to sum
                    node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],'sum_yy']+= ele_node_id_param.iloc[i,10] #add YY stress for corresponding element to sum
                    node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],'sum_zz']+= ele_node_id_param.iloc[i,11] #add ZZ stress for corresponding element to sum
                    node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],'count']+=1 #add 1 to count
            if i%10000==0: #print progress every 10000 elements
                print(str(i)+' elements done' )
        #calculate average stress
        node_id_sec['XX']=node_id_sec['sum_xx']/node_id_sec['count'] 
        node_id_sec['YY']=node_id_sec['sum_yy']/node_id_sec['count'] 
        node_id_sec['ZZ']=node_id_sec['sum_zz']/node_id_sec['count'] 
        var_sec=node_id_sec

    if parameter =='inherent_equiv_plas_strain_final' or parameter == 'inherent_thermal_strain_final': #inherent equivalent plastic strain
        #add 3 zero columns to node_id_sec
        node_id_sec['sum']=0 #sum of values
        node_id_sec['count']=0 #number of nodes
        node_id_sec['strain']=0 #average of values

        #for each element, if a node is in the cross section, add the stress value ofthe element to the node id sum and add 1 to the count
        for i in range(len(ele_node_id_param)): #for each row in ele_node_id
            for j in range(1,9): #for each value in ele_node_id row (only in node id columns)
                if ele_node_id_param.iloc[i,j] in node_id_sec['id'].values: #if node id is in node id's on cross section
                    node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],'sum']+= ele_node_id_param.iloc[i,9] #add plastic strain for corresponding element to sum
                    node_id_sec.loc[node_id_sec['id']==ele_node_id_param.iloc[i,j],'count']+=1 #add 1 to count
            if i%10000==0: #print progress every 10000 elements
                print(str(i)+' elements done' )

        #calculate average strain
        node_id_sec['strain']=node_id_sec['sum']/node_id_sec['count'] 
        var_sec=node_id_sec

    print('Imported variables')
    
    return var_sec