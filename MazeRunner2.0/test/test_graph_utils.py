import unittest

from graph_utils import Node, find_closest, trace_path

class Test_TestGraphUtils(unittest.TestCase):
    def test_find_closest(self):
        nodes = [[Node(0, 0, 'A', 'A'),  Node(0, 10, 'A', 'B')], [Node(10, 0, 'B', 'A'), Node(10, 10, 'B', 'B')]]

        self.assertEqual(find_closest((1, 6), nodes), nodes[0][1])

        self.assertEqual(find_closest((9, 2), nodes), nodes[1][0])

        self.assertEqual(find_closest((5, 5), nodes), nodes[0][0])

        self.assertEqual(find_closest((10, 8), nodes), nodes[1][1])

    def test_trace_path(self):
        nodes = [[Node(0, 0, 'A', 'A'),  Node(0, 10, 'A', 'B')], [Node(10, 0, 'B', 'A'), Node(10, 10, 'B', 'B')]]
        # AB -> AA -> BA -> BB
        nodes[0][1].set_parent(nodes[0][0], True)
        nodes[0][0].set_parent(nodes[1][0], True)
        nodes[1][0].set_parent(nodes[1][1], True)

        # AA -> AB -> BB -> BA
        nodes[0][0].set_parent(nodes[0][1], False)
        nodes[0][1].set_parent(nodes[1][1], False)
        nodes[1][1].set_parent(nodes[1][0], False)
        
        expected_start = [Node(10, 10, 'B', 'B'), Node(10, 0, 'B', 'A'), Node(0, 0, 'A', 'A'), Node(0, 10, 'A', 'B')]
        actual_start = trace_path(nodes[0][1], True)

        self.assertEqual(actual_start, expected_start)

        expected_end = [Node(10, 0, 'B', 'A'), Node(10, 10, 'B', 'B'), Node(0, 10, 'A', 'B'), Node(0, 0, 'A', 'A')]
        actual_end = trace_path(nodes[0][0], False)
        
        self.assertEqual(actual_end, expected_end)