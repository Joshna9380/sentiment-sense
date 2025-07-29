import React, { useState } from 'react';
import { analyzeText, analyzeCSV } from './api';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [csvResults, setCsvResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await analyzeText(text);
      setResult(res);
    } catch (err) {
      setError('Error analyzing text.');
    }
    setLoading(false);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleCsvSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setCsvResults(null);
    try {
      const res = await analyzeCSV(file);
      setCsvResults(res.results);
    } catch (err) {
      setError('Error analyzing CSV.');
    }
    setLoading(false);
  };

  const getBarData = (scores) => ({
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        label: 'Confidence',
        data: [scores.pos, scores.neu, scores.neg],
        backgroundColor: [
          'rgba(34,197,94,0.7)', // green
          'rgba(156,163,175,0.7)', // gray
          'rgba(239,68,68,0.7)', // red
        ],
        borderRadius: 8,
      },
    ],
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex flex-col items-center py-10 px-2">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-xl">
        <h1 className="text-4xl font-extrabold text-center text-purple-700 mb-8 tracking-tight">SentimentSense</h1>
        <form onSubmit={handleTextSubmit} className="mb-8">
          <label className="block mb-2 text-lg font-semibold text-gray-700">
            Enter text for sentiment analysis:
            <textarea
              value={text}
              onChange={e => setText(e.target.value)}
              rows={4}
              className="w-full mt-2 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
              required
            />
          </label>
          <button type="submit" disabled={loading} className="mt-3 w-full py-2 px-4 bg-purple-600 text-white font-bold rounded-lg shadow hover:bg-purple-700 transition disabled:opacity-50">
            Analyze Text
          </button>
        </form>
        {result && (
          <div className="mb-8">
            <h3 className="text-xl font-bold mb-2">Result</h3>
            <div className="flex items-center gap-4 mb-2">
              <span className={`text-lg font-semibold ${result.label === 'Positive' ? 'text-green-600' : result.label === 'Negative' ? 'text-red-500' : 'text-gray-500'}`}>{result.label}</span>
              <span className="text-gray-600">Confidence: {(result.confidence * 100).toFixed(1)}%</span>
            </div>
            <Bar
              data={getBarData(result.scores)}
              options={{
                responsive: true,
                plugins: {
                  legend: { display: false },
                  title: { display: true, text: 'Sentiment Confidence Scores' },
                },
                scales: {
                  y: { beginAtZero: true, max: 1 },
                },
              }}
              className="max-w-md mx-auto"
            />
          </div>
        )}
        <form onSubmit={handleCsvSubmit} className="mb-8">
          <label className="block mb-2 text-lg font-semibold text-gray-700">
            Upload CSV for batch analysis (must have a 'text' column):
            <input type="file" accept=".csv" onChange={handleFileChange} required className="block mt-2" />
          </label>
          <button type="submit" disabled={loading || !file} className="mt-3 w-full py-2 px-4 bg-blue-500 text-white font-bold rounded-lg shadow hover:bg-blue-600 transition disabled:opacity-50">
            Analyze CSV
          </button>
        </form>
        {csvResults && (
          <div className="overflow-x-auto">
            <h3 className="text-xl font-bold mb-2">CSV Results</h3>
            <table className="min-w-full border border-gray-300 rounded-lg overflow-hidden">
              <thead className="bg-gray-100">
                <tr>
                  <th className="py-2 px-4">Text</th>
                  <th className="py-2 px-4">Sentiment</th>
                  <th className="py-2 px-4">Confidence</th>
                </tr>
              </thead>
              <tbody>
                {csvResults.map((row, idx) => (
                  <tr key={idx} className="border-t border-gray-200">
                    <td className="py-2 px-4 max-w-xs truncate" title={row.text}>{row.text}</td>
                    <td className={`py-2 px-4 font-semibold ${row.label === 'Positive' ? 'text-green-600' : row.label === 'Negative' ? 'text-red-500' : 'text-gray-500'}`}>{row.label}</td>
                    <td className="py-2 px-4">{(row.confidence * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {error && <div className="text-red-500 mt-4 text-center font-semibold">{error}</div>}
        {loading && <div className="mt-4 text-center text-purple-600 font-bold animate-pulse">Analyzing...</div>}
      </div>
      <footer className="mt-10 text-gray-400 text-sm text-center">Made with <span className="text-pink-400">♥</span> using FastAPI & React</footer>
    </div>
  );
}

export default App;
