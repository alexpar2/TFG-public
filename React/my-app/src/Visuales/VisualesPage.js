import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import GenerateTagCloud from './TagCloud/GenerateTagCloud';

// Componente para representar cada opción del índice
const IndexOption = ({ title, link }) => (
  <li>
    <Link to={link} className="nav-link">{title}</Link>
  </li>
);

// Componente para representar cada opción del contenido
const ContentOption = ({ title, description, link }) => (
  <div className="mb-4">
    <h3>{title}</h3>
    <p>{description}</p>
    <Link to={link} className="btn btn-primary button-primary">Ir a {title}</Link>
  </div>
);

function VisualesPage() {
  return (
    <div className="container mt-4">
      <div className="row">
        {/* Índice en la izquierda */}
        <div className="col-md-3 d-none d-md-block">
          <div className="index">
            <h5>Servicios</h5>
            <ul className="nav flex-column">
              <IndexOption
                title="Generar Tag Cloud"
                link="/visuales/generar-tag-cloud"
              />
            </ul>
          </div>
        </div>

        {/* Contenido en el centro */}
        <div className="col-md-9">
          <Routes>
            <Route path="/generar-tag-cloud" element={<GenerateTagCloud />} />
            <Route path="/" element={
              <div>
                <ContentOption
                  title="Generar Tag Cloud"
                  description="Genera una nube de etiquetas a partir de texto proporcionado."
                  link="/visuales/generar-tag-cloud"
                />
              </div>
            } />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default VisualesPage;
