# This file contains class definitions for essential graph objects and graphing utility functions
import matplotlib.pyplot as plt  # library used to visualize and discretize the maze

from typing import Self
from PIL import Image  # used to get the color of pixels for wall detection

# constants for directional flags
START = True
END = False

# constants for search algorithm flags
DEPTH_FIRST = 0
BREADTH_FIRST = 1
A_STAR = 2

# class to keep track of individual nodes in the maze graph
class Node:
    def __init__(self, x: int, y: int, y_label: str, x_label: str):
        self._x = x
        self._y = y

        # apply unicode offset to use lowercase letters when needed
        if ord(x_label) > 90:
            _x_label = chr(ord(x_label) + 6)
        else:
            _x_label = x_label
        if ord(y_label) > 90:
            _y_label = chr(ord(y_label) + 6)
        else:
            _y_label = y_label

        self._label = _y_label + _x_label
        self._parent: Self | None = None
        self._end_parent: Self | None = None

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y and self.label == other.label
        return NotImplemented

    def set_parent(self, parent: Self, from_start: bool) -> None:
        if from_start:
            self._parent = parent
        else:
            self._end_parent = parent
    
    @property
    def label(self) -> str:
        return self._label

    @property
    def parent(self) -> Self | None:
        return self._parent

    @property
    def end_parent(self) -> Self | None:
        return self._end_parent

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    

"""Checks for the presence of a wall between two Nodes and returns the result.
Determines presence of wall by checking pixel coloration.

Parameters
----------
start_node : 
    Node whose pixel coordinates to begin check from.
end_node :
    Node whose pixel coordinates to check until.
image :
    Image object for use in color checks.

Returns
-------
:
    Boolean result of assessment.
"""
def check_wall(start_node: Node, end_node: Node, image: Image.Image) -> bool:
    wall = False

    # if points are on the same y, check for horizontal edge
    if start_node.y == end_node.y:
        index = end_node.x
        while index < start_node.x and wall is False:
            curr_pixel = image.getpixel((index, start_node.y))
            # check if pixel is black and thus a wall
            if (isinstance(curr_pixel, tuple) and curr_pixel[0] < 200):
                wall = True
            index = index + 1

    # points on the same x, check for vertical edge
    else:
        index = end_node.y
        while index < start_node.y and wall is False:
            curr_pixel = image.getpixel((start_node.x, index))
            if (isinstance(curr_pixel, tuple) and curr_pixel[0] < 200):
                wall = True
            index = index + 1

    return wall


"""
Recolors an Edge as the maze is traversed to show progress.
Also used to trace the successful path.

Parameters
----------
edges : 
    List of all Edges.
current :
    Node to match Edge to self and parent of.
edge_type :
    Type of Edge to convert found Edge to.
    connection = Node connections drawn during initial setup.
    from_start = Traversal step in a search beginning at maze start (orange).
    goal_from_start = Step in a successful path starting from maze start (green).
    from_end = Traversal step in a search beginning at maze goal (pink).
    goal_from_end = Step in a successful path starting from maze goal (magenta).
"""
def draw_edge(current_node: Node, other_node: Node, edge_type: str) -> None:
    # set color from edge_type
    if edge_type == 'connection':
        color = 'blue'
    elif edge_type == 'from_start':
        color = 'orange'
    elif edge_type == 'goal_from_start':
        color = 'green'
    elif edge_type == 'from_end':
        color = 'pink'
    elif edge_type == 'goal_from_end':
        color = 'magenta'
    else:
        raise ValueError("Invalid edge type.")

    # find edge whose labels corespond to current Node and its parent
    plt.plot((other_node.x, current_node.x), (other_node.y, current_node.y), color=color)
    if edge_type != 'connection':
        plt.pause(.1500)

# TODO: 
# - fix find_children test

"""
Finds the Node closest to a given point and returns it.
Used to find start and goal Nodes.

Parameters
----------
point : 
    Integer tuple containing coordinates to find the nearest Node to.
node_map :
    2D list of all nodes.

Returns
-------
:
    Node found to be closest to the given point.
"""
def find_closest(point: tuple[int, int], node_map: list[list[Node]]) -> Node:
    min_distance = 999
    closest_node = node_map[0][0]

    for y_index in range(0, len(node_map)):
        for x_index in range(0, len(node_map[0])):
            distance = abs(point[0] - node_map[y_index][x_index].x) + abs(point[1] - node_map[y_index][x_index].y)
            if (distance < min_distance):
                min_distance = distance
                closest_node = node_map[y_index][x_index]

    return closest_node


"""
Traces a path from maze start or goal to a specified end node.
Used to build successful traversal paths.

Parameters
----------
end_node :
    Node to trace a path to.
starting_point :
    Boolean flag indicating where the path to trace starts.
    START = Path starting from maze start.
    END = Path starting from maze goal.

Returns
-------
:
    List of Nodes representing the path from the starting point to the end node.
"""
def trace_path(end_node: Node, starting_point: bool) -> list[Node]:
    path: list[Node] = []
    current: Node | None = end_node

    # trace successful path backwards by moving up the tree
    while current:
        path.append(current)
        if starting_point == START:
            current = current.parent
        else:
            current = current.end_parent

    # reverse path so it is ordered start -> end
    path.reverse()

    return path
