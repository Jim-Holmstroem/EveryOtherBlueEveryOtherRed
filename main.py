from __future__ import print_function, division

from itertools import product
from operator import (
    getitem,
    setitem,
)

import os
import numpy as np

red = "."
blue = "*"
world = np.array(map(list,[
    "   .     * ",
    "*#*#.### # ",
    " . *   .   ",
    " # #*#.###.",
    " *       * ",
    ".#####*####",
]))

start = ((5, 0), None, ".")
goal = ((5, 6), (4, 6), "*")  # TODO do not require old_position for goal

def invert(color):
    if color == red:
        return blue
    elif color == blue:
        return red

def is_color(token):
    return token in {red, blue}

def update_color(color, token):
    if is_color(token):
        color = invert(color)

    return color

center = {(0, 0)}
# possible_moves = set(product([-1, 0, 1], repeat=2)) - center
possible_moves = {(1, 0), (0, 1), (-1, 0), (0, -1)}

def neighbourhood((xc, yc)):
    def inside((x, y)):
        return 0 <= x < world.shape[0] and 0 <= y < world.shape[1]

    return filter(
        inside,
        map(
            lambda (dx, dy): (xc + dx, yc + dy),
            possible_moves
        )
    )


def steps((position, old_position, color)):
    return set(map(
        lambda step_position: (step_position, position, update_color(color, getitem(world, step_position))),
        filter(
            lambda step_position: getitem(world, step_position) not in {"#", color} and step_position != old_position,
            neighbourhood(position)
        )
    ))

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph(vertex) - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def next_screen():
    raw_input()
    os.system('clear')

def view((position, old_position, color)):
    world_copy = world.copy()
    setitem(world_copy, position, '0')
    map(print, map("".join, world_copy))

    next_screen()

def main():
    next_screen()

    shortest_solution = next(bfs_paths(steps, start, goal))
    map(view, shortest_solution)

if __name__ == "__main__":
    main()
