import api from '../../Api/api';

// Función para buscar noticias de Google por tema
export const searchGoogleNewsByTopic = async (topic, options = {}) => {
  try {
    const response = await api.put(`/api/googlenews/insert/${topic}`, null, options); // Realiza una solicitud PUT
    return response.data; // Retorna los datos de la respuesta
  } catch (error) {
    console.error('Error fetching Google News data:', error); // Manejo de errores
    throw error; // Lanza el error para que pueda ser manejado externamente
  }
};

// Función para visualizar noticias de Google por tema
export const visualizeGoogleNewsByTopic = async (topic, options = {}) => {
  try {
    const response = await api.get(`/api/googlenews/visualizar/${topic}`, options); // Realiza una solicitud GET
    return response.data; // Retorna los datos de la respuesta
  } catch (error) {
    console.error('Error visualizing Google News data:', error); // Manejo de errores
    throw error; // Lanza el error para que pueda ser manejado externamente
  }
};

// Función para insertar datos seguros
export const insertSecure = async (fechaIni, fechaHasta, cantidadWebsSeguras) => {
  try {
    const response = await api.put(`/api/googlenews/insertSecure/list?fecha_ini=${fechaIni}&fecha_hasta=${fechaHasta}&cantidad_webs_seguras=${cantidadWebsSeguras}`); // Realiza una solicitud PUT con parámetros en la URL
    return response.data; // Retorna los datos de la respuesta
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail); // Captura el mensaje de error del cuerpo de la respuesta
    } else {
      console.error('Error inserting secure data:', error); // Manejo de errores
      throw error; // Lanza el error para que pueda ser manejado externamente
    }
  }
};

// Función para obtener todas las noticias de Google
export const getAllGoogleNews = async () => {
  try {
    const response = await api.get('/api/googlenews'); // Realiza una solicitud GET
    return response.data; // Retorna los datos de la respuesta
  } catch (error) {
    console.error('Error fetching all Google News:', error); // Manejo de errores
    throw error; // Lanza el error para que pueda ser manejado externamente
  }
};

// Función para insertar fuentes personalizadas
export const insertCustomSources = async (fechaIni, fechaHasta, sources) => {
  try {
    const response = await api.post(`/api/googlenews/insertCustomSources?fecha_ini=${fechaIni}&fecha_hasta=${fechaHasta}`, {
      sources // Pasa las fuentes personalizadas en el cuerpo de la solicitud
    });
    return response.data; // Retorna los datos de la respuesta
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      throw new Error(error.response.data.detail); // Captura el mensaje de error del cuerpo de la respuesta
    } else {
      console.error('Error inserting custom sources data:', error); // Manejo de errores
      throw error; // Lanza el error para que pueda ser manejado externamente
    }
  }
};

// Nueva función para procesar texto
export const preprocessText = async (text, params) => {
  const queryString = new URLSearchParams({
      text,
      ...params
  }).toString(); // Crea una cadena de consulta con los parámetros
  try {
      const response = await api.post(`/preprocess_text/?${queryString}`); // Realiza una solicitud POST con la cadena de consulta
      return response.data; // Retorna los datos de la respuesta
  } catch (error) {
      console.error('Error preprocessing text:', error); // Manejo de errores
      throw error; // Lanza el error para que pueda ser manejado externamente
  }
};

// Función para crear una nube de etiquetas
export const createTagCloud = async (text, maxWords) => {
  try {
    const response = await api.get(`/tag_cloud/${text}/${maxWords}`, { responseType: 'blob' }); // Realiza una solicitud GET con formato de respuesta 'blob'
    return response.data; // Retorna los datos de la respuesta
  } catch (error) {
    console.error('Error creating tag cloud:', error); // Manejo de errores
    throw error; // Lanza el error para que pueda ser manejado externamente
  }
};
