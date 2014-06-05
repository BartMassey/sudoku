#!/usr/bin/env python3
# Copyright © 2014 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Sudoku generator / solver through graph coloring in Python.
# Hardwired to solve standard 9x9 Sudoku

# Vertices of the graph are Sudoku square numbers in row-major
# order starting with 0.

from random import shuffle
from sys import stdin

# Produce a vertex number from a coordinate
def index(r, c):
    return 9 * r + c

# Create the graph for a 9x9 Sudoku in edge-list format.
# Only edges (v1, v2) with v1 < v2 are returned.
def mk_sudoku_graph():
    # Create a clique on the given vertices
    def mk_complete_graph(vertices):
        graph = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                edge = (vertices[i], vertices[j])
                graph += [tuple(sorted(edge))]
        return graph
    # Start with the empty graph
    graph = []
    # Add column edges for each row
    for r in range(9):
        edges = []
        for c in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    # Add row edges for each column
    for c in range(9):
        edges = []
        for r in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    # Add box edges for each box
    for rb in range(0, 9, 3):
        for cb in range(0, 9, 3):
            edges = []
            for r in range(3):
                for c in range(3):
                    edges += [index(rb + r, cb + c)]
            graph += mk_complete_graph(edges)
    # Remove duplicate edges
    return list(set(graph))

# Convert a graph from edge-list to adjacency-list format
def adj_list(graph):
    # Start with the empty graph
    alist = {}
    # Insert an edge in the graph
    def insert_edge(v1, v2):
        if v1 in alist:
            alist[v1] += [v2]
        else:
            alist[v1] = [v2]
    # For each edge, insert it both ways
    for (v1, v2) in graph:
        insert_edge(v1, v2)
        insert_edge(v2, v1)
    return alist

constraints = adj_list(mk_sudoku_graph())
colors = [0]*81
fixed = [False]*81   # Not currently used
ncolored = 0
debug = False

# Read in a Sudoku and color the given graph vertices
def read_puzzle():
    global ncolored
    for r in range(9):
        l = stdin.readline()
        for c in range(9):
            if l[c] == '.':
                continue
            v = index(r, c)
            fixed[v] = True
            colors[v] = int(l[c])
            ncolored += 1

# Print a Sudoku solution
def print_solution(soln):
    for r in range(9):
        for c in range(9):
            v = soln[index(r, c)]
            if v == 0:
                print(".", end="")
            else:
                print(v, end="")
        print()

# Actually color the graph. Returns a list of complete
# lists of colors
def color_puzzle(max_solns, shuffle_colors):
    global ncolored, colors, debug
    if debug:
        print("coloring %d" % (ncolored,))
    # Base case: If no more solutions are needed, give up
    if max_solns != None and max_solns <= 0:
        return []
    # Base case: If we've found a solution,
    # return a list containing it
    if ncolored >= 81:
        return [colors*1]
    # Return the set of colors of colored neighbors of v
    def neighbor_colors(v):
        ncs = set([])
        for v0 in constraints[v]:
            if colors[v0] > 0:
                ncs = ncs.union({colors[v0]})
        return ncs
    # Find the first v that has the least number
    # of possible colors of all uncolored vertices
    def most_constrained_free():
        ncs = -1
        target = -1
        for v in range(len(colors)):
            # Don't recolor a vertex
            if colors[v] > 0:
                continue
            ncsv = len(neighbor_colors(v))
            if ncsv > ncs:
                target = v
                ncs = ncsv
        assert target != -1
        return target
    # Return the first uncolored vertex
    def first_free():
        for v in range(len(colors)):
            if colors[v] == 0:
                return v
        assert False
    # No point in MCF if all solutions? I'm not sure
    # this is right / needed
    if max_solns == 1:
        v = most_constrained_free()
    else:
        v = first_free()
    # Get ordered set of possible colors for chosen vertex
    cs = set(range(1,10)).difference(neighbor_colors(v))
    # If there are no legal colors, we're stuck
    if len(cs) == 0:
        return []
    # If generating, shuffle the colors from priority order
    if shuffle_colors:
        cs = list(cs)
        shuffle(cs)
    # Try all possible legal colors for v
    ncolored += 1
    solns = []
    for c in cs:
        if debug:
            print("coloring %d with %d (%d)" % (v, c, ncolored))
        colors[v] = c
        solns_cur = color_puzzle(max_solns, shuffle_colors)
        if debug:
            print("found %d solutions" % (len(solns_cur),))
        solns += solns_cur
        if max_solns != None:
            max_solns -= len(solns_cur)
            if max_solns <= 0:
                break
    colors[v] = 0
    ncolored -= 1
    return solns
