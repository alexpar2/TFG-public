// src/RedesSociales/RedditApi/redditApi.js
import api from '../../Api/api'; // Asegúrate de que esta importación apunte a tu configuración de API

export const getAllRedditData = async () => {
  try {
    const response = await api.get('/api/reddit');
    return response.data;
  } catch (error) {
    console.error('Error fetching all Reddit data:', error);
    throw error;
  }
};

export const insertRedditData = async (tema, profundidad = 2, cantidad = 3, cantidad_nodo = 3) => {
    try {
      const response = await api.put(`/api/reddit/insertComent/${tema}?profundidad=${profundidad}&cantidad=${cantidad}&cantidad_nodo=${cantidad_nodo}`);
      return response.data;
    } catch (error) {
      if (error.response && error.response.data && error.response.data.detail) {
        throw new Error(error.response.data.detail); // Captura el mensaje de error del cuerpo de la respuesta
      } else {
        console.error('Error inserting Reddit comment:', error);
        throw error;
      }
    }
  };

  export const visualizeRedditData = async (tema, profundidad = 2, cantidad = 3, cantidad_nodo = 3) => {
    try {
      const response = await api.get(`/api/reddit/VisualizarComent/${tema}?profundidad=${profundidad}&cantidad=${cantidad}&cantidad_nodo=${cantidad_nodo}`);
      return response.data;
    } catch (error) {
      console.error('Error visualizing Reddit data:', error);
      throw error;
    }
  };