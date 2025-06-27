import React, { useState, useRef } from 'react';
import { toast } from 'react-toastify';
import { insertSecure } from './googleApi';
import { apiCancel } from '../../Api/api';
import { TailSpin } from 'react-loader-spinner';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import './InsertarDatosSeguros.css';

const InsertarDatosSeguros = () => {
  const [fechaIni, setFechaIni] = useState('');
  const [fechaHasta, setFechaHasta] = useState('');
  const [cantidadWebsSeguras, setCantidadWebsSeguras] = useState(45);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = useRef(null);

  const handleFechaIniChange = (e) => {
    setFechaIni(e.target.value);
  };

  const handleFechaHastaChange = (e) => {
    setFechaHasta(e.target.value);
  };

  const handleCantidadWebsSegurasChange = (e) => {
    setCantidadWebsSeguras(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    abortControllerRef.current = new AbortController();
    const signal = abortControllerRef.current.signal;

    try {
      const response = await insertSecure(fechaIni, fechaHasta, cantidadWebsSeguras, { signal });
      toast.success(response.message || 'Google data inserted successfully');
    } catch (error) {
      if (error.name === 'AbortError') {
        toast.info('Petición cancelada');
      } else {
        console.error('Failed to insert Google data:', error);
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
      <h2 className="my-4">Insertar Datos Seguros</h2>
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
          <label htmlFor="cantidadWebsSeguras" className="form-label">Cantidad de Webs Seguras</label>
          <p className="field-description">Número de webs seguras que deseas insertar. Valor por defecto es 45.</p>
          <input
            type="number"
            id="cantidadWebsSeguras"
            name="cantidadWebsSeguras"
            value={cantidadWebsSeguras}
            onChange={handleCantidadWebsSegurasChange}
            className="form-control"
            required
          />
        </div>
        <button type="submit" className="btn btn-primary button-primary" disabled={isLoading}>Insertar</button>
      </form>
    </div>
  );
};

export default InsertarDatosSeguros;
