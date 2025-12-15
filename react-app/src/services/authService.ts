import axios from 'axios';
import { LoginRequest, AuthResponse } from '../types/auth';

const API_URL = 'http://localhost:8001';

export const authService = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const { data } = await axios.post<AuthResponse>(
      `${API_URL}/auth/login`,
      credentials
    );
    return data;
  },

  async register(userData: {
    email: string;
    full_name: string;
    password: string;
    role?: string;
    phone?: string;
    department?: string;
  }): Promise<AuthResponse> {
    const { data } = await axios.post<AuthResponse>(
      `${API_URL}/auth/register`,
      userData
    );
    return data;
  },

  async logout(token: string): Promise<void> {
    await axios.post(
      `${API_URL}/auth/logout`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );
  },

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    const { data } = await axios.post<AuthResponse>(
      `${API_URL}/auth/refresh`,
      { refresh_token: refreshToken }
    );
    return data;
  }
};