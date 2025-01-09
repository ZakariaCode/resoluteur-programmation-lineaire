import React, { useState } from 'react';
import axios from 'axios';

const SimplexForm = () => {
  const [c, setC] = useState([3, 5]);  // Coefficients de la fonction objectif
  const [A, setA] = useState([[1, 0], [0, 2], [3, 2]]);  // Coefficients des contraintes
  const [b, setB] = useState([4, 12, 18]);  // Termes constants des contraintes
  const [isMinimization, setIsMinimization] = useState(false);
  const [solution, setSolution] = useState(null);
  const [optimalValue, setOptimalValue] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      // Effectuer la requête POST vers le backend Flask (ou FastAPI)
      const response = await axios.post('http://127.0.0.1:5000/simplex_two_phases', {
        c: c,
        A: A,
        b: b,
        is_minimization: isMinimization
      });
      setSolution(response.data.solution);
      setOptimalValue(response.data.optimal_value);
    } catch (err) {
      setError(err.response ? err.response.data.error : 'Erreur inconnue');
    }
  };

  return (
    <div>
      <h1>Résolution d'un problème de programmation linéaire</h1>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>Minimisation</label>
          <input
            type="checkbox"
            checked={isMinimization}
            onChange={(e) => setIsMinimization(e.target.checked)}
          />
        </div>

        <div>
          <h2>Fonction objectif (c)</h2>
          <input
            type="text"
            value={c.join(', ')}
            onChange={(e) => setC(e.target.value.split(',').map(Number))}
          />
        </div>

        <div>
          <h2>Contraintes (A et b)</h2>
          <input
            type="text"
            value={A.map(row => row.join(', ')).join('; ')}
            onChange={(e) => setA(e.target.value.split(';').map(row => row.split(',').map(Number)))}
          />
          <input
            type="text"
            value={b.join(', ')}
            onChange={(e) => setB(e.target.value.split(',').map(Number))}
          />
        </div>

        <button type="submit">Résoudre</button>
      </form>

      {solution && (
        <div>
          <h3>Solution optimale</h3>
          <p>Solution : {solution.join(', ')}</p>
          <p>Valeur optimale : {optimalValue}</p>
        </div>
      )}

      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
};

export default SimplexForm;
