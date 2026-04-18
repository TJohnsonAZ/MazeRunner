# This file contains search algorithms and utility functions to support them
from graph_utils import BREADTH_FIRST, DEPTH_FIRST, END, START, Node, draw_edge


"""
Uses bi-directional depth-first, breadth-first, or A* search to traverse the maze from start to finish.
Bi-directional search maintains two trees, one starting from maze start and the other from maze goal.
Success is determined by the detection of a frontier overlap in both trees.
Optional verbose printing allows visible output of each traversal step.

Parameters
----------
edges : 
    List of all Edges between Nodes for inserting children to search tree
node_map :
    2D list of all Nodes in the maze to be traversed during search.
start :
    Node object for first tree to begin search from.
end :
    Node object for second tree to begin search from.
search_type:
    Integer constant indicating the search algorithm to use.
verbose :
    Boolean flag to enable or disable verbose printing.

Returns
-------
:
    Node object of intersect point with parent trees leading back to maze start and goal.
"""
def bi_directional_search(edges: dict[str, list[str]], node_map: list[list[Node]], start: Node, end: Node, search_type: int, verbose: bool) -> Node:
    # initialize data structures
    start_frontier: list[Node] = []
    start_explored: list[str] = []
    end_frontier: list[Node] = []
    end_explored: list[str] = []

    # insert first node to frontiers
    start_frontier.append(start)
    end_frontier.append(end)

    print("\nExploring from " + start.label + " and " + end.label, end="")

    turn = START

    # loop while frontiers not empty
    while len(start_frontier) != 0 and len(end_frontier) != 0:
        # check for start search's turn
        if turn == START:
            # get current node from frontier
            current = start_frontier[0]
            if verbose:
                print("\n\nstart search exploring node: " + current.label, end="")
            
            # check for frontier intersection and return
            if current in end_frontier:
                print("\n\nfrontier intersection detected at " + current.label)
                return current

            # move current element from frontier to explored
            start_frontier.remove(current)
            start_explored.append(current.label)

            new_children = find_children(node_map, edges, current, start_explored)
        
        else:
            # get current node from frontier
            current = end_frontier[0]
            if verbose:
                print("\n\nend search exploring node: " + current.label, end="")

            # check for frontier intersection and return
            if current in start_frontier:
                print("\n\nfrontier intersection detected at " + current.label)
                return current

            # move current element from frontier to explored
            end_frontier.remove(current)
            end_explored.append(current.label)

            # find children of current node
            new_children = find_children(node_map, edges, current, end_explored)

            
        if search_type == DEPTH_FIRST:
            new_children.reverse()

        # insert children to frontier
        if len(new_children) > 0:
            if verbose:
                print("\ninserting new children: ", end="")

            for child in new_children:
                if turn == START:
                    child.set_parent(current, START)
                    if verbose:
                        print(child.label + " ", end="")
 
                    # insert in position appropriate for algorithm
                    if search_type == DEPTH_FIRST:
                        start_frontier.insert(0, child)
                    elif search_type == BREADTH_FIRST:
                        start_frontier.append(child)
                    # not yet implemented
                    else:
                        start_frontier.insert(0, child)
                        
                else:
                    child.set_parent(current, END)
                    if verbose:
                        print(child.label + " ", end="")

                    # insert in position appropriate for algorithm
                    if search_type == DEPTH_FIRST:
                        end_frontier.insert(0, child)
                    elif search_type == BREADTH_FIRST:
                        end_frontier.append(child)
                    # not yet implemented
                    else:
                        end_frontier.insert(0, child)
                    
        if turn == START:
            if verbose:
                print("\ncurrent frontier from start: ", end="")
                for node in start_frontier:
                    print(node.label + " ", end="")

            # recolor the newly traversed edge
            if start_frontier[0].parent:
                draw_edge(start_frontier[0], start_frontier[0].parent, 'from_start')
        
        else:
            if verbose:
                print("\ncurrent frontier from end: ", end="")
                for node in end_frontier:
                    print(node.label + " ", end="")

            # recolor the newly traversed edge
            if end_frontier[0].end_parent:
                draw_edge(end_frontier[0], end_frontier[0].end_parent, 'from_end')

        # change turn
        turn = not turn

    raise Exception("Intersection not found.")


"""
Finds and returns any children of a given Node. Children are Nodes that:
- Are connected to the given node by an edge
- Have not already been explored

Parameters
----------
node_map : 
    2D list of all Nodes.
edges :
    List of all Edges.
current_node :
    Node object to check for children of.
explored :
    List of strings containing labels of Nodes that have been explored.

Returns
-------
:
    List of Nodes containing the current Node's children (if any).
"""
def find_children(node_map: list[list[Node]], edges: dict[str, list[str]], current_node: Node, explored: list[str]) -> list[Node]:
    new_children: list[Node] = []

    for child_name in edges[current_node.label]:
        if child_name not in explored:
            child = find_node(node_map, child_name)

            # insert new nodes into alphabetically sorted list
            insert_index = 0
            while child and insert_index <= len(new_children):
                if insert_index == len(new_children):
                    new_children.append(child)
                    child = None
                elif child.label < new_children[insert_index].label:
                    new_children.insert(insert_index, child)
                    child = None

                insert_index += 1

    return new_children


"""
Finds and returns a Node in the node map given its label.

Parameters
----------
node_map :
    2D list of all Nodes.
node_label :
    Label of Node to be found.

Returns
-------
:
    Node object in map with specified label, or None if not found.
"""
def find_node(node_map: list[list[Node]], node_label: str) -> Node | None:
    for out_index in range(0, len(node_map)):
        for in_index in range(0, len(node_map[0])):
            if (node_map[out_index][in_index].label == node_label):
                return node_map[out_index][in_index]

    return None


"""
Uses depth-first, breadth-first, or A* search to traverse the maze from start to finish.
Optional verbose printing allows visible output of each traversal step.

Parameters
----------
edges : 
    List of all Edges between Nodes for inserting children to search tree
node_map :
    2D list of all Nodes in the maze to be traversed during search.
start :
    Node object to begin search from.
end :
    Node object to search for.
search_type:
    Integer constant indicating the search algorithm to use.
verbose :
    Boolean flag to enable or disable verbose printing.

Returns
-------
:
    Node object of found goal node with parent tree leading back to maze start.
"""
def search(edges: dict[str, list[str]], node_map: list[list[Node]], start: Node, end: Node, search_type: int, verbose: bool) -> Node:
    # initialize data structures
    frontier: list[Node] = []
    explored: list[str] = []

    # insert first node to frontier
    frontier.append(start)

    print("\nExploring from " + start.label + " to " + end.label, end="")

    # loop while frontier not empty
    while len(frontier) != 0:
        current = frontier[0]
        if verbose:
            print("\n\nexploring node: " + current.label, end="")

        # return goal if found
        if current.label == end.label:
            return current

        # move current element from frontier to explored
        frontier.remove(current)
        explored.append(current.label)

        # find children of current node
        new_children = find_children(node_map, edges, current, explored)

        if search_type == DEPTH_FIRST:
            new_children.reverse()

        # insert new children to frontier
        if len(new_children) > 0:
            if verbose:
                print("\ninserting new children: ", end="")

            for child in new_children:
                if verbose:
                    print(child.label + " ", end="")
                child.set_parent(current, START)

                # insert in position appropriate for algorithm
                if search_type == DEPTH_FIRST:
                    frontier.insert(0, child)
                elif search_type == BREADTH_FIRST:
                    frontier.append(child)
                # not yet implemented
                else:
                    frontier.insert(0, child)

        if verbose:
            print("\ncurrent frontier: ", end="")
            for node in frontier:
                print(node.label + " ", end="")

        # recolor the newly traversed edge
        if frontier[0].parent:
            draw_edge(frontier[0], frontier[0].parent, 'from_start')
    
    raise Exception("Goal not found.")

