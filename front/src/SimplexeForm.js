import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

const SimplexForm = () => {
  const [numVariables, setNumVariables] = useState(2);
  const [numConstraints, setNumConstraints] = useState(3);
  const [c, setC] = useState([3, 5]);
  const [A, setA] = useState([
    [1, 0],
    [0, 2],
    [3, 2],
  ]);
  const [b, setB] = useState([4, 12, 18]);
  const [isMinimization, setIsMinimization] = useState(false);
  const [method, setMethod] = useState('simplex');
  const [solution, setSolution] = useState(null);
  const [optimalValue, setOptimalValue] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);

  const handleCChange = (e, index) => {
    const newC = [...c];
    newC[index] = Number(e.target.value);
    setC(newC);
  };

  const handleAChange = (e, rowIndex, colIndex) => {
    const newA = [...A];
    const newRow = [...newA[rowIndex]];
    newRow[colIndex] = Number(e.target.value); 
    newA[rowIndex] = newRow; 
    setA(newA); 
  };

  const handleBChange = (e, index) => {
    const newB = [...b];
    newB[index] = Number(e.target.value);
    setB(newB);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    const url = {
      simplex: 'http://127.0.0.1:5000/simplex',
      simplex_two_phases: 'http://127.0.0.1:5000/simplex_two_phases',
      BigM: 'http://127.0.0.1:5000/bigM',
    }[method];
   
    try {
      const response = await axios.post(url, {
        c: c,
        A: A,
        b: b,
        is_minimization: isMinimization,
        method: method,
      });

      setSolution(response.data.solution);
      setOptimalValue(response.data.optimal_value);
      setShowResult(true);
    } catch (err) {
      setError(err.response ? err.response.data.error : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setShowResult(false);
    setSolution(null);
    setOptimalValue(null);
  };

  const InputMatrix = ({ matrix, onChange, className, rowClassName }) => {
    return (
      <div className={className}>
        {matrix.map((row, rowIndex) => (
          <motion.div
            key={rowIndex}
            className={rowClassName}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: rowIndex * 0.1 }}
          >
            {row.map((value, colIndex) => (
              <input
                key={colIndex}
                type="number"
                value={value}
                onChange={(e) => onChange(e, rowIndex, colIndex)}
                className="w-full px-4 py-2 border rounded-md transition-all duration-300 hover:border-indigo-500 focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              />
            ))}
          </motion.div>
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 flex items-center justify-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-4xl">
        <motion.h1 
          className="text-4xl sm:text-5xl lg:text-6xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-8"
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          Résolution de Programmation Linéaire
        </motion.h1>
        
        <AnimatePresence mode="wait">
          {!showResult ? (
            <motion.form
              key="form"
              onSubmit={handleSubmit}
              className="space-y-8 bg-white shadow-xl rounded-lg p-6 sm:p-8 relative overflow-hidden"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.5 }}
            >
              <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />
              
              <div className="flex flex-wrap gap-4 items-center justify-between">
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="minimization"
                    checked={isMinimization}
                    onChange={(e) => setIsMinimization(e.target.checked)}
                    className="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <label htmlFor="minimization" className="text-lg font-semibold text-gray-700">Minimisation</label>
                </div>
                <select
                  value={method}
                  onChange={(e) => setMethod(e.target.value)}
                  className="px-4 py-2 border rounded-md text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="simplex">Simplex</option>
                  <option value="simplex_two_phases">Simplex à deux phases</option>
                  <option value="BigM">Big M</option>
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="numVariables" className="text-lg font-semibold text-gray-700">Nombre de variables</label>
                  <input
                    id="numVariables"
                    type="number"
                    value={numVariables}
                    onChange={(e) => {
                      const value = Math.max(1, parseInt(e.target.value) || 1);
                      setNumVariables(value);
                      setC(new Array(value).fill(0));
                      setA(A.map(row => new Array(value).fill(0)));
                    }}
                    min="1"
                    className="w-full px-4 py-2 border rounded-md mt-1 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label htmlFor="numConstraints" className="text-lg font-semibold text-gray-700">Nombre de contraintes</label>
                  <input
                    id="numConstraints"
                    type="number"
                    value={numConstraints}
                    onChange={(e) => {
                      const value = Math.max(1, parseInt(e.target.value) || 1);
                      setNumConstraints(value);
                      setA(new Array(value).fill(new Array(numVariables).fill(0)));
                      setB(new Array(value).fill(0));
                    }}
                    min="1"
                    className="w-full px-4 py-2 border rounded-md mt-1 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>
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
                className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-semibold rounded-md hover:from-indigo-600 hover:to-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300"
                disabled={loading}
              >
                {loading ? (
                  <svg className="animate-spin h-5 w-5 mr-3 inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : null}
                {loading ? 'Résolution en cours...' : 'Résoudre'}
              </button>
            </motion.form>
          ) : (
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.5 }}
              className="bg-white shadow-xl rounded-lg p-6 sm:p-8 space-y-6 relative overflow-hidden"
            >
              <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-green-500 via-teal-500 to-blue-500" />
              
              <motion.h2 
                className="text-3xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-blue-600"
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                Solution optimale
              </motion.h2>
              
              <motion.div 
                className="space-y-4"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                <div>
                  <h3 className="text-lg font-medium text-gray-700">Solution :</h3>
                  <p className="text-gray-600 text-xl">{solution.join(', ')}</p>
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-700">Valeur optimale :</h3>
                  <p className="text-gray-600 text-2xl font-semibold">{optimalValue}</p>
                </div>
              </motion.div>
              
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
              >
                <button 
                  onClick={resetForm}
                  className="w-full py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white font-semibold rounded-md hover:from-green-600 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-300"
                >
                  Résoudre un autre problème
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 bg-red-100 text-red-700 rounded-md"
          >
            {error}
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default SimplexForm;
