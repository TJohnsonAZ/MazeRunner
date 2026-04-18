# This file contains the main driver for the maze runner programer and maze setup functions
import argparse
from collections import defaultdict  # used to retrieve command-line arguments

import matplotlib.image as plotimage
import matplotlib.pyplot as plt  # library used to visualize and discretize the maze
from PIL import Image  # used to get the color of pixels for wall detection

from graph_utils import A_STAR, BREADTH_FIRST, DEPTH_FIRST, END, START, Node, check_wall, draw_edge, find_closest, trace_path
from search import bi_directional_search, search

# constants for maze file locations
SIMPLE_MAZE = 'simple_maze.png'
MODERATE_MAZE = 'moderate_maze.jpg'
DIFFICULT_MAZE = 'difficult_maze.jpg'


def main() -> None:
    # set up argument parser
    parser = argparse.ArgumentParser(
        prog='MazeRunner',
        description='AI maze solver'
    )
    parser.add_argument(
        '-s', '--size',
        type=str,
        required=True,
        help='The size of the maze to solve: \'simple\', \'moderate\', \'difficult\''
    )
    parser.add_argument(
        '-a', '--algorithm',
        type=str,
        required=True,
        help='The graph search algorithm to use in maze traversal: \'depth-first\', \'breadth-first\', \'A*\''
    )
    parser.add_argument(
        '-d', '--direction',
        type=str,
        required=True,
        help='The type of search to be conducted: \'single\', \'bi-directional\''
    )
    parser.add_argument(
        '-v', '--verbose',
        action=argparse.BooleanOptionalAction,
        required=True,
        help='verbose printing: \'--verbose\', \'--no-verbose\''
    )
    args=parser.parse_args()

    # get maze type from command-line arguments
    if str(args.size).lower() == 'simple':
        maze_type = SIMPLE_MAZE
    elif str(args.size).lower() == 'moderate':
        maze_type = MODERATE_MAZE
    elif str(args.size).lower() == 'difficult':
        maze_type = DIFFICULT_MAZE
    else:
        raise ValueError("Invalid maze. Maze options are: simple, moderate, difficult")
    
    if (str(args.algorithm).lower() == 'depth-first'):
        algorithm = DEPTH_FIRST
    elif str(args.algorithm.lower() == 'breadth-first'):
        algorithm = BREADTH_FIRST
    elif str(args.algorithm.lower() == 'a*'):
        algorithm = A_STAR
    else:
        raise ValueError("Invalid alogrithm. Options are: depth-first, breadth-first, A*")

    # get search type from command-line arguments
    if str(args.direction) == 'single':
        search_type = 'single'
    elif str(args.direction) == 'bi-directional':
        search_type = 'bi-directional'
    else:
        raise ValueError("Invalid serach type. Options are: single, bidirectional")

    # get verbose flag from arguments
    verbose: bool = args.verbose

    # name figure (currently very messy and case specific)
    fig = plt.figure(num=maze_type.lower().capitalize().replace('_m', ' M').rsplit('.', 1)[0])
    # load image
    fig.canvas.mpl_connect('close_event', handle_close)
    image = plotimage.imread(maze_type)
    plt.imshow(image)
    
    # calibrate the locations of corners, start, and end of the maze
    if maze_type == SIMPLE_MAZE:
        calibration = [(56, 95), (1232, 94), (56, 708), (126, 165), (1163, 640)]
    elif maze_type == MODERATE_MAZE:
        calibration = [(0, 0), (500, 0), (0, 500), (236, 8), (260, 480)]
    else:
        calibration = [(21, 21), (680, 21), (21, 680), (29, 382), (670, 203)]

    # generate the maze data structure
    node_map = generate_maze(maze_type, calibration)
    edges = generate_edges(maze_type, node_map)

    # find and plot start and end nodes
    start_node = find_closest(calibration[3], node_map)
    end_node = find_closest(calibration[4], node_map)
    plt.plot(start_node.x, start_node.y, marker='o', markersize=4, color='green', linestyle='-')
    plt.plot(end_node.x, end_node.y, marker='o', markersize=4, color='magenta', linestyle='-')
    plt.pause(.0001)

    # search maze from start to goal and trace path (single)
    if search_type == 'single':
        search(edges, node_map, start_node, end_node, algorithm, verbose)
        path = trace_path(end_node, START)

        # draw the successful path graphically
        for node_index in range(1, len(path)):
            draw_edge(path[node_index - 1], path[node_index], 'goal_from_start')

        # print success and final path
        print("\n\nGoal " + end_node.label + " reached with path: ", end="")
        for node in path:
            print(node.label + " ", end="")
        print()

    # search maze from start to goal and trace path (bidirectional)
    else:
        intersect_node = bi_directional_search(edges, node_map, start_node, end_node, algorithm, verbose)

        path_from_start = trace_path(intersect_node, START)
        path_from_end = trace_path(intersect_node, END)

        # draw the successful path graphically
        for node_index in range(1, len(path_from_start)):
            draw_edge(path_from_start[node_index - 1], path_from_start[node_index], 'goal_from_start')

        for node_index in range(1, len(path_from_end)):
            draw_edge(path_from_end[node_index - 1], path_from_end[node_index], 'goal_from_end')

        # print success and final path
        print("\npath from start: ", end="")
        for node in path_from_start:
            print(node.label + " ", end="")
        print()

        print("\npath from end: ", end="")
        for node in path_from_end:
            print(node.label + " ", end="")
        print()

    input("\nExecution complete. Press enter to exit...")


"""
Generates a list of Edges to connect Nodes not separated by a wall.

Parameters
----------
maze_type : 
    String constant indicating which maze image to map.
node_map :
    2D list of Nodes representing points to be traversed in the maze.

Returns
-------
:
    A list of Edges indicating which Nodes are connected to each other (no wall between them).
"""
def generate_edges(maze_type: str, node_map: list[list[Node]]):
    maze_image = Image.open(maze_type)
    image_RGB = maze_image.convert("RGB")
    edges = defaultdict(list[str])

    for y_index in range(len(node_map)):
        for x_index in range(len(node_map[y_index])):
            curr_node = node_map[y_index][x_index]
            left_node = node_map[y_index][x_index - 1]
            top_node = node_map[y_index - 1][x_index]

            # check for an edge with the node to the left
            if x_index != 0 and not check_wall(curr_node, left_node, image_RGB):
                edges[left_node.label].append(curr_node.label)
                edges[curr_node.label].append(left_node.label)
                draw_edge(left_node, curr_node, 'connection')

            # check for an edge with the node above
            if y_index != 0 and not check_wall(curr_node, top_node, image_RGB):
                edges[top_node.label].append(curr_node.label)
                edges[curr_node.label].append(top_node.label)
                draw_edge(top_node, curr_node, 'connection')
        
    return edges


"""
Generates an nxm grid of Node objects for use in maze traversal.
Grid is adjusted based on maze size and pixel distance between Nodes.

Parameters
----------
maze_type : 
    String constant indicating which maze image to map.
calibration :
    List of integer tuples containing coordinates to maze edges and start and end points.

Returns
-------
:
    A 2D list of Nodes representing points to be traversed in the maze.
"""
def generate_maze(maze_type: str, calibration: list[tuple[int, int]]) -> list[list[Node]]:
    # determine number vertical and horizontal nodes in the maze (and plot offsets) based on its size
    if maze_type == SIMPLE_MAZE:
        num_horizontal = 10
        num_vertical = 5
        v_offset = 25
        h_offset = 0
    elif maze_type == MODERATE_MAZE:
        num_horizontal = 20
        num_vertical = 20
        v_offset = -12
        h_offset = -12
    else:
        num_horizontal = 30
        num_vertical = 30
        v_offset = 10
        h_offset = 10

    # initialize loop variables
    x_difference = (calibration[1][0] - calibration[0][0]) / num_horizontal
    y_difference = (calibration[2][1] - calibration[0][1]) / num_vertical

    curr_y = 0.0
    node_map: list[list[Node]] = []

    # generate and plot all nodes and edges
    for y_index in range(0, num_vertical):
        curr_y += y_difference
        curr_x = 0.0
        curr_row: list[Node] = []
        for x_index in range(0, num_horizontal):
            curr_x += x_difference

            # create and plot new node
            new_node = Node(int(curr_x + h_offset), int(curr_y + v_offset), chr(y_index + 65), chr(x_index + 65))
            plt.plot(new_node.x, new_node.y, marker='o', markersize=4, color='crimson', linestyle='-')

            curr_row.append(new_node)
        node_map.append(curr_row)

    return node_map


# event handler to end program if figure closed
def handle_close(evt):
    plt.close()
    raise KeyboardInterrupt("Figure closed, shutting down...")


if __name__ == '__main__':
    main()