import tkinter as tk

def display_killer_sudoku(grid, cages=None, fixed=set()):
    root = tk.Tk()
    root.title("Killer Sudoku")

    cell_size = 50
    font = ("Arial", 16, "bold")

    canvas = tk.Canvas(root, width=cell_size*9, height=cell_size*9)
    canvas.pack()

    # Draw grid
    for r in range(9):
        for c in range(9):
            x1, y1 = c*cell_size, r*cell_size
            x2, y2 = x1+cell_size, y1+cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2 if c%3==0 or r%3==0 else 1)

            val = grid[r][c]
            color = "green" if (r,c) in fixed else "black"

            # Draw number
            if val != 0:
                canvas.create_text(x1+cell_size/2, y1+cell_size/2, text=str(val), fill=color, font=font)

    # Draw cage sums
    if cages:
        for cage in cages:
            r, c = cage["cells"][0]  # top-left of cage
            sum_val = cage["sum"]
            canvas.create_text(c*cell_size+5, r*cell_size+5, text=str(sum_val),
                               anchor="nw", fill="blue", font=("Arial", 10, "bold"))

    root.mainloop()
