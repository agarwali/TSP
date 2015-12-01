
import sys
import unittest
import math
from nearest_neighbour import Nearest_Neighbour
from read_write_TSP import TspRW
from Graph import *

def test(did_pass):
    """  Print the result of a test.  """
    linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
    if did_pass:
        msg = "Test at line {0} ok.".format(linenum)
    else:
        msg = ("Test at line {0} FAILED.".format(linenum))
    print(msg)


def main():
    rw = TspRW()
    A = Nearest_Neighbour(['1', '2'], [(1, 0), (0, 1)])

    print ('Testing read_file in TspRW class..')
    rw.read_file('tsp-test.tsp')
    test(rw.header == ['NAME: tsp-test.tsp\n',
                       'COMMENT: agarwali and ramax. 6 vertices. Note that vertex 1 is at (1, 5); vertex 2 is at (3, 7), etc.\n',
                       'TYPE: TSP\n', 'DIMENSION: 6\n', 'EDGE_WEIGHT_TYPE: EUC_2D\n', 'NODE_COORD_SECTION\n'])
    test(rw.coordinates == [(1, 0), (0, 1)])
    test(rw.labels == ['1', '2'])

    print('Testing mark_unvisited_cities ..')
    A.mark_unvisited_cities()
    test(A.coordinates ==  [(1, 0), (0, 1)] )
    test(A.vertices == [Vertex('1'), Vertex('2')])

    print('Testing empty_tour ..')
    A.empty_tour()
    test(A.best_tour == Graph(A.vertices))  # resets self.best_tour to an empty graph containing vertices
    test(A.best_label == [])  # empties self.best_label
    test(A.best_coordinates ==[])   # epmties self.best_coordinates
    
    A.startcity = A.vertices[0]    # set the city to start city
    A.currentcity = A.startcity 
    
    print('Testing mark_visited ..')    
    A.mark_visited()
    test(A.currentcity_coordinate == (1,0))   # gets the coordinate for current city before removing it from the list
    test(A.vertices == [Vertex('2')])    # removes the vertex of current city from the self.vertices
    test(A.coordinates == [(0, 1)])# removes the cooordinate of current city from self.coordinates
    test(A.best_label == ['1']) # adds the current cities label to the best_label
    test(A.best_coordinates == [(1,0)])# adds the current city to the list of best_coordinates
    
    print('Testing calculate_nearneighbor ..')
    A.calculate_nearneighbor()
    test(A.cost_to_nearest_city == 2**0.5)    # if distance is less the update cost 
    test(A.nearestcity == Vertex('2'))     # upade nearest city
                

    print ('Testing add_currcity_tour..')
    A.add_currcity_tour()
    test(A.best_tour.__str__() == "Graph([Vertex('2'), Vertex('1')], set([Edge(Vertex('1'), Vertex('2'))]))")

    print('Testing add_tourCost ..')
    A.add_tourCost()
    test(A.cost_of_tour == 2**0.5)
    
main()