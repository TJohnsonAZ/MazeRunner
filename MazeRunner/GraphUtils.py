# class to keep track of individual nodes in the maze graph
class Node:
    def __init__(self, x: int, y: int, y_label: str, x_label: str):
        self._x = x
        self._y = y
        if ord(x_label) > 90:
            _x_label = chr(ord(x_label) + 6)
        if ord(y_label) > 90:
            _y_label = chr(ord(y_label) + 6)
        self._label = y_label + x_label
        self._parent = None
        self._parent2 = None

    def setParent(self, parent, num: int) -> None:
        if num == 1:
            self._parent = parent
        else:
            self._parent2 = parent
    
    @property
    def label(self) -> str:
        return self._label

    @property
    def parent(self):
        return self._parent

    @property
    def parent2(self):
        return self._parent2

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    
# class to keep track of edges between nodes in the maze graph
class Edge:
    def __init__(self, label1: str, label2: str, coords1: tuple[int, ...], coords2: tuple[int, ...]):
        self._label1 = label1
        self._label2 = label2
        self._coords1 = coords1
        self._coords2 = coords2

    @property
    def label1(self):
        return self._label1

    @property
    def label2(self):
        return self._label2
    
    @property
    def coords1(self):
        return self._coords1
    
    @property
    def coords2(self):
        return self._coords2