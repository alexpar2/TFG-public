import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
//import './customStyles.css'; 
import './bootstrap.min.css';

// Importar componentes para las rutas
import Inicio from './Inicio';
import Navbar from './Components/Navbar';
import BuscarEnGoogle from './Noticias/GoogleApi/BuscarEnGoogle';
import RedesSocialesPage from './RedesSociales/RedesSocialesPage';
import NoticiasPage from './Noticias/NoticiasPage';
import InsertarDatosSeguros from './Noticias/GoogleApi/InsertarDatosSeguros';
import VerTodosLosDatos from './Noticias/GoogleApi/VerTodosLosDatos';
import InsertarReddit from './RedesSociales/RedditApi/InsertarReddit';
import VerTodosReddit from './RedesSociales/RedditApi/VerTodosReddit';
import InsertarFuentesPersonalizadas from './Noticias/GoogleApi/InsertarFuentesPersonalizadas';
// import InsertarMastodon from './RedesSociales/MastodonApi/InsertarMastodon'; // Importa el nuevo componente
// import VerTodosMastodon from './RedesSociales/MastodonApi/VerTodosMastodon'; // Importa el nuevo componente
import GenerateTagCloud from './Visuales/TagCloud/GenerateTagCloud';
import VisualesPage from './Visuales/VisualesPage';

import AnalysisPage from './Analysis/analysisPage';
import SearchResultsPage from './Analysis/searchResultsPage';
import FakeNewsPage from './Analysis/fakenewsPage'; 


function App() {
  return (
    <Router>
      <Navbar />
      <ToastContainer />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Inicio />} />
          {/* Noticias */}
          <Route path="/noticias" element={<NoticiasPage />} />
          <Route path="/noticias/buscar-en-google" element={<BuscarEnGoogle />} />
          <Route path="/noticias/insertar-datos-seguros" element={<InsertarDatosSeguros />} />
          <Route path="/noticias/ver-datos" element={<VerTodosLosDatos />} />
          <Route path="/noticias/insertar-fuentes-personalizadas" element={<InsertarFuentesPersonalizadas />} />
          {/* Redes Sociales */}
          <Route path="/redes-sociales" element={<RedesSocialesPage />} /> 
          <Route path="/redes-sociales/reddit" element={<RedesSocialesPage showReddit={true} showMastodon={false} />} />
          <Route path="/redes-sociales/insertar-reddit" element={<InsertarReddit />} />
          <Route path="/redes-sociales/ver-todos-reddit" element={<VerTodosReddit />} />

          <Route path="/redes-sociales/mastodon" element={<RedesSocialesPage showReddit={false} showMastodon={true} />} />
          {/* <Route path="/redes-sociales/insertar-mastodon" element={<InsertarMastodon />} /> 
          <Route path="/redes-sociales/ver-todos-mastodon" element={<VerTodosMastodon />} />  */}
          {/* Visuales */}
          <Route path="/visuales" element={< VisualesPage/>} /> {/* Nueva ruta */}
          <Route path="/visuales/generar-tag-cloud" element={<GenerateTagCloud />} /> {/* Nueva ruta */}

          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/search-results" element={<SearchResultsPage />} />
          <Route path="/fakenews" element={<FakeNewsPage />} />
          {/* Puedes agregar más rutas aquí */}
        </Routes>
      </div>
    </Router>
  );
}

// function Inicio() {
//   return (
//     <div>
//       <h1>Bienvenido a Mi App</h1>
//       <p>Este es un texto introductorio de lo que sería un manual de usuario.</p>
//     </div>
//   );
// }

export default App;
