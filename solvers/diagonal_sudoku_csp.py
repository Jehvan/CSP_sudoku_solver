# solvers/diagonal_sudoku_csp.py

from constraint import Problem, AllDifferentConstraint

def solve_diagonal_sudoku(grid):
    """
    Solves a Diagonal Sudoku (X-Sudoku) using CSP.
    Modifies grid in-place.
    """
    N = 9
    problem = Problem()

    # Add variables with domains
    for r in range(N):
        for c in range(N):
            val = grid[r][c]
            if val != 0:
                problem.addVariable((r, c), [val])
            else:
                problem.addVariable((r, c), range(1, 10))

    # Row & column constraints
    for i in range(N):
        problem.addConstraint(AllDifferentConstraint(), [(i, j) for j in range(N)])  # Row
        problem.addConstraint(AllDifferentConstraint(), [(j, i) for j in range(N)])  # Column

    # Box constraints
    for br in range(0, N, 3):
        for bc in range(0, N, 3):
            box = [(br + i, bc + j) for i in range(3) for j in range(3)]
            problem.addConstraint(AllDifferentConstraint(), box)

    # Diagonal constraints
    main_diag = [(i, i) for i in range(N)]
    anti_diag = [(i, N-1-i) for i in range(N)]
    problem.addConstraint(AllDifferentConstraint(), main_diag)
    problem.addConstraint(AllDifferentConstraint(), anti_diag)

    # Solve
    solution = problem.getSolution()
    if solution:
        for r in range(N):
            for c in range(N):
                grid[r][c] = solution[(r, c)]
        return True

    return False
