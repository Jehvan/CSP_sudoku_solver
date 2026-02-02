import grids.greater_less
from api.api import get_classic_sudoku
from gui.greater_less_gui import display_greater_less
from solvers.classic_csp import solve_sudoku
from grids.killer_sudoku import get_killer_board, empty_grid
from utils.printer import pretty_print
from gui.killer_gui import display_killer_sudoku
from solvers.killer_sudoku_csp import solve_killer_csp
from solvers.greater_less_csp import solve_greater_less_csp_fast

def validate_cages(cages):
    """Checks if cages are mathematically possible"""
    from itertools import combinations
    for cage in cages:
        n = len(cage["cells"])
        s = cage["sum"]
        min_sum = sum(range(1, n+1))
        max_sum = sum(range(10-n, 10))
        if not (min_sum <= s <= max_sum):
            print("Impossible cage:", cage)


def main():
    print("Sudoku Solver")
    mode = input("Choose mode (classic, killer, greater_less): ").lower()

    if mode == "classic":
        grid = get_classic_sudoku()
        if not grid:
            print("Failed to get a classic grid.")
            return

        fixed = {(r, c) for r in range(9) for c in range(9) if grid[r][c] != 0}
        solution = solve_sudoku(grid)

        if solution:
            print("\nClassic Sudoku solved:\n")
            pretty_print(solution, fixed)
        else:
            print("No solution found.")

    elif mode == "killer":
        board = get_killer_board(3)
        grid = empty_grid()
        cages = board["cages"]
        validate_cages(cages)
        success = solve_killer_csp(grid, cages)

        if success:
            display_killer_sudoku(grid, fixed=set(), cages=cages)
        else:
            print("No solution found.")

    elif mode == "greater_less":
        grid = grids.greater_less.grid_9x9
        clues = grids.greater_less.clues_9x9
        success = solve_greater_less_csp_fast(grid, clues)

        if success:
            display_greater_less(grid, clues)
        else:
            print("No solution found.")

    else:
        print("Unknown mode!")


if __name__ == "__main__":
    main()
