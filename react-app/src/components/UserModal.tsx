import { useState } from 'react';
import { X, User, Mail, Lock, Building2, Phone, Shield } from 'lucide-react';
import { CreateUserRequest } from '../types/user';

interface UserModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (userData: CreateUserRequest) => Promise<void>;
}

export const UserModal = ({ isOpen, onClose, onSubmit }: UserModalProps) => {
  const [formData, setFormData] = useState<CreateUserRequest>({
    email: '',
    full_name: '',
    password: '',
    role: 'user',
    phone: '',
    department: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await onSubmit(formData);
      // Reset form
      setFormData({
        email: '',
        full_name: '',
        password: '',
        role: 'user',
        phone: '',
        department: '',
      });
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al crear usuario');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div 
        className="fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />
      
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative w-full max-w-2xl bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-gray-200 p-8 animate-in fade-in zoom-in duration-300">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-black bg-gradient-to-r from-red-600 to-orange-500 bg-clip-text text-transparent">
              Nuevo Usuario
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
              <p className="text-sm text-red-800 font-medium">{error}</p>
            </div>
          )}

          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Nombre completo */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Nombre Completo *
                </label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleChange}
                    required
                    className="w-full pl-12 pr-4 py-3 bg-gray-50 text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
                    placeholder="Juan Pérez"
                  />
                </div>
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Email *
                </label>
                <div className="relative">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full pl-12 pr-4 py-3 bg-gray-50 text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
                    placeholder="juan@ejemplo.com"
                  />
                </div>
              </div>

              {/* Contraseña */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Contraseña *
                </label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    minLength={8}
                    className="w-full pl-12 pr-4 py-3 bg-gray-50 text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              {/* Rol */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Rol *
                </label>
                <div className="relative">
                  <Shield className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <select
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    className="w-full pl-12 pr-4 py-3 bg-gray-50 text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
                  >
                    <option value="user">Usuario</option>
                    <option value="moderator">Moderador</option>
                    <option value="admin">Administrador</option>
                  </select>
                </div>
              </div>

              {/* Teléfono */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Teléfono
                </label>
                <div className="relative">
                  <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full pl-12 pr-4 py-3 bg-gray-50 text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
                    placeholder="+52 123 456 7890"
                  />
                </div>
              </div>

              {/* Departamento */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Departamento
                </label>
                <div className="relative">
                  <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    name="department"
                    value={formData.department}
                    onChange={handleChange}
                    className="w-full pl-12 pr-4 py-3 bg-gray-50 text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
                    placeholder="Tecnología"
                  />
                </div>
              </div>
            </div>

            {/* Botones */}
            <div className="flex items-center justify-end gap-4 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all font-semibold"
              >
                Cancelar
              </button>
              <button
                type="button"
                onClick={handleSubmit}
                disabled={loading}
                className="px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 text-white rounded-xl hover:shadow-xl transition-all font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Creando...
                  </>
                ) : (
                  'Crear Usuario'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};