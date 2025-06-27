import React, { useState, useRef } from 'react';
import { toast } from 'react-toastify';
import { insertCustomSources } from './googleApi';
import { apiCancel } from '../../Api/api';
import { TailSpin } from 'react-loader-spinner';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import './InsertarFuentesPersonalizadas.css'; // Importar estilos personalizados si es necesario

const InsertarFuentesPersonalizadas = () => {
  const today = new Date().toISOString().split('T')[0]; // Obtener la fecha actual en formato AAAA-MM-DD

  const defaultSources = [
    "nytimes.com", "wsj.com", "bbc.com", "economist.com", "newyorker.com",
    "ap.org", "reuters.com", "bloomberg.com", "foreignaffairs.com", "theatlantic.com",
    "politico.com", "c-span.org", "csmonitor.com", "npr.org", "propublica.org",
    "eu.usatoday.com", "fair.org", "pewresearch.org", "pbs.org", "cbsnews.com",
    "theguardian.com", "edition.cnn.com", "nbcnews.com", "forbes.com", "theconversation.com",
    "upi.com", "journalistsresource.org", "snopes.com", "huffpost.com", "foxnews.com",
    "dailymail.co.uk", "factcheck.org", "politifact.com", "avclub.com", "bandcamp.com",
    "deadline.com", "heavy.com", "indiewire.com", "pitchfork.com", "rollingstone.com",
    "upworthy.com", "variety.com", "vibe.com", "vulture.com", "washingtonpost.com"
  ];

  const [fechaIni, setFechaIni] = useState(today);
  const [fechaHasta, setFechaHasta] = useState(today);
  const [sources, setSources] = useState(defaultSources);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = useRef(null);

  const handleFechaIniChange = (e) => {
    setFechaIni(e.target.value);
  };

  const handleFechaHastaChange = (e) => {
    setFechaHasta(e.target.value);
  };

  const handleSourceChange = (index, value) => {
    const newSources = [...sources];
    newSources[index] = value;
    setSources(newSources);
  };

  const handleAddSource = () => {
    setSources([...sources, '']);
  };

  const handleRemoveSource = (index) => {
    const newSources = sources.filter((_, i) => i !== index);
    setSources(newSources);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    abortControllerRef.current = new AbortController();
    const signal = abortControllerRef.current.signal;

    try {
      const response = await insertCustomSources(fechaIni, fechaHasta, sources, { signal });
      toast.success(response.message || 'Custom sources data inserted successfully');
    } catch (error) {
      if (error.name === 'AbortError') {
        toast.info('Petición cancelada');
      } else {
        console.error('Failed to insert custom sources data:', error);
        toast.error(`Error inserting data: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleCancel = async () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    try {
      await apiCancel();
      setIsLoading(false); // Detener el spinner de carga
      toast.info('Petición cancelada por el servidor');
    } catch (error) {
      toast.error('Error al cancelar la petición en el servidor');
    }
  };

  return (
    <div className="container">
      <h2 className="my-4">Insertar Fuentes Personalizadas</h2>
      {isLoading && (
        <div className="loading-overlay">
          <TailSpin color="#00BFFF" height={100} width={100} />
          <button onClick={handleCancel} className="btn btn-danger cancel-button">Cancelar</button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="data-form">
        <div className="mb-3">
          <label htmlFor="fechaIni" className="form-label">Fecha Inicial</label>
          <p className="field-description">Introduce la fecha inicial en formato AAAA-MM-DD. Este campo es obligatorio.</p>
          <input
            type="date"
            id="fechaIni"
            name="fechaIni"
            value={fechaIni}
            onChange={handleFechaIniChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="fechaHasta" className="form-label">Fecha Hasta</label>
          <p className="field-description">Introduce la fecha final en formato AAAA-MM-DD. Este campo es obligatorio.</p>
          <input
            type="date"
            id="fechaHasta"
            name="fechaHasta"
            value={fechaHasta}
            onChange={handleFechaHastaChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Fuentes</label>
          <p className="field-description">Introduce las fuentes personalizadas. Puedes agregar múltiples fuentes.</p>
          {sources.map((source, index) => (
            <div key={index} className="input-group mb-2">
              <input
                type="text"
                value={source}
                onChange={(e) => handleSourceChange(index, e.target.value)}
                className="form-control"
                required
              />
              <button
                type="button"
                className="btn btn-danger"
                onClick={() => handleRemoveSource(index)}
                disabled={sources.length === 1}
              >
                Remove
              </button>
            </div>
          ))}
          <button type="button" className="btn btn-secondary" onClick={handleAddSource}>Add Source</button>
        </div>
        <button type="submit" className="btn btn-primary button-primary" disabled={isLoading}>Insertar</button>
      </form>
    </div>
  );
};

export default InsertarFuentesPersonalizadas;
