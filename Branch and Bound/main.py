# ---------------------------------------------------------------------------------------------
# Name:     main.py
# Purpose:  Uses the BNB class and read_write_TSP to find the tour and plots
#           the tour using GraphWorld
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: Dr. Jan Pearce for the branch and bound pseudocode
# Created:     11/22/15
# ---------------------------------------------------------------------------------------------

from TSP import BNB
from GraphWorld import *
from Graph import * 
from read_write_TSP import TspRW

def main():
    
    read_write = TspRW()    # create a read_write object
    read_write.read_file(raw_input('Enter file to read from: '))    # reads all the coordinates of citties from an ASCII file

    # solver is an BNB object
    solver = BNB(read_write.coordinates)
    solver.explore()    # explores all the vertex using BNB algorithm

    # write the tour in .tour ASCII file
    read_write.coordinates = solver.tour
    read_write.write_file()
    
    # The following two lines allows to switch the layout of the graph displayed
    layout = CartesianLayout(solver.tourGraph)
    # layout = RandomLayout(solver.tourGraph)
    # layout = CircleLayout(solver.tourGraph)
    # draw the graph
    gw = GraphWorld()
    gw.show_graph(solver.tourGraph, layout)
    gw.mainloop()

main()