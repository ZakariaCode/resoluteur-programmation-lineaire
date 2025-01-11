import React, { useState } from 'react';
import axios from 'axios';

const SimplexForm = () => {
  const [numVariables, setNumVariables] = useState(2); // Nombre de variables
  const [numConstraints, setNumConstraints] = useState(3); // Nombre de contraintes
  const [c, setC] = useState([3, 5]); // Fonction objectif
  const [A, setA] = useState([
    [1, 0],
    [0, 2],
    [3, 2],
  ]); // Matrice des contraintes
  const [b, setB] = useState([4, 12, 18]); // Vecteur b
  const [isMinimization, setIsMinimization] = useState(false);
  const [method, setMethod] = useState('simplex');
  const [solution, setSolution] = useState(null);
  const [optimalValue, setOptimalValue] = useState(null);
  const [error, setError] = useState(null);

  // Mise à jour dynamique des variables c
  const handleCChange = (e, index) => {
    const newC = [...c];
    newC[index] = Number(e.target.value);
    setC(newC);
  };

  // Mise à jour dynamique de la matrice A (contraintes)
  const handleAChange = (e, rowIndex, colIndex) => {
    const newA = [...A];
    newA[rowIndex][colIndex] = Number(e.target.value);
    setA(newA);
  };

  // Mise à jour dynamique du vecteur b
  const handleBChange = (e, index) => {
    const newB = [...b];
    newB[index] = Number(e.target.value);
    setB(newB);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/simplex_auto', {
        c: c,
        A: A,
        b: b,
        is_minimization: isMinimization,
        method: method,
      });
      setSolution(response.data.solution);
      setOptimalValue(response.data.optimal_value);
    } catch (err) {
      setError(err.response ? err.response.data.error : 'Erreur inconnue');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="max-w-4xl w-full bg-white shadow-lg rounded-lg p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Résolution d'un problème de programmation linéaire</h1>
        
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Minimisation */}
          <div className="flex items-center space-x-4">
            <label className="text-lg font-semibold text-gray-700">Minimisation</label>
            <input
              type="checkbox"
              checked={isMinimization}
              onChange={(e) => setIsMinimization(e.target.checked)}
              className="h-5 w-5 text-green-500"
            />
          </div>

          {/* Choisir la méthode */}
          <div className="flex items-center space-x-4">
            <label className="text-lg font-semibold text-gray-700">Méthode</label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value)}
              className="px-4 py-2 border rounded-md text-gray-700"
            >
              <option value="simplex">Simplex</option>
              <option value="big_m">Big M</option>
            </select>
          </div>

          {/* Nombre de variables et contraintes */}
          <div className="flex space-x-4">
            <div className="flex flex-col">
              <label className="text-lg font-semibold text-gray-700">Nombre de variables</label>
              <input
                type="number"
                value={numVariables}
                onChange={(e) => {
                  setNumVariables(Number(e.target.value));
                  setC(new Array(Number(e.target.value)).fill(0)); // Réinitialiser c
                  setA(new Array(numConstraints).fill(new Array(Number(e.target.value)).fill(0))); // Réinitialiser A
                }}
                min="1"
                className="w-full px-4 py-2 border rounded-md"
              />
            </div>
            <div className="flex flex-col">
              <label className="text-lg font-semibold text-gray-700">Nombre de contraintes</label>
              <input
                type="number"
                value={numConstraints}
                onChange={(e) => {
                  setNumConstraints(Number(e.target.value));
                  setA(new Array(Number(e.target.value)).fill(new Array(numVariables).fill(0))); // Réinitialiser A
                  setB(new Array(Number(e.target.value)).fill(0)); // Réinitialiser b
                }}
                min="1"
                className="w-full px-4 py-2 border rounded-md"
              />
            </div>
          </div>

          {/* Saisie dynamique de c */}
          <div>
            <label className="text-lg font-semibold text-gray-700">Fonction objectif (c)</label>
            <div className="grid grid-cols-3 gap-4">
              {c.map((value, index) => (
                <input
                  key={index}
                  type="number"
                  value={value}
                  onChange={(e) => handleCChange(e, index)}
                  className="w-full px-4 py-2 border rounded-md"
                />
              ))}
            </div>
          </div>

          {/* Saisie dynamique de A et b */}
          <div>
            <label className="text-lg font-semibold text-gray-700">Contraintes (A et b)</label>
            {A.map((row, rowIndex) => (
              <div key={rowIndex} className="flex space-x-4 mb-4">
                {row.map((col, colIndex) => (
                  <input
                    key={colIndex}
                    type="number"
                    value={col}
                    onChange={(e) => handleAChange(e, rowIndex, colIndex)}
                    className="w-full px-4 py-2 border rounded-md"
                  />
                ))}
                <input
                  type="number"
                  value={b[rowIndex]}
                  onChange={(e) => handleBChange(e, rowIndex)}
                  className="w-full px-4 py-2 border rounded-md"
                />
              </div>
            ))}
          </div>

          <button
            type="submit"
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 focus:outline-none"
          >
            Résoudre
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
