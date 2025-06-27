import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import InsertarReddit from './RedditApi/InsertarReddit';
import VerTodosReddit from './RedditApi/VerTodosReddit';
// import InsertarMastodon from './MastodonApi/InsertarMastodon';
// import VerTodosMastodon from './MastodonApi/VerTodosMastodon';

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

function RedesSocialesPage({ showReddit }) { //despues de showReddit va showMastodon
  return (
    <div className="container mt-4">
      <div className="row">
        {/* Índice en la izquierda */}
        <div className="col-md-3 d-none d-md-block">
          <div className="index">
            <h5>Servicios</h5>
            <ul className="nav flex-column">
              {showReddit && (
                <>
                  <IndexOption
                    title="Extraer Reddit"
                    link="/redes-sociales/insertar-reddit"
                  />
                  <IndexOption
                    title="Ver Todos los Reddit"
                    link="/redes-sociales/ver-todos-reddit"
                  />
                </>
              )}
              {/* {showMastodon && (
                <>
                  <IndexOption
                    title="Extraer Mastodon"
                    link="/redes-sociales/insertar-mastodon"
                  />
                  <IndexOption
                    title="Ver Todos los Mastodon"
                    link="/redes-sociales/ver-todos-mastodon"
                  />
                </>
              )} */}
            </ul>
          </div>
        </div>

        {/* Contenido en el centro */}
        <div className="col-md-9">
          <Routes>
            {showReddit && (
              <>
                <Route path="/insertar-reddit" element={<InsertarReddit />} />
                <Route path="/ver-todos-reddit" element={<VerTodosReddit />} />
              </>
            )}
            {/* {showMastodon && (
              <>
                <Route path="/insertar-mastodon" element={<InsertarMastodon />} />
                <Route path="/ver-todos-mastodon" element={<VerTodosMastodon />} />
              </>
            )} */}
            <Route path="/" element={
              <div>
                {showReddit && (
                  <>
                    <h2 className="mb-4">Reddit</h2>
                    <ContentOption
                      title="Extraer Reddit"
                      description="Se da la Opcion de Insertar, Visualizar y Descargar en formato JSON datos de Reddit."
                      link="/redes-sociales/insertar-reddit"
                    />
                    <ContentOption
                      title="Ver Todos los Reddit"
                      description="Ver todos los datos de Reddit."
                      link="/redes-sociales/ver-todos-reddit"
                    />
                  </>
                )}
                {/* {showMastodon && (
                  <>
                    <h2 className="mb-4">Mastodon</h2>
                    <ContentOption
                      title="Extraer Mastodon"
                      description="Se da la Opcion de Insertar, Visualizar y Descargar en formato JSON datos de Mastodon."
                      link="/redes-sociales/insertar-mastodon"
                    />
                    <ContentOption
                      title="Ver Todos los Mastodon"
                      description="Ver todos los datos de Mastodon."
                      link="/redes-sociales/ver-todos-mastodon"
                    />
                  </>
                )} */}
              </div>
            } />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default RedesSocialesPage;
