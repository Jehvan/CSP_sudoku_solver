import grids.greater_less
import grids.odd_even

from api.api import get_classic_sudoku
from gui.greater_less_gui import display_greater_less
from solvers.classic_csp import solve_sudoku

from grids.killer_sudoku import get_killer_board, empty_grid
from utils.printer import pretty_print
from gui.killer_gui import display_killer_sudoku
from solvers.killer_sudoku_csp import solve_killer_csp

from solvers.greater_less_csp import solve_greater_less_csp_fast
from solvers.odd_even_csp import solve_odd_even_sudoku


def validate_cages(cages):
    """Checks if cages are mathematically possible"""
    for cage in cages:
        n = len(cage["cells"])
        s = cage["sum"]
        min_sum = sum(range(1, n + 1))
        max_sum = sum(range(10 - n, 10))
        if not (min_sum <= s <= max_sum):
            print("Impossible cage:", cage)


def main():
    print("Sudoku Solver")
    mode = input(
        "Choose mode (classic, killer, greater_less, odd_even): "
    ).lower()

    # ======================
    # CLASSIC SUDOKU
    # ======================
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

    # ======================
    # KILLER SUDOKU
    # ======================
    elif mode == "killer":
        difficulty = input("Choose killer board (easy, medium, hard): ")
        board = get_killer_board(difficulty)

        grid = empty_grid()
        cages = board["cages"]

        validate_cages(cages)
        success = solve_killer_csp(grid, cages)

        if success:
            display_killer_sudoku(grid, fixed=set(), cages=cages)
        else:
            print("No solution found.")

    # ======================
    # GREATER / LESS SUDOKU
    # ======================
    elif mode == "greater_less":
        grid = grids.greater_less.grid_9x9
        clues = grids.greater_less.clues_9x9

        success = solve_greater_less_csp_fast(grid, clues)

        if success:
            display_greater_less(grid, clues)
        else:
            print("No solution found.")

    # ======================
    # ODD / EVEN SUDOKU
    # ======================
    elif mode == "odd_even":
        grid = grids.odd_even.ODD_EVEN_SUDOKU["grid"]
        parity = grids.odd_even.ODD_EVEN_SUDOKU["parity"]

        success = solve_odd_even_sudoku(grid, parity)

        if success:
            print("\nOdd/Even Sudoku solved:\n")
            pretty_print(grid, fixed=set(), parity=parity)
        else:
            print("No solution found.")

    else:
        print("Unknown mode!")


if __name__ == "__main__":
    main()
