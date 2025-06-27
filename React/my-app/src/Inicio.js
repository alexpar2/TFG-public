import React from 'react';
import { Link } from 'react-router-dom';

function Inicio() {
  return (
    <div className="container mt-4 text-center">
      <h1>Trendalyzer</h1>
      <p>A centralized tool for online data extraction and analysis</p>

      <div className="mb-4 text-center bg-dark p-4 rounded">
        <p>Search for a subreddit and analyze trends news and sentiments.</p>
        <Link to="/analysis" className="btn btn-primary btn-lg d-block mx-auto">Go to Topic Analysis</Link>
      </div>

      <div className="mb-4 text-center bg-dark p-4 rounded">
        <p>Detect fake news in text.</p>
        <Link to="/fakenews" className="btn btn-primary btn-lg d-block mx-auto">Go to Fake News Detection</Link>
      </div>

      <div className="mb-4 text-center bg-dark p-4 rounded">
        <p>Extract data from Google News and analyze it or create a tag cloud.</p>
        <Link to="/noticias" className="btn btn-primary btn-lg d-block mx-auto">Go to News</Link>
      </div>

      <div className="mb-4 text-center bg-dark p-4 rounded">
        <p>Extract data from Reddit and analyze it or create a tag cloud.</p>
        <Link to="/redes-sociales/reddit" className="btn btn-primary btn-lg d-block mx-auto">Go to Reddit</Link>
      </div>

      <div className="mb-4 text-center bg-dark p-4 rounded">
        <p>Create custom tag clouds.</p>
        <Link to="/visuales" className="btn btn-primary btn-lg d-block mx-auto">Go to Visuals</Link>
      </div>
    </div>
  );
}

export default Inicio;