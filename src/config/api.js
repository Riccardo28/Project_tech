// API configuration
// Use environment variable or default to relative path for production
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const API_ENDPOINTS = {
  hackerNews: `${API_BASE_URL}/api/v1/hacker-news/`,
  rss: `${API_BASE_URL}/api/v1/rss/`,
};
