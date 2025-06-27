// import api from '../../Api/api';

// export const getAllMastodonData = async () => {
//   try {
//     const response = await api.get('/api/mastodon');
//     return response.data;
//   } catch (error) {
//     console.error('Error fetching Mastodon data:', error);
//     throw error;
//   }
// };

// export const insertMastodonData = async (tema, options = {}) => {
//   try {
//     await api.put(`/api/mastodon/insert/${tema}`, null, options);
//   } catch (error) {
//     console.error('Error inserting Mastodon data:', error);
//     throw error;
//   }
// };

// export const visualizeMastodonDataByTopic = async (tema, options = {}) => {
//   try {
//     const response = await api.get(`/api/mastodon/visualizar/${tema}`, options);
//     return response.data;
//   } catch (error) {
//     console.error('Error visualizing Mastodon data:', error);
//     throw error;
//   }
// };
