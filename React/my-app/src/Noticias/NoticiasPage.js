import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import BuscarEnGoogle from './GoogleApi/BuscarEnGoogle';
import InsertarDatosSeguros from './GoogleApi/InsertarDatosSeguros';
import VerTodosLosDatos from './GoogleApi/VerTodosLosDatos';
import InsertarFuentesPersonalizadas from './GoogleApi/InsertarFuentesPersonalizadas'; // Importar el nuevo componente

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
    <Link to={link} className="btn btn-primary button-primary">Go to {title}</Link>
  </div>
);

function NoticiasPage() {
  return (
    <div className="container mt-4">
      <div className="row">
        {/* Índice en la izquierda */}
        <div className="col-md-3 d-none d-md-block">
          <div className="index">
            <h5>Services</h5>
            <ul className="nav flex-column">
              <IndexOption
                title="Search on Google News"
                link="/noticias/buscar-en-google"
              />
              <IndexOption
                title="Extract Reliable Source Data"
                link="/noticias/insertar-datos-seguros"
              />
              <IndexOption
                title="Extract Custom Sources"
                link="/noticias/insertar-fuentes-personalizadas"
              />
              <IndexOption
                title="View All News"
                link="/noticias/ver-datos"
              />
            </ul>
          </div>
        </div>

        {/* Contenido en el centro */}
        <div className="col-md-9">
          <Routes>
            <Route path="/buscar-en-google" element={<BuscarEnGoogle />} />
            <Route path="/insertar-datos-seguros" element={<InsertarDatosSeguros />} />
            <Route path="/insertar-fuentes-personalizadas" element={<InsertarFuentesPersonalizadas />} />
            <Route path="/ver-datos" element={<VerTodosLosDatos />} />
            {/* Ruta por defecto para mostrar opciones en el centro */}
            <Route path="/" element={
              <div>
                <ContentOption
                  title="Search on Google News"
                  description="In this option you can search by topic being able to: Insert, Visualize and Download the JSON file."
                  link="/noticias/buscar-en-google"
                />
                <ContentOption
                  title="Extract Reliable Source Data"
                  description="This option allows you to insert news from a series of sources deemed 'Reliable' into the database."
                  link="/noticias/insertar-datos-seguros"
                />
                <ContentOption
                  title="Extract Custom Sources"
                  description="This option allows you to modify the sources from which information is retrieved."
                  link="/noticias/insertar-fuentes-personalizadas"
                />
                <ContentOption
                  title="View All News"
                  description="View all news stored in the database."
                  link="/noticias/ver-datos"
                />
              </div>
            } />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default NoticiasPage;
