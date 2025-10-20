// API configuration
// Use environment variable or default to empty string for production (uses relative paths)
export const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const API_ENDPOINTS = {
  hackerNews: `${API_BASE_URL}/api/v1/hacker-news/`,
  rss: `${API_BASE_URL}/api/v1/rss/`,
};
