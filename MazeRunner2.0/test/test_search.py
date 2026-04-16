import unittest

from search import find_children, find_node
from graph_utils import Edge, Node

class Test_TestSearch(unittest.TestCase):
    def test_find_children(self):
        nodes = [[Node(0, 0, 'A', 'A'),  Node(0, 10, 'A', 'B')], [Node(10, 0, 'B', 'A'), Node(10, 10, 'B', 'B')]]

        explored = ['BB']

        BB_expected = [Node(10, 0, 'B', 'A'), Node(0, 10, 'A', 'B')]
        BB_actual = find_children(nodes, [Edge('AA', 'AB', (0, 0), (0, 10)), Edge('AB', 'BB', (0, 10), (10, 10)), Edge('BA', 'BB', (10, 0), (10, 10))], nodes[1][1], explored)
        
        self.assertEqual(BB_actual, BB_expected)

        AB_expected = [Node(0, 0, 'A', 'A')]
        AB_actual = find_children(nodes, [Edge('AA', 'AB', (0, 0), (0, 10)), Edge('AB', 'BB', (0, 10), (10, 10)), Edge('BA', 'BB', (10, 0), (10, 10))], nodes[0][1], explored)

        self.assertEqual(AB_actual, AB_expected)

        explored.append('AB')

        AA_expected = []
        AA_actual = find_children(nodes, [Edge('AA', 'AB', (0, 0), (0, 10)), Edge('AB', 'BB', (0, 10), (10, 10)), Edge('BA', 'BB', (10, 0), (10, 10))], nodes[0][0], explored)

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