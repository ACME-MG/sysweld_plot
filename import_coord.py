#%% Import libraries
import pandas as pd
#%%
def import_coord(file, sysweld_app):
    """
    This script puts the coordinates of all the nodes into a dataframe.
    
    Required arguments:
        file (HDF5 group):      imported results file
        sysweld_app (string):   application used to generate results file ('min_weld' for minimum results file from visual weld, 
                                                                        'weld' for normal results file from visual weld, or 
                                                                        'assembly' for results file from visual assembly)
    Returns:
        coord (dataframe):      coordinates of nodes (columns: X,Y,Z)
    """
    # Path to coordinates
    if sysweld_app == 'min_weld' or sysweld_app == 'weld':
        coord = file['SYSWELD']['constant']['entityresults']['NODE']['COORDINATE']['ZONE1_set0']['erfblock']['res']
    elif sysweld_app == 'assembly':
        coord = file['CSMIMPL']['constant']['entityresults']['NODE']['COORDINATE']['ZONE1_set0']['erfblock']['res']
    else:
        print('Please choose "min_weld", "weld", or "assembly"')

    # Convert to dataframe
    coord = pd.DataFrame(coord) #Convert to dataframe
    coord = coord.rename(columns={0: 'X', 1: 'Y', 2: 'Z'}) #rename columns X,Y,Z

    return coord
