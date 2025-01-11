import numpy as np


def simplex_big_m(c, A, b, is_minimization=False):
    """
    Résout un problème de programmation linéaire avec la méthode Big M.
    
    :param c: Coefficients de la fonction objectif (vecteur).
    :param A: Coefficients des contraintes (matrice).
    :param b: Termes constants des contraintes (vecteur).
    :param is_minimization: Si True, le problème est une minimisation, sinon une maximisation.
    :return: Solution optimale x et valeur de la fonction objectif.
    """
    num_vars = len(c)
    num_constraints = len(A)

    for i in range(len(b)):
        if b[i] < 0:
            A[i] *= -1
            b[i] *= -1

    M = 1e6  # Une grande valeur pour Big M
    artificial_vars = np.eye(num_constraints)
    A = np.hstack([A, artificial_vars])
    c = np.hstack([c, [M] * num_constraints])

    tableau = np.zeros((num_constraints + 1, len(c) + 1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = b
    tableau[-1, :-1] = c if not is_minimization else -c

    for i in range(num_constraints):
        tableau[-1, :] -= M * tableau[i, :]

    while True:
        pivot_col = np.argmax(tableau[-1, :-1]) if not is_minimization else np.argmin(tableau[-1, :-1])

        if (not is_minimization and tableau[-1, pivot_col] <= 0) or (is_minimization and tableau[-1, pivot_col] >= 0):
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
    return solution[:num_vars], optimal_value
