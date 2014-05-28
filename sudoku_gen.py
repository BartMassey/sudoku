#!/usr/bin/env python3
# Copyright © 2014 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source
# distribution of this software for license terms.
# Sudoku generator

import sudoku_color
from sudoku_color import color_puzzle, print_solution
from random import shuffle
from sys import setrecursionlimit

def gen_sudoku_layout():
    solns = color_puzzle(1, True)
    assert len(solns) == 1
    [cs] = solns
    sudoku_color.colors = cs

# deletion-based puzzle creation algorithm
# suggested by ksudoku.
# g is assumed to be a partial solution
def del_soln():
    delns = list(range(81))
    ndelns = 0
    shuffle(delns)
    for v in delns:
        save = sudoku_color.colors[v]
        sudoku_color.colors[v] = 0
        sudoku_color.ncolored = 81 - ndelns - 1
        solns = color_puzzle(2, False)
        if len(solns) > 1:
            sudoku_color.colors[v] = save
        else:
            ndelns += 1

setrecursionlimit(100)
gen_sudoku_layout()
del_soln()
print_solution(sudoku_color.colors)

def debug_coloring():
    sudoku_color.colors[0] = 0
    sudoku_color.ncolored = 80
    sudoku_color.debug = True
    [soln1, soln2] = color_puzzle(2, False)
    print_solution(soln1)
    print()
    print_solution(soln2)
