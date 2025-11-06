# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 13:11:03 2025

@author: Sande

Implementation of 4048

Given two randomd positions with a 2. Given an imput (direction: up, right, down, left). Give the resulting grid (4x4) of the game. That means: Swiping to a direction, aligns all blocks to that direction. When multiple ajecant blocks are of the same value, combine them into one. Add one random position 2 or 4 after each move
"""

import numpy as np
import random as random


grid = np.zeros((4,4))

ry = random.randint(0,3)
rx = random.randint(0,3)
grid[ry][rx] = 2

def addrandom24(matrix):
    nonzero_indices = np.argwhere(matrix == 0)
    random_index = nonzero_indices[np.random.choice(len(nonzero_indices))]
    addedvalue = 2*random.randint(1,2)
    i = random_index[0]
    j = random_index[1]
    matrix[j][i] = addedvalue
    return matrix

def shiftleft(grid):
    shifted = np.zeros_like(grid)
    for i, row in enumerate(grid):
        nonzeros = row[row != 0]
        shifted[i, :len(nonzeros)] = nonzeros
    return shifted

def mergeshift(grid):
    for i, row in enumerate(grid):
        for j in range(3):
            if row[j] == row[j+1]:
                row[j] += row[j+1]
                row[j+1] = 0
        grid[i] = row 
    grid = shiftleft(grid)
    return grid

def moveleft(grid):
    grid = shiftleft(grid)
    return mergeshift(grid)

def moveup(grid):
    grid = np.rot90(grid, k = 1)
    grid = moveleft(grid)
    return np.rot90(grid, k = 3)

def moveright(grid):
    grid = np.rot90(grid, k = 2)
    grid = moveleft(grid)
    return np.rot90(grid, k = 2)

def movedown(grid):
    grid = np.rot90(grid, k = 3)
    grid = moveleft(grid)
    return np.rot90(grid, k = 1)

def game(grid):
    store = grid
    print(store)
    while True:
        typemove = input("")
        if typemove == "left":
            store = addrandom24(moveleft(store))
        if typemove == "up":
            store = addrandom24(moveup(store))
        if typemove == "right":
            store = addrandom24(moveright(store))
        if typemove == "down":
            store = addrandom24(movedown(store))
        else:
            print("Not valid")
        print(store)

game(grid)
