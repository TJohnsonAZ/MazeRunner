import unittest

from search import find_children, find_node
from graph_utils import Node

class Test_TestSearch(unittest.TestCase):
    def test_find_children(self):
        # connections: 
        # AA -> AB
        # AB -> AA, AB
        # BA -> AB, BB
        # BB -> AB, BA
        nodes = [[Node(0, 0, 'A', 'A'),  Node(0, 10, 'A', 'B')], [Node(10, 0, 'B', 'A'), Node(10, 10, 'B', 'B')]]
        edges = {'AA': ['AB'], 'AB': ['AA', 'BB'], 'BA': ['AB', 'BB'], 'BB': ['AB', 'BA']}
        explored = ['BB']

        # test BB, shoud return AB, BA
        BB_expected = [Node(0, 10, 'A', 'B'), Node(10, 0, 'B', 'A')]
        BB_actual = find_children(nodes, edges, nodes[1][1], explored)
        
        self.assertEqual(BB_actual, BB_expected)

        # test AB, should return AA
        AB_expected = [Node(0, 0, 'A', 'A')]
        AB_actual = find_children(nodes, edges, nodes[0][1], explored)

        self.assertEqual(AB_actual, AB_expected)

        explored.append('AB')

        # test AA, should return empty
        AA_expected = []
        AA_actual = find_children(nodes, edges, nodes[0][0], explored)

        assert len(AA_expected) == len(AA_actual) == 0
        assert AA_actual == AA_expected
        
    def test_find_node(self):
        nodes = [[Node(0, 0, 'A', 'A'),  Node(0, 10, 'A', 'B')], [Node(10, 0, 'B', 'A'), Node(10, 10, 'B', 'B')]]

        AA_expected = Node(0, 0, 'A', 'A')
        AA_actual = find_node(nodes, 'AA')
        
        self.assertEqual(AA_actual, AA_expected)

        AB_expected = Node(0, 10, 'A', 'B')
        AB_actual = find_node(nodes, 'AB')
        
        self.assertEqual(AB_actual, AB_expected)

        AC_expected = None
        AC_actual = find_node(nodes, 'AC')
        
        self.assertEqual(AC_actual, AC_expected)