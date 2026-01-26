from api.api import get_classic_sudoku
from solvers.classic_csp import solve_sudoku
from utils.printer import pretty_print

def main():
    grid = get_classic_sudoku()

    fixed = {
        (r, c)
        for r in range(9)
        for c in range(9)
        if grid[r][c] != 0
    }

    print("Classic Sudoku:")
    pretty_print(grid, fixed)

    solution = solve_sudoku(grid)

    if solution:
        print("\nSolved:")
        pretty_print(solution, fixed)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
