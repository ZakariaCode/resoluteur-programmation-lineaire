import numpy as np

def simplex_big_m(c, A, b, is_minimization=False):
    """
    Résout un problème de programmation linéaire avec la méthode Big M améliorée.

    :param c: Coefficients de la fonction objectif (vecteur).
    :param A: Coefficients des contraintes (matrice).
    :param b: Termes constants des contraintes (vecteur).
    :param is_minimization: Si True, le problème est une minimisation, sinon une maximisation.
    :return: Solution optimale x et valeur de la fonction objectif.
    """
    num_vars = len(c)
    num_constraints = len(A)

    # Convertir tous les inputs en numpy arrays
    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Gérer les contraintes négatives
    for i in range(len(b)):
        if b[i] < 0:
            A[i] *= -1
            b[i] *= -1

    # Ajouter des variables d'écart
    slack_vars = np.eye(num_constraints)
    A = np.hstack([A, slack_vars])
    c = np.hstack([c, np.zeros(num_constraints)])

    # Identifier les contraintes qui nécessitent des variables artificielles
    artificial_vars_needed = np.where(np.all(A[:, :num_vars] >= 0, axis=1))[0]
    num_artificial = len(artificial_vars_needed)

    if num_artificial > 0:
        M = 1e6  # Une grande valeur pour Big M
        artificial_vars = np.zeros((num_constraints, num_artificial))
        artificial_vars[artificial_vars_needed, np.arange(num_artificial)] = 1
        A = np.hstack([A, artificial_vars])
        c = np.hstack([c, np.zeros(num_artificial)])

    tableau = np.zeros((num_constraints + 1, len(c) + 1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = b
    tableau[-1, :-1] = -c if is_minimization else c

    # Mettre à jour la fonction objectif avec le facteur M pour chaque variable artificielle
    if num_artificial > 0:
        for i in artificial_vars_needed:
            tableau[-1, :] += M * tableau[i, :] if is_minimization else -M * tableau[i, :]

    while True:
        pivot_col = np.argmin(tableau[-1, :-1]) if is_minimization else np.argmax(tableau[-1, :-1])

        if (is_minimization and tableau[-1, pivot_col] >= 0) or (not is_minimization and tableau[-1, pivot_col] <= 0):
            break

        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        positive_ratios = np.where(tableau[:-1, pivot_col] > 0)[0]
        if len(positive_ratios) == 0:
            raise ValueError("Le problème est non borné.")
        pivot_row = positive_ratios[np.argmin(ratios[positive_ratios])]

        tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]
        for i in range(len(tableau)):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    # Extraire la solution
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau[:-1, i]
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            row = np.where(col == 1)[0][0]
            solution[i] = tableau[row, -1]

    optimal_value = tableau[-1, -1] if not is_minimization else -tableau[-1, -1]

    # Vérifier si des variables artificielles sont dans la base
    if num_artificial > 0:
        artificial_in_base = np.any(solution[num_vars + num_constraints:] > 1e-6)
        if artificial_in_base:
            raise ValueError("Le problème n'a pas de solution réalisable.")

    return solution[:num_vars], optimal_value