# solvers/killer_sudoku_csp.py
from constraint import Problem, AllDifferentConstraint
import itertools

# Precompute all valid combinations for cages (length 1-9)
# This is done once to avoid recomputing combinations during solving
PRECOMPUTED_COMBS = {}
for length in range(1, 10):
    for comb in itertools.combinations(range(1, 10), length):
        s = sum(comb)
        # Store sorted tuples so comparison is easy later
        PRECOMPUTED_COMBS.setdefault((length, s), []).append(tuple(sorted(comb)))


def solve_killer_csp(grid, cages):
    """
    Killer Sudoku solver using python-constraint.
    grid: 9x9 list of lists, will be filled in-place
    cages: list of dicts with "sum" and "cells" keys
    Returns True if solved, False otherwise
    """

    # Create the CSP problem
    problem = Problem()

    # Step 1: Filter domains for each cell based on cages
    # This avoids trying numbers that can't appear in a cage
    cell_domains = {}
    for cage in cages:
        n = len(cage["cells"])
        cage_sum = cage["sum"]
        valid_combs = PRECOMPUTED_COMBS.get((n, cage_sum), [])

        # Allowed numbers in this cage
        allowed_numbers = set()
        for comb in valid_combs:
            allowed_numbers.update(comb)

        for cell in cage["cells"]:
            if cell in cell_domains:
                cell_domains[cell] &= allowed_numbers  # intersect if cell is in multiple cages
            else:
                cell_domains[cell] = allowed_numbers.copy()

    # Step 2: Add variables to CSP with filtered domains
    for r in range(9):
        for c in range(9):
            domain = list(cell_domains.get((r, c), range(1, 10)))
            problem.addVariable((r, c), domain)

    # Step 3: Standard Sudoku constraints
    # Rows
    for r in range(9):
        problem.addConstraint(AllDifferentConstraint(), [(r, c) for c in range(9)])
    # Columns
    for c in range(9):
        problem.addConstraint(AllDifferentConstraint(), [(r, c) for r in range(9)])
    # 3x3 boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box_cells = [(r, c) for r in range(br, br + 3) for c in range(bc, bc + 3)]
            problem.addConstraint(AllDifferentConstraint(), box_cells)

    # Step 4: Cage constraints
    # We enforce uniqueness (AllDifferent) and sum constraints
    for cage in cages:
        cells = cage["cells"]
        n = len(cells)
        cage_sum = cage["sum"]

        valid_combs = PRECOMPUTED_COMBS.get((n, cage_sum), [])

        # Uniqueness in cage
        problem.addConstraint(AllDifferentConstraint(), cells)

        # Sum constraint: only allow values matching a valid combination
        def cage_constraint(*vals, valid_combs=valid_combs):
            # Sort values to compare with precomputed combinations
            return tuple(sorted(vals)) in valid_combs

        problem.addConstraint(cage_constraint, cells)

    # Step 5: Solve the CSP
    solution = problem.getSolution()
    if not solution:
        return False  # no solution found

    # Step 6: Fill the grid with the solution
    for (r, c), val in solution.items():
        grid[r][c] = val

    # print("Solved Killer Sudoku grid:")
    # for row in grid:
    #     print(row)

    return True
