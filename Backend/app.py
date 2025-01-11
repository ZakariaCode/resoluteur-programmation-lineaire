from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS
from simplexe import simplex
from simplexe2Phases import simplex_two_phases

app = Flask(__name__)

CORS(app)

@app.route('/simplex', methods=['POST'])
def solve_simplex_auto():
    data = request.get_json()
    c = np.array(data['c'])
    A = np.array(data['A'])
    b = np.array(data['b'])
    is_minimization = data.get('is_minimization', False)

    try:
        solution, optimal_value = simplex(c, A, b, is_minimization)
        return jsonify({
            'solution': solution.tolist(),
            'optimal_value': optimal_value
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/simplex_two_phases', methods=['POST'])
def solve_simplex_two_phases():
    data = request.get_json()
    c = np.array(data['c'])
    A = np.array(data['A'])
    b = np.array(data['b'])
    is_minimization = data.get('is_minimization', False)

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
