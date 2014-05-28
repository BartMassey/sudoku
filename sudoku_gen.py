#!/usr/bin/env python3
# Copyright © 2014 Bart Massey
# Sudoku generator

from sudoku_color import *
from random import shuffle
from sys import setrecursionlimit

def gen_sudoku_layout():
    global colors
    solns = color_puzzle(1, True)
    assert len(solns) == 1
    [cs] = solns
    colors = cs

# deletion-based puzzle creation algorithm
# suggested by ksudoku.
# g is assumed to be a partial solution
def del_soln():
    global colors
    delns = list(range(81))
    shuffle(delns)
    for v in delns:
        save = colors[v]
        colors[v] = 0
        solns = color_puzzle(2, False)
        if len(solns) > 1:
            for s in solns:
                print_solution(s)
            print()
            colors[v] = save

setrecursionlimit(100)
gen_sudoku_layout()
del_soln()
print_solution(colors)
