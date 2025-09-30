import axios from 'axios';
import { DEFAULT_URL } from './defaults';

const axiosInstance = axios.create({
  baseURL: DEFAULT_URL,
  withCredentials: true,
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && (error.response.status === 401 || error.response.status === 400) && !originalRequest._retry && originalRequest.url !== '/api/user/me/') {
      originalRequest._retry = true;
      try {
        await axios.get(`${DEFAULT_URL}/api/auth/refresh`, { withCredentials: true });
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
