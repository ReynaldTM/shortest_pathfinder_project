import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", " ", " ", "#", " ", "#", "#", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", "X"],
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"]
]


def print_maze(maze, stdscr, path=[]): # prints maze
    if path is None:
        path = []
    RED = curses.color_pair(1)
    GREEN = curses.color_pair(2)

    for i, row in enumerate(maze):  # i = row # of nested list, row = nested list
        for j, value in enumerate(row):  # j = column, value = symbol in cloumn
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", RED)
            else:
                stdscr.addstr(i, j * 2, value, GREEN)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


def find_path(maze, stdscr):
    # determine start coords
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))  # tuple; current pos and path to node

    visited = set()

    while not q.empty():
        current_pos, path = q.get() # get first in queue row, col
        row, col = current_pos

        stdscr.clear()  # clear terminal
        print_maze(maze, stdscr, path)  # row cloumn then what igoes no
        time.sleep(0.2)
        stdscr.refresh()  # refresh screen

        if maze[row][col] == end: # check if at end
            return path

        neighbors = find_neighbors(maze, row, col) # checking all neighbors
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#": # checking obstacle
                continue

            new_path = path + [neighbor] # adding to path
            q.put((neighbor, new_path)) # adding to queue
            visited.add(neighbor)


def find_neighbors(maze, row, col): # gives valid neighbors in maze
    neightbors = []

    if row > 0:  # UP
        neightbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neightbors.append((row + 1, col))
    if col > 0:  # LEFT
        neightbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neightbors.append((row, col + 1))

    return neightbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()  # wait for user input


wrapper(main)  # initailizes curses, calls function, with stdscr to control
