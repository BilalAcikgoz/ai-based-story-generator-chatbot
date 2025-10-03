import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const chatAPI = {
  sendMessage: async (message, sessionId = null) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        session_id: sessionId
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  checkHealth: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
};