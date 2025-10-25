import api from './api';

const transactionService = {
  getTransactions: async (filters = {}) => {
    const params = new URLSearchParams(filters).toString();
    const response = await api.get(`/transactions/transactions/?${params}`);
    return response.data;
  },

  createTransaction: async (transactionData) => {
    const response = await api.post('/transactions/transactions/', transactionData);
    return response.data;
  },

  updateTransaction: async (id, transactionData) => {
    const response = await api.patch(`/transactions/transactions/${id}/`, transactionData);
    return response.data;
  },

  deleteTransaction: async (id) => {
    await api.delete(`/transactions/transactions/${id}/`);
  },

  getSummary: async (startDate, endDate) => {
    const params = new URLSearchParams({ start_date: startDate, end_date: endDate }).toString();
    const response = await api.get(`/transactions/transactions/summary/?${params}`);
    return response.data;
  },

  getTrends: async () => {
    const response = await api.get('/transactions/transactions/trends/');
    return response.data;
  },

  getCategories: async () => {
  const response = await api.get('/transactions/categories/');
  // Check if response has results array (paginated) or is direct array
  return response.data.results || response.data;
},
};

export default transactionService;