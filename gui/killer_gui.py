import tkinter as tk


def build_cage_map(cages):
    """
    Returns a dict mapping (row, col) -> cage_id
    """
    cage_map = {}
    for cage_id, cage in enumerate(cages):
        for (r, c) in cage["cells"]:
            cage_map[(r, c)] = cage_id
    return cage_map



def display_killer_sudoku(grid, cages, fixed=set()):
    root = tk.Tk()
    root.title("Killer Sudoku")

    SIZE = 60
    canvas = tk.Canvas(root, width=SIZE*9, height=SIZE*9, bg="white")
    canvas.pack()

    cage_map = build_cage_map(cages)

    # Draw cells
    for r in range(9):
        for c in range(9):
            x1, y1 = c*SIZE, r*SIZE
            x2, y2 = x1+SIZE, y1+SIZE

            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

            val = grid[r][c]
            color = "green" if (r, c) in fixed else "black"
            if val:
                canvas.create_text(
                    x1+SIZE/2, y1+SIZE/2,
                    text=str(val),
                    font=("Arial", 18, "bold"),
                    fill=color
                )

    # Draw cage sums
    for cage in cages:
        r, c = cage["cells"][0]
        canvas.create_text(
            c*SIZE+5, r*SIZE+5,
            text=str(cage["sum"]),
            anchor="nw",
            font=("Arial", 10, "bold"),
            fill="blue"
        )

    # Draw thick cage borders
    for r in range(9):
        for c in range(9):
            cid = cage_map[(r, c)]
            x, y = c*SIZE, r*SIZE

            # Top
            if r == 0 or cage_map.get((r-1, c)) != cid:
                canvas.create_line(x, y, x+SIZE, y, width=4)

            # Bottom
            if r == 8 or cage_map.get((r+1, c)) != cid:
                canvas.create_line(x, y+SIZE, x+SIZE, y+SIZE, width=4)

            # Left
            if c == 0 or cage_map.get((r, c-1)) != cid:
                canvas.create_line(x, y, x, y+SIZE, width=4)

            # Right
            if c == 8 or cage_map.get((r, c+1)) != cid:
                canvas.create_line(x+SIZE, y, x+SIZE, y+SIZE, width=4)

    root.mainloop()
