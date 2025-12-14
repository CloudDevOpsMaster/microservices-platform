import axios from 'axios';
import { User, UserListResponse } from '../types/user';

// Opción 1: Usar variable de entorno con fallback
// const API_URL = typeof window !== 'undefined' && (window as any).ENV?.VITE_API_URL 
//   ? (window as any).ENV.VITE_API_URL 
//   : 'http://localhost:8002';

// Opción 2: Configurar directamente (recomendado para desarrollo)
const API_URL = 'http://localhost:8002';

const api = axios.create({
  baseURL: API_URL,
  headers: { 
    'Content-Type': 'application/json' 
  },
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const userService = {
  async getUsers(skip = 0, limit = 100): Promise<UserListResponse> {
    const { data } = await api.get<UserListResponse>('/users', {
      params: { skip, limit },
    });
    return data;
  },

  async getUserById(id: string): Promise<User> {
    const { data } = await api.get<User>(`/users/${id}`);
    return data;
  },

  async createUser(userData: Partial<User>): Promise<User> {
    const { data } = await api.post<User>('/users', userData);
    return data;
  },

  async updateUser(id: string, userData: Partial<User>): Promise<User> {
    const { data } = await api.put<User>(`/users/${id}`, userData);
    return data;
  },

  async deleteUser(id: string): Promise<void> {
    await api.delete(`/users/${id}`);
  },
};