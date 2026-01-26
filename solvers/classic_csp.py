from constraint import Problem, AllDifferentConstraint

def solve_sudoku(grid):
    problem = Problem()

    # Adding variables and domains in the CSP solver
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                problem.addVariable((r, c), range(1, 10))
            else:
                problem.addVariable((r, c), [grid[r][c]])

    # Row constraints
    for r in range(9):
        problem.addConstraint(
            AllDifferentConstraint(),
            [(r, c) for c in range(9)]
        )

    # Column constraints
    for c in range(9):
        problem.addConstraint(
            AllDifferentConstraint(),
            [(r, c) for r in range(9)]
        )

    # 3x3 block constraints
    for br in range(3):
        for bc in range(3):
            block = [
                (r, c)
                for r in range(br * 3, br * 3 + 3)
                for c in range(bc * 3, bc * 3 + 3)
            ]
            problem.addConstraint(AllDifferentConstraint(), block)

    solution = problem.getSolution()
    if solution is None:
        return None

    return [[solution[(r, c)] for c in range(9)] for r in range(9)]
