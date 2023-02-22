# sysweld_plot
Plot maps of data from SYSWELD result files
# Summary 
plot_map_script.py runs all the required functions to import and plot maps of the SYSWELD result files. Required changes to the plots such as which variable to plot, which cross section to plot on, scale of the colour bar, etc., can be made in this script. The functions called by this script are listed below.
## Importing results file
import_file.py imports the required results file
## Coordinates of nodes
import_coord.py takes in a results file (output of imporrt_file) and outputs the coordinates of all the nodes
## Plotting the cross section
plot_outline.py takes the coordinates of all the nodes (output of import_coord) and picks the nodes that lie on the required cross section. The outline is plotted by picking the nodes that lie on the boundary of the cross section, and finally both the outline and nodes are plotted.
## Importing and calculating variables
import_var.py takes a results file and the indices of the required nodes (outputs of import_file and plot_outline respectively), and outputs the required variable at these particular nodes. This file currently can output the following variables: hardness, the maximum temperature, phases, stresses, and equivalent plastic strain.
## Plotting the map
plot_variable.py takes the variable's values and plots them on the cross section (outputs of import_var and plot_outline respectively). Once the map has been plotted, it is removed so that the outline can be reused for another map.

