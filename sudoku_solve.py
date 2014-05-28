#!/usr/bin/env python3
# Copyright © 2014 Bart Massey
# Sudoku solver

from sudoku_color import *
from sys import setrecursionlimit

setrecursionlimit(100)
read_puzzle()
for soln in color_puzzle(None, False):
    print_solution(soln)
    print()
