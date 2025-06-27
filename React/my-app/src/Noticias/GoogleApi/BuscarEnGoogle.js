import React, { useState, useRef } from 'react';
import { toast } from 'react-toastify';
import { searchGoogleNewsByTopic, visualizeGoogleNewsByTopic } from './googleApi';
import { apiCancel } from '../../Api/api';
import { TailSpin } from 'react-loader-spinner';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import './BuscarEnGoogle.css';
import googleLogo from './googleLogo.png';

// Componente principal para la búsqueda en Google
const BuscarEnGoogle = () => {
  // Definiendo los estados y referencias con hooks
  const [topic, setTopic] = useState(''); // Estado para el tema a buscar
  const [isLoading, setIsLoading] = useState(false); // Estado para el indicador de carga
  const [visualData, setVisualData] = useState(null); // Estado para los datos visualizados
  const abortControllerRef = useRef(null); // Referencia para controlar la cancelación de solicitudes

  // Maneja cambios en el input de tema
  const handleTopicChange = (e) => {
    setTopic(e.target.value);
  };

  // Maneja el envío del formulario de búsqueda
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true); // Indica que una solicitud está en curso
    abortControllerRef.current = new AbortController(); // Crea un nuevo controlador de aborto
    const signal = abortControllerRef.current.signal; // Obtiene la señal de aborto

    try {
      const response = await searchGoogleNewsByTopic(topic, { signal });
      toast.success(response.message || 'Google News data fetched successfully'); // Notificación de éxito
    } catch (error) {
      if (error.name === 'AbortError') {
        toast.info('Petición cancelada'); // Notificación de cancelación
      } else {
        console.error('Failed to fetch Google News data:', error);
        toast.error(`Error fetching data: ${error.message}`); // Notificación de error
      }
    } finally {
      setIsLoading(false); // Indica que la solicitud ha terminado
      abortControllerRef.current = null; // Resetea el controlador de aborto
    }
  };

  // Maneja la visualización de datos
  const handleVisualize = async () => {
    setIsLoading(true); // Indica que una solicitud está en curso
    abortControllerRef.current = new AbortController(); // Crea un nuevo controlador de aborto
    const signal = abortControllerRef.current.signal; // Obtiene la señal de aborto

    try {
      const data = await visualizeGoogleNewsByTopic(topic, { signal });
      setVisualData(data); // Almacena los datos visualizados
      toast.success('Google News data visualized successfully'); // Notificación de éxito
    } catch (error) {
      if (error.name === 'AbortError') {
        toast.info('Petición cancelada'); // Notificación de cancelación
      } else {
        console.error('Failed to visualize Google News data:', error);
        toast.error(`Error visualizing data: ${error.message}`); // Notificación de error
      }
    } finally {
      setIsLoading(false); // Indica que la solicitud ha terminado
      abortControllerRef.current = null; // Resetea el controlador de aborto
    }
  };

  // Maneja la descarga de datos visualizados
  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(visualData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob); // Crea una URL para el blob
    const a = document.createElement('a'); // Crea un elemento de anclaje
    a.href = url; // Establece la URL del blob como href del anclaje
    a.download = 'visualData.json'; // Establece el nombre del archivo a descargar
    a.click(); // Simula un clic para iniciar la descarga
    URL.revokeObjectURL(url); // Libera la URL del blob
  };

  // Maneja la cancelación de solicitudes
  const handleCancel = async () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort(); // Aborta la solicitud en curso
    }
    try {
      await apiCancel();
      toast.info('Petición cancelada por el servidor'); // Notificación de cancelación por el servidor
    } catch (error) {
      toast.error('Error al cancelar la petición en el servidor'); // Notificación de error
    }
  };

  return (
    <div className="search-container">
      <img src={googleLogo} alt="Google" className="google-logo" /> {/* Logo de Google */}
      {isLoading && (
        <div className="loading-overlay">
          <TailSpin color="#00BFFF" height={100} width={100} /> {/* Indicador de carga */}
          <button onClick={handleCancel} className="btn btn-danger cancel-button">Cancel</button> {/* Botón para cancelar */}
        </div>
      )}
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-container">
          <input
            type="text"
            id="topic"
            name="topic"
            value={topic}
            onChange={handleTopicChange}
            className="search-input"
            placeholder="Search Google News"
            required
          />
        </div>
        <div className="button-group">
          <button type="submit" className="btn btn-primary search-button" disabled={isLoading}>Search</button> {/* Botón para buscar/insertar */}
          <button type="button" className="btn btn-secondary visualize-button" onClick={handleVisualize} disabled={isLoading}>Visualize</button> {/* Botón para visualizar */}
          <button type="button" className="btn btn-success download-button" onClick={handleDownload} disabled={!visualData}>Download JSON</button> {/* Botón para descargar JSON */}
        </div>
      </form>
    </div>
  );
};

export default BuscarEnGoogle;
