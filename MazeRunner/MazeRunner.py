import argparse  # used to retrieve command-line arguments

import matplotlib.image as plotimage
import matplotlib.pyplot as pyplot  # library used to visualize and discretize the maze
import PIL.Image  # used to get the color of pixels for wall detection

from GraphUtils import Edge, Node

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
        '-d', '--direction',
        type=str,
        required=True,
        help='The type of search to be conducted: \'single\', \'bidirectional\''
    )
    parser.add_argument(
        '-v', '--verbose',
        action=argparse.BooleanOptionalAction,
        required=True,
        help='verbose printing: \'--verbose\', \'--no-verbose\''
    )
    args=parser.parse_args()

    # get maze type from command-line arguments
    if str(args.size) == 'simple':
        mazeType = SIMPLE_MAZE
    elif str(args.size) == 'moderate':
        mazeType = MODERATE_MAZE
    else:
        mazeType = DIFFICULT_MAZE

    # get search type from command-line arguments
    if str(args.direction) == 'single':
        searchType = 'single'
    else:
        searchType = 'bi-directional'

    # get verbose flag from arguments
    verbose = args.verbose

    # load image
    image = plotimage.imread(mazeType)
    pyplot.imshow(image)

    # get input on the locations of corners, start, and end of the maze
    inData = pyplot.ginput(5)

    # generate the maze data structure
    edges = []
    nodeMap = generateMaze(mazeType, edges, inData)

    # find and plot start and end nodes
    startNode = findClosest(inData[3], nodeMap)
    endNode = findClosest(inData[4], nodeMap)
    pyplot.plot(startNode.x, startNode.y, marker='o', markersize=4, color='green', linestyle='-')
    pyplot.plot(endNode.x, endNode.y, marker='o', markersize=4, color='magenta', linestyle='-')
    pyplot.pause(.0001)

    # search maze from start to goal and trace path (single)
    if searchType == 'single':
        search(edges, nodeMap, startNode, endNode.label, verbose)
        path = tracePath(endNode, 1)

        # draw the successful path graphically
        for index in range(1, len(path)):
            drawEdge(edges, path[index], 'finished')

        # print success and final path
        print("\n\nGoal " + endNode.label + " reached with path: ", end="")
        for index in path:
            print(index.label + " ", end="")
        print()

    # search maze from start to goal and trace path (bidirectional)
    else:
        intersectNode = biDirectionalSearch(edges, nodeMap, startNode, endNode, verbose)

        path1 = tracePath(intersectNode, 1)
        path2 = tracePath(intersectNode, 2)

        # draw the successful path graphically
        for index in range(1, len(path1)):
            drawEdge(edges, path1[index], 'finished')

        for index in range(1, len(path2)):
            drawEdge(edges, path2[index], 'finished2')

        # print success and final path
        print("\npath from start: ", end="")
        for index in path1:
            print(index.label + " ", end="")
        print()

        print("\npath from end: ", end="")
        for index in path2:
            print(index.label + " ", end="")
        print()

    pyplot.show()

def generateMaze(mazeType: str, edges: list, inData: list) -> list:
    # determine number vertical and horizontal nodes in the maze (and plot offsets) based on its size
    if mazeType == SIMPLE_MAZE:
        numHorizontal = 10
        numVertical = 5
        vOffset = 25
        hOffset = 0
    elif mazeType == MODERATE_MAZE:
        numHorizontal = 20
        numVertical = 20
        vOffset = -12
        hOffset = -12
    else:
        numHorizontal = 30
        numVertical = 30
        vOffset = 10
        hOffset = 10

    # initialize loop variables
    x_difference = (inData[1][0] - inData[0][0]) / numHorizontal
    y_difference = (inData[2][1] - inData[0][1]) / numVertical
    curr_y = 0.0
    nodeMap = []
    PIL_image = PIL.Image.open(mazeType)
    image_RGB = PIL_image.convert("RGB")

    # generate and plot all nodes and edges
    for outIndex in range(0, numVertical):
        curr_y += y_difference
        curr_x = 0.0
        currRow = []
        for inIndex in range(0, numHorizontal):
            curr_x += x_difference

            # create and plot new node
            newNode = Node(curr_x + hOffset, curr_y + vOffset, chr(outIndex + 65), chr(inIndex + 65))
            pyplot.plot(newNode.x, newNode.y, marker='o', markersize=4, color='crimson', linestyle='-')

            # check for an edge with the node to the left
            if inIndex != 0 and not checkWall(newNode, currRow[inIndex - 1], image_RGB):
                edges.append(Edge(currRow[inIndex - 1].label, newNode.label, (currRow[inIndex - 1].x, newNode.x),
                                  (currRow[inIndex - 1].y, newNode.y)))
                pyplot.plot([currRow[inIndex - 1].x, newNode.x], [currRow[inIndex - 1].y, newNode.y], color='blue')

            # check for an edge with the node above
            if outIndex != 0 and not checkWall(newNode, nodeMap[outIndex - 1][inIndex], image_RGB):
                edges.append(Edge(nodeMap[outIndex - 1][inIndex].label, newNode.label,
                                  (nodeMap[outIndex - 1][inIndex].x, newNode.x), (nodeMap[outIndex - 1][inIndex].y, newNode.y)))
                pyplot.plot([nodeMap[outIndex - 1][inIndex].x, newNode.x], [nodeMap[outIndex - 1][inIndex].y, newNode.y],
                            color = 'blue')

            currRow.append(newNode)
        nodeMap.append(currRow)

    return nodeMap

# checks for the presence of a wall between two points and returns the result
def checkWall(node1: Node, node2: Node, image) -> bool:
    wall = False
    # if points are on the same y, check for horizontal edge
    if int(node1.y - node2.y) == 0:
        for index in range(int(node2.x), int(node1.x)):
            if (image.getpixel((index, node1.y))[0] < 200):
                wall = True
                break

    # otherwise, assume points on the same x, check for vertical edge
    else:
        for index in range(int(node2.y), int(node1.y)):
            if (image.getpixel((node1.x, index))[0] < 200):
                wall = True
                break

    return wall

# finds the node closest to a given point and returns it (used for start and goal)
def findClosest(point: tuple, nodes: list) -> Node:
    minimum = 999
    minNode = nodes[0][0]
    for outIndex in range(0, len(nodes)):
        for inIndex in range(0, len(nodes[0])):
            distance = abs(point[0] - nodes[outIndex][inIndex].x) + abs(point[1] - nodes[outIndex][inIndex].y)
            if (distance < minimum):
                minimum = distance
                minNode = nodes[outIndex][inIndex]

    return minNode

# uses depth-first search to traverse the maze from start to finish
def search(edges: list, nodeMap: list, start: Node, end: str, verbose: bool) -> None:
    frontier = []
    explored = []

    # insert first node to frontier
    frontier.append(start)

    print("\nExploring from " + start.label + " to " + end, end="")

    # loop while frontier not empty
    while len(frontier) != 0:
        current = frontier[0]
        if verbose:
            print("\n\nexploring node: " + current.label, end="")

        # return goal if found
        if current.label == end:
            return current

        # move current element from frontier to explored
        frontier.remove(current)
        explored.append(current.label)

        # find children of current node
        newChildren = []
        newNode = Node(0, 0, 'X', 'X')
        for index in edges:
            insert = False
            if index.label1 == current.label and index.label2 not in explored:
                newNode = findNode(nodeMap, index.label2)
                insert = True
            elif index.label2 == current.label and index.label1 not in explored:
                newNode = findNode(nodeMap, index.label1)
                insert = True

            insertIndex = 0
            while insert and insertIndex < len(newChildren):
                if newNode.label < newChildren[insertIndex].label:
                    newChildren.insert(insertIndex, newNode)
                    insert = False

                insertIndex += 1

            if insertIndex == len(newChildren) and insert:
                newChildren.append(newNode)


        # insert children to frontier
        newChildren.reverse()
        if len(newChildren) > 0:
            if verbose:
                print("\ninserting new children: ", end="")
        for index in newChildren:
            if verbose:
                print(index.label + " ", end="")
            index.setParent(current, 1)
            frontier.insert(0, index)

        if verbose:
            print("\ncurrent frontier: ", end="")
            for index in frontier:
                print(index.label + " ", end="")

        # recolor the newly traversed edge
        drawEdge(edges, frontier[0], 'single')

# uses bi-directional depth-first search to find an intersection in the frontiers of each search
def biDirectionalSearch(edges: list, nodeMap: list, start: Node, end: Node, verbose: bool) -> None:
    frontier1 = []
    explored1 = []
    frontier2 = []
    explored2 = []

    # insert first node to frontiers
    frontier1.append(start)
    frontier2.append(end)

    print("\nExploring from " + start.label + " and " + end.label, end="")
    turn = 1

    # loop while frontiers not empty
    while len(frontier1) != 0 and len(frontier2) != 0:
        # check for start search's turn
        if turn == 1:
            # get current node from frontier
            startCurrent = frontier1[0]
            if verbose:
                print("\n\nstart search exploring node: " + startCurrent.label, end="")
            if startCurrent in frontier2:
                print("\n\nfrontier intersection detected at " + startCurrent.label)
                return startCurrent

            # move current element from frontier to explored
            frontier1.remove(startCurrent)
            explored1.append(startCurrent.label)

            # find children of current node
            newChildren = []
            newNode = Node(0, 0, 'X', 'X')
            for index in edges:
                insert = False
                if index.label1 == startCurrent.label and index.label2 not in explored1:
                    newNode = findNode(nodeMap, index.label2)
                    insert = True
                elif index.label2 == startCurrent.label and index.label1 not in explored1:
                    newNode = findNode(nodeMap, index.label1)
                    insert = True

                insertIndex = 0
                while insert and insertIndex < len(newChildren):
                    if newNode.label < newChildren[insertIndex].label:
                        newChildren.insert(insertIndex, newNode)
                        insert = False

                    insertIndex += 1

                if insertIndex == len(newChildren) and insert:
                    newChildren.append(newNode)

            # insert children to frontier
            newChildren.reverse()
            if len(newChildren) > 0:
                if verbose:
                    print("\nstart search inserting new children: ", end="")
                for index in newChildren:
                    if verbose:
                        print(index.label + " ", end="")
                    index.setParent(startCurrent, 1)
                    frontier1.insert(0, index)

            if verbose:
                print("\ncurrent frontier from start: ", end="")
                for index in frontier1:
                    print(index.label + " ", end="")

            # recolor the newly traversed edge
            drawEdge(edges, frontier1[0], 'single')

            turn = 2

        # end search's turn
        else:
            # get current node from frontier
            endCurrent = frontier2[0]
            if verbose:
                print("\n\nend search exploring node: " + endCurrent.label, end="")
            if endCurrent in frontier1:
                print("\n\nfrontier intersection detected at " + endCurrent.label)
                return endCurrent

            # move current element from frontier to explored
            frontier2.remove(endCurrent)
            explored2.append(endCurrent.label)

            # find children of current node
            newChildren = []
            newNode = Node(0, 0, 'X', 'X')
            for index in edges:
                insert = False
                if index.label1 == endCurrent.label and index.label2 not in explored2:
                    newNode = findNode(nodeMap, index.label2)
                    insert = True
                elif index.label2 == endCurrent.label and index.label1 not in explored2:
                    newNode = findNode(nodeMap, index.label1)
                    insert = True

                insertIndex = 0
                while insert and insertIndex < len(newChildren):
                    if newNode.label < newChildren[insertIndex].label:
                        newChildren.insert(insertIndex, newNode)
                        insert = False

                    insertIndex += 1

                if insertIndex == len(newChildren) and insert:
                    newChildren.append(newNode)

            # insert children to frontier
            if len(newChildren) > 0:
                if verbose:
                    print("\nend search inserting new children: ", end="")
                for index in newChildren:
                    if verbose:
                        print(index.label + " ", end="")
                    index.setParent(endCurrent, 2)
                    frontier2.insert(0, index)

            if verbose:
                print("\ncurrent frontier from end: ", end="")
                for index in frontier2:
                    print(index.label + " ", end="")

            # recolor the newly traversed edge
            drawEdge(edges, frontier2[0], 'bi')

            turn = 1

# recolors an edge as the maze is traversed to show progress (also used to trace the successful path)
def drawEdge(edges: list, current: Node, color: str) -> None:
    if color == 'single':
        col = 'orange'
    elif color == 'finished':
        col = 'green'
    elif color == 'bi':
        col = 'pink'
    else:
        col = 'magenta'

    if color == 'single' or color == 'finished':
        for index in edges:
            if (index.label1 == current.label and index.label2 == current.parent.label) \
            or (index.label1 == current.parent.label and index.label2 == current.label):
                pyplot.plot(index.coords1, index.coords2, color=col)
                pyplot.pause(.0001)
                break
    else:
        for index in edges:
            if (index.label1 == current.label and index.label2 == current.parent2.label) \
            or (index.label1 == current.parent2.label and index.label2 == current.label):
                pyplot.plot(index.coords1, index.coords2, color=col)
                pyplot.pause(.0001)
                break

# finds a node in the node map given its label
def findNode(nodeMap: list, node: Node) -> Node:
    foundNode = Node(0, 0, 'X', 'X')
    for outIndex in range(0, len(nodeMap)):
        for inIndex in range(0, len(nodeMap[0])):
            if (nodeMap[outIndex][inIndex].label == node):
                foundNode = nodeMap[outIndex][inIndex]

    return foundNode

# traces the successful path backwards from goal to start
def tracePath(endNode: Node, num: int) -> list:
    path = []
    current = endNode
    while current is not None:
        path.append(current)
        if num == 1:
            current = current.parent
        else:
            current = current.parent2

    path.reverse()

    return path

main()
