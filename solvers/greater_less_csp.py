def solve_greater_less_csp_fast(grid, clues):
    """
    Solves a Greater-Less Sudoku using CSP backtracking with:
    - MRV
    - Forward checking
    - Proper constraint propagation
    """

    N = len(grid)
    BOX = int(N ** 0.5)

    # -----------------------------
    # Initialize domains
    # -----------------------------
    domains = [[set(range(1, N + 1)) for _ in range(N)] for _ in range(N)]

    for r in range(N):
        for c in range(N):
            if grid[r][c] != 0:
                domains[r][c] = {grid[r][c]}

    # -----------------------------
    # Constraint propagation
    # -----------------------------
    def propagate(r, c, val, domains):
        domains[r][c] = {val}

        # Row & column
        for i in range(N):
            if i != c:
                domains[r][i].discard(val)
            if i != r:
                domains[i][c].discard(val)

        # Box
        br = (r // BOX) * BOX
        bc = (c // BOX) * BOX
        for i in range(br, br + BOX):
            for j in range(bc, bc + BOX):
                if (i, j) != (r, c):
                    domains[i][j].discard(val)

        # Directed inequality propagation
        for (a, b, op) in clues:
            ar, ac = a
            br_, bc_ = b

            if (ar, ac) == (r, c):
                if op == '<':
                    domains[br_][bc_] = {x for x in domains[br_][bc_] if x > val}
                else:
                    domains[br_][bc_] = {x for x in domains[br_][bc_] if x < val}

            elif (br_, bc_) == (r, c):
                if op == '<':
                    domains[ar][ac] = {x for x in domains[ar][ac] if x < val}
                else:
                    domains[ar][ac] = {x for x in domains[ar][ac] if x > val}

        # Bidirectional inequality tightening (SAFE)
        for (a, b, op) in clues:
            ar, ac = a
            br_, bc_ = b

            if not domains[ar][ac] or not domains[br_][bc_]:
                return False  # Dead end

            if op == '<':
                max_b = max(domains[br_][bc_])
                min_a = min(domains[ar][ac])

                domains[ar][ac] = {x for x in domains[ar][ac] if x < max_b}
                if not domains[ar][ac]:
                    return False

                domains[br_][bc_] = {x for x in domains[br_][bc_] if x > min_a}
                if not domains[br_][bc_]:
                    return False
            else:
                min_b = min(domains[br_][bc_])
                max_a = max(domains[ar][ac])

                domains[ar][ac] = {x for x in domains[ar][ac] if x > min_b}
                if not domains[ar][ac]:
                    return False

                domains[br_][bc_] = {x for x in domains[br_][bc_] if x < max_a}
                if not domains[br_][bc_]:
                    return False

        return True

    # -----------------------------
    # MRV
    # -----------------------------
    def select_cell(domains):
        best = None
        best_len = N + 1
        for r in range(N):
            for c in range(N):
                if grid[r][c] == 0:
                    l = len(domains[r][c])
                    if l < best_len:
                        best_len = l
                        best = (r, c)
        return best

    # -----------------------------
    # Backtracking
    # -----------------------------
    def backtrack(domains):
        cell = select_cell(domains)
        if not cell:
            return True, domains

        r, c = cell

        for val in sorted(domains[r][c]):
            new_domains = [[d.copy() for d in row] for row in domains]
            grid[r][c] = val

            if propagate(r, c, val, new_domains):
                solved, result = backtrack(new_domains)
                if solved:
                    return True, result

            grid[r][c] = 0

        return False, None

    # -----------------------------
    # Solve
    # -----------------------------
    solved, final_domains = backtrack(domains)

    if solved:
        for r in range(N):
            for c in range(N):
                grid[r][c] = next(iter(final_domains[r][c]))
        return True

    return False
