// import React, { useState, useRef } from 'react';
// import { toast } from 'react-toastify';
// import { insertMastodonData, visualizeMastodonDataByTopic } from './mastodonApi';
// import { apiCancel } from '../../Api/api';
// import { TailSpin } from 'react-loader-spinner';
// import 'react-toastify/dist/ReactToastify.css';
// import 'bootstrap/dist/css/bootstrap.min.css';
// // import './InsertarMastodon.css'; // Asegúrate de importar el archivo CSS

// const InsertarMastodon = () => {
//   const [tema, setTema] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [visualData, setVisualData] = useState(null);
//   const abortControllerRef = useRef(null);

//   const handleTemaChange = (e) => {
//     setTema(e.target.value);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsLoading(true);
//     abortControllerRef.current = new AbortController();
//     const signal = abortControllerRef.current.signal;

//     try {
//       await insertMastodonData(tema, { signal });
//       toast.success('Mastodon data inserted successfully');
//     } catch (error) {
//       if (error.name === 'AbortError') {
//         toast.info('Petición cancelada');
//       } else {
//         console.error('Failed to insert Mastodon data:', error);
//         toast.error(`Error inserting data: ${error.message || 'Unknown error'}`);
//       }
//     } finally {
//       setIsLoading(false);
//       abortControllerRef.current = null;
//     }
//   };

//   const handleVisualize = async () => {
//     setIsLoading(true);
//     abortControllerRef.current = new AbortController();
//     const signal = abortControllerRef.current.signal;

//     try {
//       const data = await visualizeMastodonDataByTopic(tema, { signal });
//       setVisualData(data);
//       toast.success('Mastodon data visualized successfully');
//     } catch (error) {
//       if (error.name === 'AbortError') {
//         toast.info('Petición cancelada');
//       } else {
//         console.error('Failed to visualize Mastodon data:', error);
//         toast.error(`Error visualizing data: ${error.message}`);
//       }
//     } finally {
//       setIsLoading(false);
//       abortControllerRef.current = null;
//     }
//   };

//   const handleDownload = () => {
//     const blob = new Blob([JSON.stringify(visualData, null, 2)], { type: 'application/json' });
//     const url = URL.createObjectURL(blob);
//     const a = document.createElement('a');
//     a.href = url;
//     a.download = 'visualData.json';
//     a.click();
//     URL.revokeObjectURL(url);
//   };

//   const handleCancel = async () => {
//     if (abortControllerRef.current) {
//       abortControllerRef.current.abort();
//     }
//     try {
//       await apiCancel();
//       toast.info('Petición cancelada por el servidor');
//     } catch (error) {
//       toast.error('Error al cancelar la petición en el servidor');
//     }
//   };

//   return (
//     <div className="insertar-mastodon-container">
//       <h1 className="my-4">Extraer datos de Mastodon</h1>
//       {isLoading && (
//         <div className="loading-overlay">
//           <TailSpin color="#00BFFF" height={100} width={100} />
//           <button onClick={handleCancel} className="btn btn-danger cancel-button">Cancelar</button>
//         </div>
//       )}
//       <form onSubmit={handleSubmit} className="mastodon-form">
//         <div className="mb-3">
//           <label htmlFor="tema" className="form-label">Tema</label>
//           <p className="field-description">Introduce el tema de la búsqueda. Este campo es obligatorio.</p>
//           <input
//             type="text"
//             id="tema"
//             name="tema"
//             value={tema}
//             onChange={handleTemaChange}
//             className="form-control"
//             required
//           />
//         </div>
//         <div className="d-flex justify-content-center">
//           <button type="submit" className="btn button-insertar" disabled={isLoading}>Insertar</button>
//           <button type="button" className="btn button-visualizar" onClick={handleVisualize} disabled={isLoading}>Visualizar</button>
//           <button type="button" className="btn button-descargar" onClick={handleDownload} disabled={!visualData}>Descargar JSON</button>
//         </div>
//       </form>
//       {visualData && (
//         <div className="mt-4">
//           <h3>Datos Visualizados</h3>
//           <pre>{JSON.stringify(visualData, null, 2)}</pre>
//         </div>
//       )}
//     </div>
//   );
// };

// export default InsertarMastodon;
