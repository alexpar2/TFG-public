import React from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary justify-content-center" style={{ backgroundColor: '#13344C' }}>
      <div className="container-fluid">
        TFG
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse justify-content-center" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link to="/" className="nav-link" style={{ color: '#C9E7F5' }}>Home</Link>
            </li>
            <li className="nav-item">
              <Link to="/noticias" className="nav-link" style={{ color: '#C9E7F5' }}>News</Link>
            </li>
            <li className="nav-item">
              <li><Link to="/redes-sociales/reddit" className="nav-link" style={{ color: '#C9E7F5' }}>Reddit</Link></li>
            </li>
            <li className="nav-item">
              <Link to="/visuales" className="nav-link" style={{ color: '#C9E7F5' }}>TagCloud</Link>
            </li>
            <li className="nav-item">
              <Link to="/fakenews" className="nav-link" style={{ color: '#C9E7F5' }}>Fake News</Link>
            </li>
            <li className="nav-item">
              <Link to="/analysis" className="nav-link" style={{ color: '#C9E7F5' }}>Analysis</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
