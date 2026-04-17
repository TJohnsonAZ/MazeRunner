# MazeRunner
Final project for CS470 Artificial Intelligence. AI maze solver that uses maze images as input.

This repository contains two top level directories: MazeRunner and MazeRunner2.0. MazeRunner contains the original project code as submitted for my final project on December 8, 2021. MazeRunner2.0 contains the updated code after revisions made on the week of April 13, 2026. The original project is included for reference and use in a "then vs. now" comparison.

### Requirements
Python 3.11 or newer\
matplotlib\
pillow\
PyQt6

### Usage
Once all requirements are satisfied, run the program with

```python maze_runner.py -s [size] -a [algorithm] -d [direction] --verbose/--no-verbose```

where size represents the size of the maze, algorithm represents the tree search algorithm to be used when traversing the maze, direction indicates whether the maze will be searched from one direction or two similtaniously, and verbose determines whether the program will output verbose printing for each maze traversal step.

Size options are: ```simple, moderate, difficult```.\
Algorithm options are ```depth-first, breadth-first```.\
Direction options are ```single, bidirectional```.
