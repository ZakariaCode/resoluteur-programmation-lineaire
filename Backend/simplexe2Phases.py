import numpy as np

def simplex_two_phases(c, A, b, is_minimization=False):
    num_vars = len(c)
    num_constraints = len(A)

    tableau_phase1 = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    
    tableau_phase1[:-1, :num_vars] = A
    tableau_phase1[:-1, num_vars:num_vars + num_constraints] = np.eye(num_constraints)  
    tableau_phase1[:-1, -1] = b

    tableau_phase1[-1, num_vars:num_vars + num_constraints] = np.ones(num_constraints)

    while True:
        pivot_col = np.argmin(tableau_phase1[-1, :-1]) if is_minimization else np.argmax(tableau_phase1[-1, :-1])
        
        if (is_minimization and tableau_phase1[-1, pivot_col] >= 0) or (not is_minimization and tableau_phase1[-1, pivot_col] <= 0):
            break
        
        ratios = np.where(tableau_phase1[:-1, pivot_col] > 0, tableau_phase1[:-1, -1] / tableau_phase1[:-1, pivot_col], np.inf)
        pivot_row = np.where(ratios == np.min(ratios))[0][0]
        
        tableau_phase1[pivot_row, :] /= tableau_phase1[pivot_row, pivot_col]
        for i in range(len(tableau_phase1)):
            if i != pivot_row:
                tableau_phase1[i, :] -= tableau_phase1[i, pivot_col] * tableau_phase1[pivot_row, :]

    if np.sum(tableau_phase1[-1, num_vars:num_vars + num_constraints]) > 0:
        raise ValueError("Le problème n'a pas de solution faisable.")

    tableau_phase2 = tableau_phase1.copy()
    tableau_phase2[-1, :num_vars] = c 
    tableau_phase2[-1, num_vars:num_vars + num_constraints] = 0 

    while True:
        pivot_col = np.argmin(tableau_phase2[-1, :-1]) if is_minimization else np.argmax(tableau_phase2[-1, :-1])
        
        if (is_minimization and tableau_phase2[-1, pivot_col] >= 0) or (not is_minimization and tableau_phase2[-1, pivot_col] <= 0):
            break
        
        ratios = np.where(tableau_phase2[:-1, pivot_col] > 0, tableau_phase2[:-1, -1] / tableau_phase2[:-1, pivot_col], np.inf)
        pivot_row = np.where(ratios == np.min(ratios))[0][0]
        
        tableau_phase2[pivot_row, :] /= tableau_phase2[pivot_row, pivot_col]
        for i in range(len(tableau_phase2)):
            if i != pivot_row:
                tableau_phase2[i, :] -= tableau_phase2[i, pivot_col] * tableau_phase2[pivot_row, :]

    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau_phase2[:-1, i]
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            row = np.where(col == 1)[0][0]
            solution[i] = tableau_phase2[row, -1]

    optimal_value = tableau_phase2[-1, -1]
    return solution, -optimal_value