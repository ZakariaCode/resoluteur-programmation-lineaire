import React, { useState } from 'react';
import axios from 'axios';

const SimplexForm = () => {
  const [c, setC] = useState([]);
  const [A, setA] = useState([]);
  const [b, setB] = useState([]);
  const [isMinimization, setIsMinimization] = useState(false);
  const [method, setMethod] = useState('simplex');  
  const [solution, setSolution] = useState(null);
  const [optimalValue, setOptimalValue] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);  
    const url = method === 'simplex' ? 'http://127.0.0.1:5000/simplex' : 'http://127.0.0.1:5000/simplex_two_phases'; 

    try {
      const response = await axios.post(url, {
        c: c,
        A: A,
        b: b,
        is_minimization: isMinimization,
        method: method
      });

      setSolution(response.data.solution);
      setOptimalValue(response.data.optimal_value);
    } catch (err) {
      setError(err.response ? err.response.data.error : 'Erreur inconnue');
    } finally {
      setLoading(false);  
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="max-w-4xl w-full bg-white shadow-lg rounded-lg p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Résolution d'un problème de programmation linéaire</h1>
        
        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="flex items-center space-x-4">
            <label className="text-lg font-semibold text-gray-700">Minimisation</label>
            <input
              type="checkbox"
              checked={isMinimization}
              onChange={(e) => setIsMinimization(e.target.checked)}
              className="h-5 w-5 text-green-500"
            />
          </div>

          <div className="flex flex-col space-y-4">
            <div className="flex items-center space-x-4">
              <label className="text-lg font-semibold text-gray-700">Méthode</label>
              <select
                value={method}
                onChange={(e) => setMethod(e.target.value)}
                className="px-4 py-2 border rounded-md text-gray-700"
              >
                <option value="simplex">Simplex</option>
                <option value="simplex_two_phases">Simplex à deux phases</option>
              </select>
            </div>

            <div>
              <label className="text-lg font-semibold text-gray-700">Fonction objectif (c)</label>
              <input
                type="text"
                value={c.join(', ')}
                onChange={(e) => setC(e.target.value.split(',').map(Number))}
                className="w-full px-4 py-2 border rounded-md"
                placeholder="Entrez les coefficients de la fonction objectif, par exemple : 3, 5"
              />
            </div>

            <div>
              <label className="text-lg font-semibold text-gray-700">Contraintes (A et b)</label>
              <input
                type="text"
                value={A.map(row => row.join(', ')).join('; ')}
                onChange={(e) => setA(e.target.value.split(';').map(row => row.split(',').map(Number)))}
                className="w-full px-4 py-2 border rounded-md"
                placeholder="Entrez les coefficients de A, par exemple : 1, 0; 0, 2; 3, 2"
              />
              <input
                type="text"
                value={b.join(', ')}
                onChange={(e) => setB(e.target.value.split(',').map(Number))}
                className="w-full mt-4 px-4 py-2 border rounded-md"
                placeholder="Entrez les valeurs de b, par exemple : 4, 12, 18"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 focus:outline-none"
            disabled={loading}  
          >
            {loading ? 'Chargement...' : 'Résoudre'}
          </button>
        </form>

        {solution && (
          <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-md">
            <h3 className="text-xl font-semibold text-gray-700">Solution optimale</h3>
            <p className="text-gray-800">Solution : {solution.join(', ')}</p>
            <p className="text-gray-800">Valeur optimale : {optimalValue}</p>
          </div>
        )}

        {error && <div className="mt-4 text-red-600 bg-red-100 p-4 rounded-md">{error}</div>}
      </div>
    </div>
  );
};

export default SimplexForm;
