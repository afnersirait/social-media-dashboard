import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Analytics endpoints
export const analyticsAPI = {
  getDashboardStats: () => api.get('/api/analytics/dashboard'),
  getEngagementTrends: (days = 30) => api.get(`/api/analytics/trends?days=${days}`),
  getPlatformStats: () => api.get('/api/analytics/platforms'),
  getTopPosts: (limit = 10) => api.get(`/api/analytics/top-posts?limit=${limit}`),
  getDemographics: (accountId = null) => {
    const url = accountId 
      ? `/api/analytics/demographics?account_id=${accountId}`
      : '/api/analytics/demographics'
    return api.get(url)
  }
}

// Posts endpoints
export const postsAPI = {
  getPosts: (params = {}) => api.get('/api/posts/', { params }),
  getPost: (id) => api.get(`/api/posts/${id}`),
  createPost: (data) => api.post('/api/posts/', data),
  updatePost: (id, data) => api.put(`/api/posts/${id}`, data),
  deletePost: (id) => api.delete(`/api/posts/${id}`),
  publishPost: (id) => api.post(`/api/posts/${id}/publish`),
  getScheduledPosts: () => api.get('/api/posts/scheduled'),
  updateEngagement: (id, data) => api.put(`/api/posts/${id}/engagement`, null, { params: data })
}

// Accounts endpoints
export const accountsAPI = {
  getAccounts: () => api.get('/api/accounts/'),
  getAccount: (id) => api.get(`/api/accounts/${id}`),
  createAccount: (data) => api.post('/api/accounts/', data),
  deleteAccount: (id) => api.delete(`/api/accounts/${id}`),
  getAccountAnalytics: (id, days = 30) => api.get(`/api/accounts/${id}/analytics?days=${days}`),
  addAnalytics: (id, data) => api.post(`/api/accounts/${id}/analytics`, data)
}

// Seed data (for demo)
export const seedData = () => api.post('/api/seed')

export default api
