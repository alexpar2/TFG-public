import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
})

export default api

export const apiCancel = async () => {
    try {
        await api.put('/api/cancel');
    } catch (error) {
        console.error('Error cancelling the request:', error);
        throw error;
    }
};

export const generateTagCloud = async (text, params) => {
    const queryString = new URLSearchParams({
        text,
        ...params
    }).toString();
    try {
        const response = await api.post(`/generate_tag_cloud/?${queryString}`, {}, { responseType: 'blob' });
        return response.data;
    } catch (error) {
        console.error('Error generating tag cloud:', error);
        throw error;
    }
};
