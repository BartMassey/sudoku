#!/usr/bin/env python3
# Copyright (c) 2014 Bart Massey

# Sudoku solver through graph coloring in Python
# Hardwired to solve standard 9x9 Sudoku

# Vertices of the graph are Sudoku square numbers in row-major
# order starting with 0.

# Graph format is list of edge 2-tuples with lower vertex first.

from sys import stdin, setrecursionlimit

setrecursionlimit(82)

def index(r, c):
    return 9 * r + c

def mk_sudoku_graph():
    def mk_complete_graph(vertices):
        graph = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                edge = (vertices[i], vertices[j])
                graph += [tuple(sorted(edge))]
        return graph
    graph = []
    # Add column edges for each row.
    for r in range(9):
        edges = []
        for c in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    # Add row edges for each column.
    for c in range(9):
        edges = []
        for r in range(9):
            edges += [index(r, c)]
        graph += mk_complete_graph(edges)
    # Add box edges for each box.
    for rb in range(0, 9, 3):
        for cb in range(0, 9, 3):
            edges = []
            for r in range(3):
                for c in range(3):
                    edges += [index(rb + r, cb + c)]
            graph += mk_complete_graph(edges)
    return list(set(graph))

def adj_list(graph):
    alist = {}
    def insert_vertices(v1, v2):
        if v1 in alist:
            alist[v1] += [v2]
        else:
            alist[v1] = [v2]
    for (v1, v2) in graph:
        insert_vertices(v1, v2)
        insert_vertices(v2, v1)
    return alist

constraints = adj_list(mk_sudoku_graph())
colors = [0]*81
fixed = [False]*81
ncolored = 0

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

def print_solution():
    for r in range(9):
        for c in range(9):
            v = colors[index(r, c)]
            if v == 0:
                print(".", end="")
            else:
                print(v, end="")
        print()

def color_puzzle():
    global ncolored, colors, fixed
    if ncolored >= 81:
        print_solution()
        return
    def neighbor_colors(v):
        ncs = set([])
        for v0 in constraints[v]:
            if colors[v0] > 0:
                ncs = ncs.union({colors[v0]})
        return ncs
    def most_constrained_free():
        ncs = -1
        target = -1
        for v in range(len(colors)):
            if fixed[v]:
                continue
            ncsv = len(neighbor_colors(v))
            if ncsv > ncs:
                target = v
                ncs = ncsv
        assert target != -1
        return target
    v = most_constrained_free()
    cs = set(range(1,10)).difference(neighbor_colors(v))
    if len(cs) == 0:
        return
    ncolored += 1
    fixed[v] = True
    for c in cs:
        colors[v] = c
        color_puzzle()
    colors[v] = 0
    fixed[v] = False
    ncolored -= 1

read_puzzle()
color_puzzle()