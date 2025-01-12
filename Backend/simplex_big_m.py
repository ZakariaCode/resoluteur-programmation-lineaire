import numpy as np

def simplex_big_m(c, A, b, is_minimization=False):
    num_vars = len(c)
    num_constraints = len(A)
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    for i in range(len(b)):
        if b[i] < 0:
            A[i] *= -1
            b[i] *= -1

    slack_vars = np.eye(num_constraints)
    A = np.hstack([A, slack_vars])
    c = np.hstack([c, np.zeros(num_constraints)])

    artificial_vars_needed = []
    for i in range(num_constraints):
        if np.sum(A[i, :num_vars]) > b[i]:
            artificial_vars_needed.append(i)
    
    artificial_vars = np.zeros((num_constraints, len(artificial_vars_needed)))
    for idx, row in enumerate(artificial_vars_needed):
        artificial_vars[row, idx] = 1

    A = np.hstack([A, artificial_vars])
    c = np.hstack([c, [1e3] * len(artificial_vars_needed) if is_minimization else [-1e3] * len(artificial_vars_needed)])

    tableau = np.zeros((num_constraints + 1, len(c) + 1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = b
    tableau[-1, :-1] = -c if is_minimization else c

    for idx, row in enumerate(artificial_vars_needed):
        tableau[-1, :] += 1e3 * tableau[row, :] if is_minimization else -1e3 * tableau[row, :]

    while True:
        pivot_col = np.argmin(tableau[-1, :-1]) if is_minimization else np.argmax(tableau[-1, :-1])
        if (is_minimization and tableau[-1, pivot_col] >= 0) or (not is_minimization and tableau[-1, pivot_col] <= 0):
            break  

        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        valid_ratios = np.where(tableau[:-1, pivot_col] > 0, ratios, np.inf)
        pivot_row = np.argmin(valid_ratios)
        if valid_ratios[pivot_row] == np.inf:
            raise ValueError("Unbounded problem")

        tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]
        for i in range(len(tableau)):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau[:-1, i]
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            row = np.where(col == 1)[0][0]
            solution[i] = tableau[row, -1]

    optimal_value = tableau[-1, -1] if not is_minimization else -tableau[-1, -1]
    optimal_value = abs(optimal_value)
    if np.any(solution[num_vars:] > 1e-6):
        raise ValueError("No feasible solution")

    return solution[:num_vars], optimal_value
