import grids.greater_less
import grids.odd_even

from api.api import get_classic_sudoku
from solvers.classic_csp import solve_sudoku

from grids.killer_sudoku import get_killer_board, empty_grid
from utils.printer import pretty_print
from gui.killer_gui import display_killer_sudoku
from solvers.killer_sudoku_csp import solve_killer_csp

from solvers.odd_even_csp import solve_odd_even_sudoku
from grids.diagonal_sudoku import DIAGONAL_1
from solvers.diagonal_sudoku_csp import solve_diagonal_sudoku

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
        "Choose mode (classic, killer, diagonal, odd_even): "
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

        initial_grid = board["grid"]
        grid = [row[:] for row in initial_grid]
        cages = board["cages"]

        fixed = {
            (r,c)
            for r in range(9)
            for c in range(9)
            if initial_grid[r][c] != 0
        }

        validate_cages(cages)
        success = solve_killer_csp(grid, cages, initial_grid)

        if success:
            display_killer_sudoku(grid, fixed=fixed, cages=cages)
        else:
            print("No solution found.")

    # ======================
    # DIAGONAL SUDOKU
    # ======================
    elif mode == "diagonal":
        grid = [row[:] for row in DIAGONAL_1["grid"]]

        success = solve_diagonal_sudoku(grid)

        if success:
            print("\nDiagonal Sudoku solved:\n")
            pretty_print(grid, fixed={(r, c) for r in range(9) for c in range(9) if DIAGONAL_1['grid'][r][c] != 0})
        else:
            print("No solution found.")

    # ======================
    # ODD / EVEN SUDOKU
    # ======================
    elif mode == "odd_even":
        initial_grid = grids.odd_even.ODD_EVEN_SUDOKU["grid"]
        parity = grids.odd_even.ODD_EVEN_SUDOKU["parity"]
        grid = [row [:] for row in initial_grid]
        success = solve_odd_even_sudoku(grid, parity)

        fixed = {
            (r, c)
            for r in range(9)
            for c in range(9)
            if initial_grid[r][c] != 0
        }

        if success:
            print("\nBlue numbers must be odd\nMagenta numbers must be even\nWhite numbers are prefilled")
            print("Odd/Even Sudoku solved:")
            pretty_print(grid, fixed=fixed, parity=parity)
        else:
            print("No solution found.")

    else:
        print("Unknown mode!")


if __name__ == "__main__":
    main()
