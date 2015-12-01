# ---------------------------------------------------------------------------------------------
# Name:     TSP.py
# Purpose:  Test suite for BNB and TspRW class
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: None
# Created:     11/22/15
# ---------------------------------------------------------------------------------------------

import sys
import unittest
from math import sqrt
from TSP import BNB
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
    v1 = Vertex('1')
    v1.pos = (1, 0)
    v2 = Vertex('2')
    v2.pos = (0, 1)
    rw = TspRW()
    A = BNB([v1, v2])

    print ('Testing read_file in TspRW class..')
    rw.read_file('tsp-test.tsp')
    test(rw.header == ['NAME: tsp-test.tsp\n',
    'COMMENT: agarwali and ramax. 6 vertices. Note that vertex 1 is at (1, 5); vertex 2 is at (3, 7), etc.\n',
                       'TYPE: TSP\n', 'DIMENSION: 6\n', 'EDGE_WEIGHT_TYPE: EUC_2D\n', 'NODE_COORD_SECTION\n'])
    test(rw.coordinates == [v1, v2])
    
    print('Testing explore in BNB class.. ')
    A.explore()
    test(A.tour == [v1, v2])
    
    print ('Testing chop in BNB class.. ')
    test(A.chop() == None)
    
    print('Testing distance in BNB class..')
    test (A.distance(v1, v2) == sqrt(2))

    print('Testing compute_bound in BNB class..')
    test(A.compute_bound(v2) == float('inf'))  # resets self.best_tour to an empty graph containing vertices
    
    
main()