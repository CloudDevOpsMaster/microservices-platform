export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    email: string;
    full_name: string;
    role: 'user' | 'admin' | 'moderator';
    is_verified: boolean;
  };
}

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: 'user' | 'admin' | 'moderator';
  is_verified: boolean;
}