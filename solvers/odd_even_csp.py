from constraint import Problem, AllDifferentConstraint

GRID_SIZE = 9
ODD = {1, 3, 5, 7, 9}
EVEN = {2, 4, 6, 8}


def solve_odd_even_sudoku(grid, parity):
    """
    grid   : 9x9 matrix, 0 = empty
    parity : 9x9 matrix with 'O', 'E', or '.'
    """

    problem = Problem()

    # Variables + Domains
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            var = (r, c)

            if grid[r][c] != 0:
                # Pre-filled cell
                problem.addVariable(var, [grid[r][c]])

            else:
                if parity[r][c] == "O":
                    problem.addVariable(var, ODD)
                elif parity[r][c] == "E":
                    problem.addVariable(var, EVEN)
                else:
                    problem.addVariable(var, range(1, 10))

    # Row constraints
    for r in range(GRID_SIZE):
        problem.addConstraint(
            AllDifferentConstraint(),
            [(r, c) for c in range(GRID_SIZE)]
        )

    # Column constraints
    for c in range(GRID_SIZE):
        problem.addConstraint(
            AllDifferentConstraint(),
            [(r, c) for r in range(GRID_SIZE)]
        )

    # 3x3 box constraints
    for br in range(0, GRID_SIZE, 3):
        for bc in range(0, GRID_SIZE, 3):
            box = []
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    box.append((r, c))

            problem.addConstraint(AllDifferentConstraint(), box)

    # Solve
    solution = problem.getSolution()

    if solution is None:
        return False

    # Write solution back into grid
    for (r, c), value in solution.items():
        grid[r][c] = value

    return True
