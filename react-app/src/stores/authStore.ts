import { create } from 'zustand';
import { AuthUser } from '../types/auth';
import { authService } from '../services/authService';

interface AuthState {
  user: AuthUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;

  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: localStorage.getItem('access_token'),
  refreshToken: localStorage.getItem('refresh_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),
  loading: false,
  error: null,

  login: async (email: string, password: string) => {
    set({ loading: true, error: null });
    try {
      const response = await authService.login({ email, password });
      
      // Guardar tokens
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      
      set({
        user: response.user,
        accessToken: response.access_token,
        refreshToken: response.refresh_token,
        isAuthenticated: true,
        loading: false
      });
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Error al iniciar sesión',
        loading: false
      });
      throw error;
    }
  },

  logout: async () => {
    const { accessToken } = get();
    try {
      if (accessToken) {
        await authService.logout(accessToken);
      }
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    } finally {
      // Limpiar todo
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false
      });
    }
  },

  checkAuth: () => {
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
      set({
        accessToken: token,
        user: JSON.parse(user),
        isAuthenticated: true
      });
    } else {
      set({ isAuthenticated: false });
    }
  },

  clearError: () => set({ error: null })
}));