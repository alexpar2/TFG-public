import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../Api/api';
import 'bootstrap/dist/css/bootstrap.min.css';

const SearchBar = ({ onSearch, isLoading, selectedModel, setSelectedModel }) => {
  const [query, setQuery] = useState('');
  const models = [
    'all-mpnet-base-v2',
    'paraphrase-MiniLM-L6-v2',
    'bert-base-nli-mean-tokens'
  ];

  const handleInputChange = (event) => setQuery(event.target.value);
  const handleModelChange = (event) => setSelectedModel(event.target.value);

  const handleSearch = (event) => {
    event.preventDefault();
    if (query.trim() !== '') {
      onSearch(query, selectedModel);
    }
  };

  return (
    <form onSubmit={handleSearch} className="input-group mb-3">
      <input
        type="text"
        className="form-control"
        placeholder="Search Subreddit..."
        value={query}
        onChange={handleInputChange}
        disabled={isLoading}
      />
      <select 
        className="form-select"
        value={selectedModel}
        onChange={handleModelChange}
        disabled={isLoading}
      >
        {models.map((model) => (
          <option key={model} value={model}>{model}</option>
        ))}
      </select>
      <button type="submit" className="btn btn-primary" disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Search'}
      </button>
    </form>
  );
};

const AnalysisPage = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [selectedModel, setSelectedModel] = useState('all-mpnet-base-v2');

  const handleSearch = async (query, model) => {
    console.log("Buscando:", query, "con modelo:", model);
    setIsLoading(true);
    setLoadingMessage('Loading Sentence Transformer...');

    try {
      const response = await api.get(`/analysis/api/Search/${encodeURIComponent(query)}`, {
        params: { stmodel: model }
      });
      console.log("Respuesta recibida:", response.data);
      navigate('/search-results', { state: { results: response.data, query, model } });
    } catch (error) {
      console.error("Error al realizar la búsqueda:", error);
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  return (
    <>
      <h1 className="text-center display-3 fw-bold my-4">Topic Analysis</h1>
      <SearchBar 
        onSearch={handleSearch} 
        isLoading={isLoading} 
        selectedModel={selectedModel} 
        setSelectedModel={setSelectedModel} 
      />
      {isLoading && (
        <div className="text-center mt-3">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">{loadingMessage}</p>
        </div>
      )}
      <p>Steps for Topic Analysis use:</p>
        <ol className="list-group list-group-numbered">
          <li className="list-group-item">
            Input valid subreddit name and click search. Topics will be generated and displayed as keyword groups.
          </li>
          <li className="list-group-item">
            Select any topic to view related news and AI-generated explanations.
          </li>
          <li className="list-group-item">
            Explore sentiment distribution through interactive charts.
          </li>
        </ol>
    </>
  );
};

export default AnalysisPage;
