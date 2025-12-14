import { create } from 'zustand';
import { User, CreateUserRequest } from '../types/user';
import { userService } from '../services/userService';

interface UserState {
  users: User[];
  selectedUser: User | null;
  loading: boolean;
  error: string | null;
  total: number;
  
  fetchUsers: (skip?: number, limit?: number) => Promise<void>;
  createUser: (userData: CreateUserRequest) => Promise<void>;
  updateUser: (id: string, userData: Partial<User>) => Promise<void>;
  deleteUser: (id: string) => Promise<void>;
  clearError: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  users: [],
  selectedUser: null,
  loading: false,
  error: null,
  total: 0,

  fetchUsers: async (skip = 0, limit = 100) => {
    set({ loading: true, error: null });
    try {
      const response = await userService.getUsers(skip, limit);
      set({ users: response.users, total: response.total, loading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Error al cargar usuarios',
        loading: false 
      });
    }
  },

  createUser: async (userData: CreateUserRequest) => {
    set({ loading: true, error: null });
    try {
      const newUser = await userService.createUser(userData);
      set((state) => ({ 
        users: [...state.users, newUser],
        total: state.total + 1,
        loading: false 
      }));
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Error al crear usuario',
        loading: false 
      });
      throw error;
    }
  },

  updateUser: async (id: string, userData: Partial<User>) => {
    set({ loading: true, error: null });
    try {
      const updatedUser = await userService.updateUser(id, userData);
      set((state) => ({
        users: state.users.map(u => u.id === id ? updatedUser : u),
        loading: false
      }));
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Error al actualizar usuario',
        loading: false 
      });
      throw error;
    }
  },

  deleteUser: async (id: string) => {
    set({ loading: true, error: null });
    try {
      await userService.deleteUser(id);
      set((state) => ({
        users: state.users.filter(u => u.id !== id),
        total: state.total - 1,
        loading: false
      }));
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Error al eliminar usuario',
        loading: false 
      });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));