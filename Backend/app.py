from flask import Flask, request, jsonify
import numpy as np
from simplexe import simplex
from simplexe2Phases import simplex_two_phases  # Importez vos fonctions de résolution
from flask_cors import CORS  # Importez CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This will allow requests from any origin

# Alternatively, if you want to restrict CORS to specific origins (e.g., localhost:3000)
# CORS(app, origins=["http://localhost:3000"])

# Endpoint pour résoudre un problème avec le simplexe standard
@app.route('/simplex', methods=['POST'])
def solve_simplex():
    data = request.get_json()
    c = np.array(data['c'])
    A = np.array(data['A'])
    b = np.array(data['b'])
    is_minimization = data.get('is_minimization', False)  # Par défaut, maximisation

    try:
        solution, optimal_value = simplex(c, A, b, is_minimization)
        return jsonify({
            'solution': solution.tolist(),
            'optimal_value': optimal_value
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint pour résoudre avec le simplexe à deux phases
@app.route('/simplex_two_phases', methods=['POST'])
def solve_simplex_two_phases():
    data = request.get_json()
    c = np.array(data['c'])
    A = np.array(data['A'])
    b = np.array(data['b'])
    is_minimization = data.get('is_minimization', False)  # Par défaut, maximisation

    try:
        solution, optimal_value = simplex_two_phases(c, A, b, is_minimization)
        return jsonify({
            'solution': solution.tolist(),
            'optimal_value': optimal_value
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
