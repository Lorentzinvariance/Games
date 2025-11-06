import tkinter as tk
import numpy as np
import random as random


grid = np.zeros((4,4))

ry = random.randint(0,3)
rx = random.randint(0,3)
grid[ry][rx] = 2

root = tk.Tk()
tiles = [[None for _ in range(4)] for _ in range(4)]

# Outer frame for padding and score
frame = tk.Frame(root, bg="#bbada0", padx=10, pady=10)
frame.grid(padx=20, pady=20, sticky = "snew")

# Score label
score = 0
score_label = tk.Label(frame, text=f"Score: {score}", font=("Helvetica", 24, "bold"),
                       bg="#bbada0", fg="white")
score_label.grid(row=0, column=0, columnspan=4, pady=(0,10))

for i in range(4):
    for j in range(4):
        label = tk.Label(frame, text="", font=("Helvetica", 34, "bold"),
                         width=4, height=2, bg="#cdc1b4", fg="#776e65",
                         borderwidth=2, relief="ridge")
        label.grid(row=i+1, column=j, padx=5, pady=5)
        tiles[i][j] = label

colors = {0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563"}


def update_gui(board):
    for i in range(4):
        for j in range(4):
            num = board[i][j]
            label = tiles[i][j]
            label.config(
                text=str(int(num)) if num else "",
                bg=colors.get(num, "#3c3a32")
            )

def addrandom24(matrix):
    nonzero_indices = np.argwhere(matrix == 0)
    random_index = nonzero_indices[np.random.choice(len(nonzero_indices))]
    addedvalue = 2*random.randint(1,2)
    i = random_index[1]
    j = random_index[0]
    matrix[j][i] = addedvalue
    return matrix, addedvalue

def shiftleft(grid):
    shifted = np.zeros_like(grid)
    for i, row in enumerate(grid):
        nonzeros = row[row != 0]
        shifted[i, :len(nonzeros)] = nonzeros
    return shifted

def mergeshift(grid):
    global score
    for i, row in enumerate(grid):
        for j in range(3):
            if row[j] == row[j+1] and row[j] != 0:
                row[j] += row[j+1]
                score += 2 * row[j]
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

def game_over(board):
    if np.any(board == 0):
        return False
    # Horizontal check
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1]:
                return False
    # Vertical check
    for j in range(4):
        for i in range(3):
            if board[i][j] == board[i+1][j]:
                return False
    return True

def you_won(board):
    if np.any(board == 4096):
        return True
    else:
        return False

def game(event):
    global grid
    global score
    typemove = event.keysym
    if typemove == "Left":
        grid, value = addrandom24(moveleft(grid))
    elif typemove == "Up":
        grid, value = addrandom24(moveup(grid))
    elif typemove == "Right":
        grid, value = addrandom24(moveright(grid))
    elif typemove == "Down":
        grid, value = addrandom24(movedown(grid))
    else:
        return
    score += value
    score = int(score)
    score_label.config(text=f"Score: {score}")
    
    update_gui(grid)

    if game_over(grid):
        overlay = tk.Label(root, text="You suck!", font=("Helvetica", 32, "bold"),
                           bg="red", fg="white")
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        
    if you_won(grid):
        overlay = tk.Label(root, text="Killing it bro!", font=("Helvetica", 32, "bold"),
                           bg="black", fg="gold")
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        
root.bind("<Key>", game)

update_gui(grid)
root.mainloop()
