# Sudoku Generator / Solver
Copyright &copyr; 2014 Bart Massey

This little chunk of Python code is a rewrite of my
originally [Nickle](http://nickle.org)
[Sudoku](http://en.wikipedia.org/wiki/Sudoku) generator /
solver.

The solver is a graph-coloring solver that works pretty
well.

The generator is an algorithm more-or-less taken from
[KSudoku](http://kde.org/applications/games/ksudoku/): it
starts by generating a random solved puzzle using the solver
on an empty board with random choices, and then deletes
squares in random order until it comes to a deletion that
would make the solution ambiguous.

This program is licensed under the "MIT License".  Please
see the file COPYING in the source distribution of this
software for license terms.
