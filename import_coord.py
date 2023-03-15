#%% Import libraries
import pandas as pd
#%%
def import_coord(file,sysweld_app):
    """
    This script imports the coordinates of all the nodes.
    
    Required arguments:
        file: imported file
        sysweld_app: application used to generate results file
    Returns:
        coord: coordinates of nodes
    """
    #Coordinates of nodes
    if sysweld_app=='weld':#Choose path to coordinates in results file 
        coord=file['SYSWELD']['constant']['entityresults']['NODE']['COORDINATE']['ZONE1_set0']['erfblock']['res']
    elif sysweld_app=='assembly':
        coord=file['CSMIMPL']['constant']['entityresults']['NODE']['COORDINATE']['ZONE1_set0']['erfblock']['res']
    else:
        print('Please choose weld or assembly')

    coord=pd.DataFrame(coord) #Convert to dataframe
    coord=coord.rename(columns={0: 'X', 1: 'Y', 2: 'Z'}) #rename columns X,Y,Z

    return coord