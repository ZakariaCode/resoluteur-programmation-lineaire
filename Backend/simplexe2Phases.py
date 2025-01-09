import numpy as np

def simplex_two_phases(c, A, b, is_minimization=False):
    num_vars = len(c)
    num_constraints = len(A)

    # Phase 1: Construction de la table du simplexe avec les variables artificielles
    tableau_phase1 = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    
    # Construire la matrice avec les variables artificielles
    tableau_phase1[:-1, :num_vars] = A
    tableau_phase1[:-1, num_vars:num_vars + num_constraints] = np.eye(num_constraints)  # Variables artificielles
    tableau_phase1[:-1, -1] = b

    # Fonction objectif pour phase 1: minimiser la somme des variables artificielles
    tableau_phase1[-1, num_vars:num_vars + num_constraints] = np.ones(num_constraints)

    # Phase 1: Trouver une solution faisable
    while True:
        pivot_col = np.argmin(tableau_phase1[-1, :-1]) if is_minimization else np.argmax(tableau_phase1[-1, :-1])
        
        # Si tous les coefficients dans la dernière ligne sont >= 0 (minimisation) ou <= 0 (maximisation), on a trouvé une solution faisable
        if (is_minimization and tableau_phase1[-1, pivot_col] >= 0) or (not is_minimization and tableau_phase1[-1, pivot_col] <= 0):
            break
        
        # Calcul des ratios tout en évitant les divisions par zéro
        ratios = np.where(tableau_phase1[:-1, pivot_col] > 0, tableau_phase1[:-1, -1] / tableau_phase1[:-1, pivot_col], np.inf)
        pivot_row = np.where(ratios == np.min(ratios))[0][0]
        
        # Effectuer l'opération de pivot pour la phase 1
        tableau_phase1[pivot_row, :] /= tableau_phase1[pivot_row, pivot_col]
        for i in range(len(tableau_phase1)):
            if i != pivot_row:
                tableau_phase1[i, :] -= tableau_phase1[i, pivot_col] * tableau_phase1[pivot_row, :]

    # Vérifier si le problème est faisable
    if np.sum(tableau_phase1[-1, num_vars:num_vars + num_constraints]) > 0:
        raise ValueError("Le problème n'a pas de solution faisable.")

    # Phase 2: Construction de la table du simplexe avec la fonction objectif d'origine
    tableau_phase2 = tableau_phase1.copy()
    tableau_phase2[-1, :num_vars] = c  # Fonction objectif originale (maximisation ou minimisation)
    tableau_phase2[-1, num_vars:num_vars + num_constraints] = 0  # Les variables artificielles n'ont plus d'impact en phase 2

    # Phase 2: Résoudre le problème original
    while True:
        pivot_col = np.argmin(tableau_phase2[-1, :-1]) if is_minimization else np.argmax(tableau_phase2[-1, :-1])
        
        # Si tous les coefficients dans la dernière ligne sont >= 0 (minimisation) ou <= 0 (maximisation), on a trouvé la solution optimale
        if (is_minimization and tableau_phase2[-1, pivot_col] >= 0) or (not is_minimization and tableau_phase2[-1, pivot_col] <= 0):
            break
        
        ratios = np.where(tableau_phase2[:-1, pivot_col] > 0, tableau_phase2[:-1, -1] / tableau_phase2[:-1, pivot_col], np.inf)
        pivot_row = np.where(ratios == np.min(ratios))[0][0]
        
        # Effectuer l'opération de pivot pour la phase 2
        tableau_phase2[pivot_row, :] /= tableau_phase2[pivot_row, pivot_col]
        for i in range(len(tableau_phase2)):
            if i != pivot_row:
                tableau_phase2[i, :] -= tableau_phase2[i, pivot_col] * tableau_phase2[pivot_row, :]

    # Extraire la solution optimale de la phase 2
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau_phase2[:-1, i]
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            row = np.where(col == 1)[0][0]
            solution[i] = tableau_phase2[row, -1]

    optimal_value = tableau_phase2[-1, -1]
    return solution, optimal_value

# Exemple d'utilisation pour maximisation
c = np.array([3, 5])
A = np.array([[1, 0], [0, 2], [3, 2]])
b = np.array([4, 12, 18])

try:
    solution, optimal_value = simplex_two_phases(c, A, b, is_minimization=False)
    print(f"Solution optimale (maximisation) : {solution}")
    print(f"Valeur optimale de la fonction objectif (maximisation) : {optimal_value}")
except ValueError as e:
    print(e)

# Exemple d'utilisation pour minimisation
c_min = np.array([3, 5])
A_min = np.array([[1, 0], [0, 2], [3, 2]])
b_min = np.array([4, 12, 18])

try:
    solution_min, optimal_value_min = simplex_two_phases(c_min, A_min, b_min)
    print(f"Solution optimale (minimisation) : {solution_min}")
    print(f"Valeur optimale de la fonction objectif (minimisation) : {optimal_value_min}")
except ValueError as e:
    print(e)
