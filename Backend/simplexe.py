import numpy as np

def simplex(c, A, b, is_minimization=False):
    """
    Résout le problème de programmation linéaire :
    Maximize ou Minimize c^T x
    Sous les contraintes Ax <= b, x >= 0

    :param c: Coefficients de la fonction objectif (vecteur).
    :param A: Coefficients des contraintes (matrice).
    :param b: Termes constants des contraintes (vecteur).
    :param is_minimization: Si True, le problème est une minimisation, sinon une maximisation.
    :return: Solution optimale x et valeur de la fonction objectif.
    """
    num_vars = len(c)
    num_constraints = len(A)
    
    # Si c'est un problème de minimisation, on inverse les signes des coefficients de la fonction objectif.
    
    # Construire la table du simplexe initiale
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    tableau[:-1, :num_vars] = A
    tableau[:-1, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
    tableau[:-1, -1] = b
    tableau[-1, :num_vars] = c

    while True:
        # Trouver la colonne pivot (colonne avec le coefficient le plus négatif pour maximisation ou le plus positif pour minimisation)
        if is_minimization:
            pivot_col = np.argmin(tableau[-1, :-1])  # Maximiser pour minimisation
        else:
            pivot_col = np.argmax(tableau[-1, :-1])  # Minimiser pour maximisation
        
        # Si tous les coefficients dans la dernière ligne sont >= 0 pour maximisation (ou <= 0 pour minimisation), on a trouvé la solution optimale
        if (is_minimization and tableau[-1, pivot_col] >= 0) or (not is_minimization and tableau[-1, pivot_col] <= 0):
            break
        
        # Trouver la ligne pivot
        ratios = tableau[:-1, -1] / tableau[:-1, pivot_col]
        pivot_row = np.where(ratios > 0, ratios, np.inf).argmin()
        
        # Effectuer l'opération de pivot
        tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]
        for i in range(len(tableau)):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    # Extraire la solution optimale
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau[:-1, i]
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            row = np.where(col == 1)[0][0]
            solution[i] = tableau[row, -1]

    optimal_value = tableau[-1, -1]
    return solution, optimal_value

# Exemple d'utilisation pour maximisation
c = np.array([3, 5])
A = np.array([[1, 0], [0, 2], [3, 2]])
b = np.array([4, 12, 18])

solution, optimal_value = simplex(c, A, b, is_minimization=False)
print(f"Solution optimale (maximisation) : {solution}")
print(f"Valeur optimale de la fonction objectif (maximisation) : {optimal_value}")

# Exemple d'utilisation pour minimisation
c_min = np.array([3, 5])
A_min = np.array([[1, 0], [0, 2], [3, 2]])
b_min = np.array([4, 12, 18])

solution_min, optimal_value_min = simplex(c_min, A_min, b_min)
print(f"Solution optimale (minimisation) : {solution_min}")
print(f"Valeur optimale de la fonction objectif (minimisation) : {optimal_value_min}")
