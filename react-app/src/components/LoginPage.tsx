import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { Mail, Lock, LogIn, XCircle } from 'lucide-react';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login, loading, error, clearError, isAuthenticated } = useAuthStore();
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  // Redirect si ya está autenticado
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/users');
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(formData.email, formData.password);
      navigate('/users');
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
    if (error) clearError();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-white to-blue-50 relative overflow-hidden flex items-center justify-center p-4">
      {/* Background effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-96 h-96 bg-red-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-yellow-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Card */}
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-gray-200 p-8 md:p-10">
          {/* Logo y Header */}
          <div className="text-center mb-8">
            <div className="relative mx-auto w-24 h-24 mb-6">
              <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-500 rounded-3xl blur-xl opacity-75 animate-pulse" />
              <div className="relative w-24 h-24 rounded-2xl overflow-hidden bg-white shadow-2xl border-4 border-white/20">
                <img src="/logo.png" alt="Toka" className="w-full h-full object-cover" />
              </div>
            </div>
            
            <h1 className="text-4xl md:text-5xl font-black mb-2">
              <span className="bg-gradient-to-r from-red-600 via-orange-500 to-yellow-400 bg-clip-text text-transparent">
                Bienvenido
              </span>
            </h1>
            <p className="text-gray-600 font-medium">
              Inicia sesión para continuar
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg animate-in fade-in slide-in-from-top duration-300">
              <div className="flex items-start">
                <XCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-sm text-red-800 font-medium">{error}</p>
                </div>
                <button onClick={clearError} className="ml-3 text-red-600 hover:text-red-800 font-bold">
                  ×
                </button>
              </div>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Email
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
                  placeholder="tu@email.com"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Contraseña
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
                  disabled={loading}
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-red-600 to-orange-500 text-white rounded-xl hover:shadow-2xl transition-all shadow-lg flex items-center justify-center gap-2 font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed group"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Iniciando sesión...
                </>
              ) : (
                <>
                  <LogIn className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  Iniciar Sesión
                </>
              )}
            </button>
          </form>

          {/* Footer */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500">
              Sistema de Gestión Toka
            </p>
          </div>
        </div>

        {/* Demo credentials hint */}
        <div className="mt-6 p-4 bg-blue-50/80 backdrop-blur-xl rounded-2xl border border-blue-200">
          <p className="text-xs text-blue-800 font-semibold text-center">
            💡 Demo: admin@toka.com / Admin123456
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;