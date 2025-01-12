import numpy as np

def simplex(c, A, b, is_minimization=False):
    num_vars = len(c)
    num_constraints = len(A)

    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    tableau[:-1, :num_vars] = A
    tableau[:-1, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
    tableau[:-1, -1] = b
    tableau[-1, :num_vars] = c

    while True:
        if is_minimization:
            pivot_col = np.argmin(tableau[-1, :-1])  
        else:
            pivot_col = np.argmax(tableau[-1, :-1])  

        if (is_minimization and tableau[-1, pivot_col] >= 0) or (not is_minimization and tableau[-1, pivot_col] <= 0):
            break
        
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        pivot_row = np.where(ratios > 0, ratios, np.inf).argmin()

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

    optimal_value = tableau[-1, -1]
    if is_minimization==False:
        optimal_value = -optimal_value
    return solution, optimal_value
