export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'user' | 'admin' | 'moderator';
  is_active: boolean;
  is_verified: boolean;
  phone?: string;
  department?: string;
  created_at: string;
  updated_at: string;
}

export interface UserListResponse {
  users: User[];
  total: number;
  skip: number;
  limit: number;
}