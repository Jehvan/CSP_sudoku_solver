import tkinter as tk

CELL_SIZE = 50  # pixels per cell
GRID_COLOR = "black"
NUM_COLOR = "blue"
INEQUALITY_COLOR = "red"


def display_greater_less(grid, clues):
    N = len(grid)

    root = tk.Tk()
    root.title("Greater/Less Sudoku")
    canvas = tk.Canvas(root, width=CELL_SIZE * N, height=CELL_SIZE * N)
    canvas.pack()

    # Draw cells and numbers
    for r in range(N):
        for c in range(N):
            x0, y0 = c * CELL_SIZE, r * CELL_SIZE
            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
            canvas.create_rectangle(x0, y0, x1, y1, outline=GRID_COLOR, width=2)

            # Draw numbers
            if grid[r][c] != 0:
                canvas.create_text(x0 + CELL_SIZE / 2, y0 + CELL_SIZE / 2,
                                   text=str(grid[r][c]), fill=NUM_COLOR, font=("Arial", 16, "bold"))

    # Draw inequalities
    for (r1, c1), (r2, c2), rel in clues:
        x1 = c1 * CELL_SIZE + CELL_SIZE / 2
        y1 = r1 * CELL_SIZE + CELL_SIZE / 2
        x2 = c2 * CELL_SIZE + CELL_SIZE / 2
        y2 = r2 * CELL_SIZE + CELL_SIZE / 2

        if r1 == r2:  # horizontal
            canvas.create_text((x1 + x2) / 2, y1, text=rel, fill=INEQUALITY_COLOR, font=("Arial", 14, "bold"))
        elif c1 == c2:  # vertical
            # Flip < or > to show up-down correctly
            if rel == '>':
                rel = 'v'  # cell1 > cell2 -> draw downward arrow
            elif rel == '<':
                rel = '^'  # cell1 < cell2 -> draw upward arrow
            canvas.create_text(x1, (y1 + y2) / 2, text=rel, fill=INEQUALITY_COLOR, font=("Arial", 14, "bold"))

    root.mainloop()
