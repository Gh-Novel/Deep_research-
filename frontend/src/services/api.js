import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: '/api/research',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Research API functions
export const conductResearch = async (query, searchType = 'normal', siteCount = 5) => {
  try {
    const response = await api.post('/query', { 
      query,
      search_type: searchType,
      site_count: siteCount
    });
    return response.data;
  } catch (error) {
    console.error('Research API error:', error);
    throw error.response?.data?.detail || error.message || 'Research failed';
  }
};

export const exportReport = async (content, images, format = 'pdf') => {
  try {
    const response = await api.post('/export', { 
      content, 
      images,
      format 
    });
    return response.data;
  } catch (error) {
    console.error('Export API error:', error);
    throw error.response?.data?.detail || error.message || 'Export failed';
  }
};

export const getImages = async () => {
  try {
    const response = await api.get('/images');
    return response.data.images;
  } catch (error) {
    console.error('Get images API error:', error);
    throw error.response?.data?.detail || error.message || 'Failed to get images';
  }
};

export default {
  conductResearch,
  exportReport,
  getImages
}; 