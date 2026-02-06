import tkinter as tk

def display_killer_sudoku(grid, cages=None, fixed=None):
    if fixed is None:
        fixed = {(r, c) for r in range(9) for c in range(9) if grid[r][c] != 0}

    root = tk.Tk()
    root.title("Killer Sudoku")

    cell_size = 50
    font_fixed = ("Arial", 16, "bold")
    font_user = ("Arial", 16)

    canvas = tk.Canvas(root, width=cell_size*9, height=cell_size*9)
    canvas.pack()

    # Draw grid + values
    for r in range(9):
        for c in range(9):
            x1, y1 = c*cell_size, r*cell_size
            x2, y2 = x1+cell_size, y1+cell_size

            canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="black",
                width=2 if c % 3 == 0 or r % 3 == 0 else 1
            )

            val = grid[r][c]
            if val != 0:
                is_fixed = (r, c) in fixed
                canvas.create_text(
                    x1 + cell_size/2,
                    y1 + cell_size/2,
                    text=str(val),
                    fill="green" if is_fixed else "black",
                    font=font_fixed if is_fixed else font_user
                )

    # Draw cage sums
    if cages:
        for cage in cages:
            r, c = cage["cells"][0]
            canvas.create_text(
                c*cell_size + 5,
                r*cell_size + 5,
                text=str(cage["sum"]),
                anchor="nw",
                fill="blue",
                font=("Arial", 10, "bold")
            )

    root.mainloop()
