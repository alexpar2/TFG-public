import React, { useState, useRef } from 'react';
import { toast } from 'react-toastify';
import { insertRedditData, visualizeRedditData } from './redditApi';
import { apiCancel } from '../../Api/api';
import { TailSpin } from 'react-loader-spinner';
import 'react-toastify/dist/ReactToastify.css';
import './InsertarReddit.css';

const InsertarReddit = () => {
  const [tema, setTema] = useState('');
  const [profundidad, setProfundidad] = useState(2);
  const [cantidad, setCantidad] = useState(3);
  const [cantidadNodo, setCantidadNodo] = useState(3);
  const [isLoading, setIsLoading] = useState(false);
  const [visualData, setVisualData] = useState(null);
  const abortControllerRef = useRef(null);

  const handleTemaChange = (e) => {
    setTema(e.target.value);
  };

  const handleProfundidadChange = (e) => {
    setProfundidad(e.target.value);
  };

  const handleCantidadChange = (e) => {
    setCantidad(e.target.value);
  };

  const handleCantidadNodoChange = (e) => {
    setCantidadNodo(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    abortControllerRef.current = new AbortController();
    const signal = abortControllerRef.current.signal;

    try {
      const response = await insertRedditData(tema, profundidad, cantidad, cantidadNodo, { signal });
      toast.success(response.message || 'Reddit comment inserted successfully');
    } catch (error) {
      if (error.name === 'AbortError') {
        toast.info('Petición cancelada');
      } else {
        console.error('Failed to insert Reddit comment:', error);
        toast.error(`Error inserting data: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleVisualize = async () => {
    setIsLoading(true);
    abortControllerRef.current = new AbortController();
    const signal = abortControllerRef.current.signal;

    try {
      const data = await visualizeRedditData(tema, profundidad, cantidad, cantidadNodo, { signal });
      setVisualData(data);
      toast.success('Reddit data visualized successfully');
    } catch (error) {
      if (error.name === 'AbortError') {
        toast.info('Petición cancelada');
      } else {
        console.error('Failed to visualize Reddit data:', error);
        toast.error(`Error visualizing data: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(visualData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'visualDataReddit.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleCancel = async () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setIsLoading(false); // Añade esta línea
    try {
      await apiCancel();
      toast.info('Petición cancelada por el servidor');
    } catch (error) {
      toast.error('Error al cancelar la petición en el servidor');
    }
  };

  return (
    <div className="container">
      <h2 className="my-4">Extraer Reddit</h2>
      {isLoading && (
        <div className="loading-overlay">
          <TailSpin color="#00BFFF" height={100} width={100} />
          <button onClick={handleCancel} className="btn btn-danger cancel-button">Cancelar</button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="reddit-form">
        <div className="mb-3">
          <label htmlFor="tema" className="form-label">Tema</label>
          <p className="field-description">Introduce el tema del comentario. Este campo es obligatorio.</p>
          <input
            type="text"
            id="tema"
            name="tema"
            value={tema}
            onChange={handleTemaChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="cantidad" className="form-label">Cantidad</label>
          <p className="field-description">Número de Reddits que deseas insertar. Valor por defecto es 3.</p>
          <input
            type="number"
            id="cantidad"
            name="cantidad"
            value={cantidad}
            onChange={handleCantidadChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="profundidad" className="form-label">Profundidad</label>
          <p className="field-description">Nivel de profundidad de las respuestas en el comentario. Valor por defecto es 2.</p>
          <input
            type="number"
            id="profundidad"
            name="profundidad"
            value={profundidad}
            onChange={handleProfundidadChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="cantidadNodo" className="form-label">Cantidad por Nodo</label>
          <p className="field-description">Número de comentarios por nodo. Valor por defecto es 3.</p>
          <input
            type="number"
            id="cantidadNodo"
            name="cantidadNodo"
            value={cantidadNodo}
            onChange={handleCantidadNodoChange}
            className="form-control"
            required
          />
        </div>
        <div className="d-flex">
          <button type="submit" className="btn button-insertar" disabled={isLoading}>Insertar</button>
          <button type="button" className="btn button-visualizar" onClick={handleVisualize} disabled={isLoading}>Visualizar</button>
          <button type="button" className="btn button-descargar" onClick={handleDownload} disabled={!visualData}>Descargar JSON</button>
        </div>
      </form>

      {visualData && (
        <div className="mt-4">
          <h3>Datos Visualizados</h3>
          <pre>{JSON.stringify(visualData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default InsertarReddit;
