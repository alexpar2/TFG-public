import React, { useState } from 'react';
import api from '../Api/api';
import 'bootstrap/dist/css/bootstrap.min.css';

// Reusable search bar component
const SearchBar = ({ query, setQuery, onSearch, isLoading }) => (
  <form
    onSubmit={e => {
      e.preventDefault();
      if (query.trim()) onSearch(query);
    }}
    className="input-group mb-4"
  >
    <input
      type="text"
      className="form-control"
      placeholder="Enter headline or short text..."
      value={query}
      onChange={e => setQuery(e.target.value)}
      disabled={isLoading}
    />
    <button
      type="submit"
      className="btn btn-primary"
      disabled={isLoading}
    >
      {isLoading ? 'Analyzing...' : 'Analyze'}
    </button>
  </form>
);

// Main fake news detection page
export default function FakeNewsPage() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (text) => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await api.get('/analysis/api/fakenews', { params: { text } });
      const { assessment, verdict, probability } = response.data;
      setResult({ assessment, verdict, probability });
    } catch (err) {
      console.error('Fake news API error:', err);
      setError('Error fetching analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Fake News Detector</h1>
      <SearchBar
        query={query}
        setQuery={setQuery}
        onSearch={handleSearch}
        isLoading={isLoading}
      />

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {result && (
        <div
          className="p-4 mb-4 border rounded bg-light text-dark"
          style={{ opacity: 0, animation: 'fadeIn 0.5s ease forwards' }}
        >
            <h4>LLM Assessment</h4>
          <p> {result.assessment}</p>
            <h4>Trained model verdict</h4>
          <p>
            The trained model assesses that the text is likely{' '}
            <strong>{result.verdict}</strong>{' '}
            with a <strong>{result.probability.toFixed(2)}%</strong> probability of being fake news.
          </p>
          <div className="progress" style={{ height: '1.5rem' }}>
            <div
              className={`progress-bar ${result.verdict === 'Fake' ? 'bg-danger' : 'bg-success'}`}
              role="progressbar"
              style={{
                width: `${result.probability}%`,
                transition: 'width 1s ease-out'
              }}
              aria-valuenow={result.probability}
              aria-valuemin="0"
              aria-valuemax="100"
            />
          </div>
        </div>
      )}

      <style>
        {`@keyframes fadeIn { to { opacity: 1; } }`}
      </style>
      <p>Warning: The result of the analysis of both the LLM and the trained model are not to be taken as definitive or truthful, but only as a guidance tool. The user should exercise caution and critical thinking when interpreting the results, and always trust their judgement before these tools. LLM analysis is usually more accurate than trained model analysis, as the former can leverage more contextual information and nuances in language than the latter.</p>
    </div>
  );
}
