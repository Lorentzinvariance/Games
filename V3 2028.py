"""
Not finished!
"""
import tkinter as tk
import numpy as np
import random as random


# Grid initialisation
grid = np.zeros((4,4))

ry = random.randint(0,3)
rx = random.randint(0,3)
grid[ry][rx] = 2

root = tk.Tk()

# Tile dimensions and animation parameters
tile_size = 100
padding = 50

ANIM_STEPS = 10
ANIM_DELAY = 30 # ms

# Outer frame for padding and score
frame = tk.Frame(root, bg="#bbada0", padx=10, pady=10)
frame.grid(padx=20, pady=20)
frame_width = 4 * tile_size + 3 * padding
frame_height = 4 * tile_size + 3 * padding + 50  # extra space for score

frame.config(width=frame_width, height=frame_height)

def get_pixel_position(row, column):
    x = column * (tile_size + padding)
    y = row * (tile_size + padding) + 50  # leave room for score
    return x, y

tiles = {}
tile_positions = {}
# Initialisation of tiles
for i in range(4):
    for j in range(4):
        label = tk.Label(frame, text="", font=("Helvetica", 34, "bold"),
                         width=4, height=2, bg="#cdc1b4", fg="#776e65",
                         borderwidth=2, relief="ridge")
        x,y = get_pixel_position(i, j)
        label.place(x=x, y=y)
        tiles[(i,j)] = label
        tile_positions[label] = (i,j)


# Score label
score = 0
score_label = tk.Label(frame, text=f"Score: {score}", font=("Helvetica", 24, "bold"),
                       bg="#bbada0", fg="white")
#score_label.grid(row=0, column=0, columnspan=4, pady=(0,10))
score_label.place(x=0,y=0)

colors = {0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563"}


# Functions

#CHECK THIS
def animate_tile_move(label, start_pos, end_pos, new_grid_pos, steps=ANIM_STEPS, delay=ANIM_DELAY):
    global tile_positions
    x0, y0 = start_pos
    x1, y1 = end_pos

    def step(step_num=0):
        if step_num <= steps:
            x = x0 + (x1 - x0) * step_num / steps
            y = y0 + (y1 - y0) * step_num / steps
            label.place(x=x, y=y)
            label.after(delay, step, step_num + 1)
        else:
            tile_positions[label] = new_grid_pos

    step()


def update_gui(board):
    for i in range(4):
        for j in range(4):
            num = board[i][j]
            label = tiles[(i,j)]
            label.config(
                text=str(int(num)) if num else "",
                bg=colors.get(num, "#3c3a32")
            )

def addrandom24(board):
    nonzero_indices = np.argwhere(board == 0)
    random_index = nonzero_indices[np.random.choice(len(nonzero_indices))]
    addedvalue = 2 * random.randint(1,2)
    i = random_index[0]
    j = random_index[1]
    board[i][j] = addedvalue
    return board, addedvalue

def shiftleft(board):
    shifted = np.zeros_like(board)
    for i, row in enumerate(board):
        nonzeros = row[row != 0]
        shifted[i, :len(nonzeros)] = nonzeros
    return shifted

def mergeshift(board):
    global score
    for i, row in enumerate(board):
        for j in range(3):
            if row[j] == row[j+1] and row[j] != 0:
                row[j] += row[j+1]
                score += 2 * row[j]
                row[j+1] = 0
        board[i] = row 
    board = shiftleft(board)
    return board

def moveleft(board):
    board = shiftleft(board)
    return mergeshift(board)

def moveup(board):
    board = np.rot90(board, k = 1)
    board = moveleft(board)
    return np.rot90(board, k = 3)

def moveright(board):
    board = np.rot90(board, k = 2)
    board = moveleft(board)
    return np.rot90(board, k = 2)

def movedown(board):
    board = np.rot90(board, k = 3)
    board = moveleft(board)
    return np.rot90(board, k = 1)

def movingtiles(old_grid, new_grid):
    movements = {}
    used_old_positions = set()
    
    # First pass: find tiles that moved (same value, different position)
    for new_i in range(4):
        for new_j in range(4):
            new_val = new_grid[new_i][new_j]
            if new_val == 0:
                continue
                
            # Look for this tile in the old grid
            for old_i in range(4):
                for old_j in range(4):
                    if (old_i, old_j) in used_old_positions:
                        continue
                    old_val = old_grid[old_i][old_j]
                    if old_val == new_val:
                        # Found matching tile
                        label = tiles[(old_i, old_j)]
                        movements[label] = (new_i, new_j)
                        used_old_positions.add((old_i, old_j))
                        break
                else:
                    continue
                break
    return movements

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
    global grid, score
    old_grid = grid.copy()
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
    
    new_positions = movingtiles(old_grid, grid)
    print("Tiles to animate:", new_positions)
    for label, (i,j) in new_positions.items():
        old_row, old_col = tile_positions[label]
        new_row, new_col = i, j
        start = get_pixel_position(old_row, old_col)
        end = get_pixel_position(new_row, new_col)
        animate_tile_move(label, start, end, (i,j))

    # Update score
    score_label.config(text=f"Score: {int(score)}")

    # Update GUI after animation
    #root.after(ANIM_STEPS*ANIM_DELAY + 20, lambda: update_gui(grid))
    update_gui(grid)
    if game_over(grid):
        overlay = tk.Label(root, text="You suck!", font=("Helvetica", 32, "bold"),
                           bg="red", fg="white")
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        
    if you_won(grid):
        overlay = tk.Label(root, text="Killing it bro!", font=("Helvetica", 32, "bold"),
                           bg="black", fg="gold")
        overlay.place(relx=0.5, rely=0.5, anchor="center")


def game(event):
    global grid, score
    old_grid = grid.copy()
    move_made = False
    
    typemove = event.keysym
    if typemove == "Left":
        new_grid = moveleft(grid.copy())
        move_made = not np.array_equal(grid, new_grid)
        if move_made:
            grid = new_grid
            grid, value = addrandom24(grid)
    elif typemove == "Up":
        new_grid = moveup(grid.copy())
        move_made = not np.array_equal(grid, new_grid)
        if move_made:
            grid = new_grid
            grid, value = addrandom24(grid)
    elif typemove == "Right":
        new_grid = moveright(grid.copy())
        move_made = not np.array_equal(grid, new_grid)
        if move_made:
            grid = new_grid
            grid, value = addrandom24(grid)
    elif typemove == "Down":
        new_grid = movedown(grid.copy())
        move_made = not np.array_equal(grid, new_grid)
        if move_made:
            grid = new_grid
            grid, value = addrandom24(grid)
    else:
        return
    
    if move_made:
        score_label.config(text=f"Score: {score}")
        
        movements = movingtiles(old_grid, grid)
        print("Tiles to animate:", movements)
        
        for label, (new_i, new_j) in movements.items():
            old_i, old_j = tile_positions[label]
            start_pos = get_pixel_position(old_i, old_j)
            end_pos = get_pixel_position(new_i, new_j)
            animate_tile_move(label, start_pos, end_pos, (new_i, new_j))
        
        # Update GUI after animation completes
        root.after(ANIM_STEPS * ANIM_DELAY + 50, lambda: update_gui(grid))
        
        if you_won(grid):
            overlay = tk.Label(root, text="You Win!", font=("Helvetica", 32, "bold"),
                               bg="gold", fg="black")
            overlay.place(relx=0.5, rely=0.5, anchor="center")
        elif game_over(grid):
            overlay = tk.Label(root, text="Game Over!", font=("Helvetica", 32, "bold"),
                               bg="red", fg="white")
            overlay.place(relx=0.5, rely=0.5, anchor="center")
    else:
        # Still update GUI even if no move was made
        update_gui(grid)

root.bind("<Key>", game)

update_gui(grid)
root.mainloop()
