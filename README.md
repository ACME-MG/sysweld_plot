# sysweld_plot
Plot maps of data from SYSWELD result files.
## Main Script
script.py runs all the required functions to import and plot maps of the SYSWELD result files. This should be the only script that users interact with. The parameters section can be changed to modify the plots. 

This currently can plot a cross section of the model, and a colour map of a variable on this cros section. The variables that have been coded are the fusion zone (based on max temp), phases, hardness, stresses, and peeq.

The time step to extract the variable at can be controlled by the user, however it is currently coded based on state number, e.g. the last timestep can be plotted by setting the state number to -1 (python indices).

Optionally, this script can also plot the variable values along either a horizontal or vertical line on a cross-section. Since the variable values along the line are exported to a csv, only the parameters and import of libraries sections need to be rerun. This reduces the time from not recalculating the variable values.

Note: To accommodate setting up loops, e.g. plotting different timesteps, and to reduce plotting time, the cross-section is plotted once, and the colour maps and bars are plotted on then removed from the cross-section. This leaves the cross-section plotted for the next map instead of replotting. 

The following describes the various functions used in the script.

## Importing results file
import_file.py imports the required results file
## Coordinates of nodes
import_coord.py takes in a results file (output of import_file) and outputs the coordinates of all the nodes.
## Plotting the cross section
plot_section.py takes the coordinates of all the nodes (output of import_coord) and picks the nodes that lie on the required cross section. The outline can be input using an excel file, or automatically detected from the nodes, though this is more useful when the outline is difficult to put in a list of points. The outline and nodes are both plotted and the figure is outputted.
## Importing and calculating variables
import_var.py takes a results file and the indices of the required nodes (outputs of import_file and plot_section respectively), and outputs the required variable at these particular nodes. This file currently can output the following variables: hardness, the maximum temperature, phases, stresses, and equivalent plastic strain.
## Plotting the map
plot_variable.py takes the variable's values and plots them on the cross section (outputs of import_var and plot_outline respectively). Once the map has been plotted, it is removed so that the outline can be reused for another map.
## Plotting along a line (optional)
line_on_section.py plots the line on the cross section and exports the variable values along the line to a csv. plot_variable_on_line.py plots the variable values along the line. 

