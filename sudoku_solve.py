#!/usr/bin/env python3
# Copyright © 2014 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source
# distribution of this software for license terms.
# Sudoku solver

from sudoku_color import *
from sys import setrecursionlimit

setrecursionlimit(100)
read_puzzle()
for soln in color_puzzle(None, False):
    print_solution(soln)
    print()
