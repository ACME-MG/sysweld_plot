#%% Import libraries
import pandas as pd
#%%
def import_coord(file):
    """
    This script imports the coordinates of all the nodes.
    
    Required arguments:
        file: imported file
    Returns:
        coord: coordinates of nodes
    """
    #Coordinates of nodes
    coord=file['SYSWELD']['constant']['entityresults']['NODE']['COORDINATE']['ZONE1_set0']['erfblock']['res']
    coord=pd.DataFrame(coord) #Convert to dataframe
    coord=coord.rename(columns={0: 'X', 1: 'Y', 2: 'Z'}) #rename columns X,Y,Z

    return coord