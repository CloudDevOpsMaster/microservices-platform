import { useState, useEffect } from 'react';
import { Menu, X, Bell, User, Users, Mail, Lock, LogIn, XCircle } from 'lucide-react';
import UserListPage from './components/UserListPage';
import { useAuthStore } from './stores/authStore';
import { PageType } from './types/pages';
import './App.css';

// LoginPage component
const LoginPage = ({ onLoginSuccess }: { onLoginSuccess: () => void }) => {
  const { login, loading, error, clearError } = useAuthStore();
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(formData.email, formData.password);
      onLoginSuccess();
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
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
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
          <div className="space-y-6">
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
              type="button"
              onClick={handleSubmit}
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
          </div>

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

const App = () => {
  const { isAuthenticated, user, logout } = useAuthStore();
  const [currentPage, setCurrentPage] = useState<PageType>('login');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);

  // Check auth on mount
  useEffect(() => {
    if (isAuthenticated) {
      setCurrentPage('users');
    } else {
      setCurrentPage('login');
    }
  }, [isAuthenticated]);

  const navigation = [
    {
      name: 'Usuarios',
      page: 'users' as PageType,
      icon: Users,
      current: currentPage === 'users'
    }
  ];

  const handleNavigation = (page: PageType) => {
    setCurrentPage(page);
    setMobileMenuOpen(false);
  };

  const handleLogout = async () => {
    await logout();
    setCurrentPage('login');
    setProfileMenuOpen(false);
  };

  const handleLoginSuccess = () => {
    setCurrentPage('users');
  };

  // Show login page if not authenticated
  if (!isAuthenticated || currentPage === 'login') {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-white to-blue-50">
      {/* Navbar */}
      <nav className="bg-white/90 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b-4 border-red-600">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo y navegación desktop */}
            <div className="flex items-center">
              <div className="shrink-0">
                <div className="w-12 h-12 rounded-full overflow-hidden bg-white shadow-lg border-2 border-red-600">
                  <img
                    src="/logo.png"
                    alt="Toka"
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  {navigation.map((item) => {
                    const Icon = item.icon;
                    return (
                      <button
                        key={item.name}
                        onClick={() => handleNavigation(item.page)}
                        className={`rounded-lg px-3 py-2 text-sm font-bold transition-all flex items-center gap-2 ${
                          item.current
                            ? 'bg-red-600 text-white shadow-lg'
                            : 'text-blue-900 hover:bg-yellow-400 hover:text-blue-900'
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                        {item.name}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Iconos derecha desktop */}
            <div className="hidden md:flex items-center gap-4">
              <button className="relative rounded-full p-1 text-blue-900 hover:text-red-600 transition-colors">
                <Bell className="w-6 h-6" />
              </button>

              <div className="relative">
                <button
                  onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                  className="flex items-center gap-3 rounded-full px-3 py-1 hover:bg-yellow-100 transition-colors"
                >
                  <div className="text-right">
                    <div className="text-sm font-bold text-blue-900">{user?.full_name || 'Usuario'}</div>
                    <div className="text-xs text-gray-600">{user?.role || 'user'}</div>
                  </div>
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-red-600 to-red-700 flex items-center justify-center text-white shadow-md">
                    <User className="w-5 h-5" />
                  </div>
                </button>

                {profileMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl ring-1 ring-black/5 py-1 border-t-2 border-red-600">
                    <button className="block w-full text-left px-4 py-2 text-sm text-blue-900 hover:bg-yellow-50 font-medium">
                      Tu perfil
                    </button>
                    <button className="block w-full text-left px-4 py-2 text-sm text-blue-900 hover:bg-yellow-50 font-medium">
                      Configuración
                    </button>
                    <hr className="my-1 border-gray-200" />
                    <button 
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 font-bold"
                    >
                      Cerrar sesión
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Botón menú móvil */}
            <div className="md:hidden">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="inline-flex items-center justify-center rounded-md p-2 text-blue-900 hover:bg-yellow-100 hover:text-red-600"
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Menú móvil */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t-2 border-red-600">
            <div className="space-y-1 px-2 pt-2 pb-3">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.name}
                    onClick={() => handleNavigation(item.page)}
                    className={`w-full text-left flex items-center gap-2 rounded-lg px-3 py-2 text-base font-bold ${
                      item.current
                        ? 'bg-red-600 text-white shadow-md'
                        : 'text-blue-900 hover:bg-yellow-400 hover:text-blue-900'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {item.name}
                  </button>
                );
              })}
            </div>
            <div className="border-t border-yellow-200 pt-4 pb-3">
              <div className="flex items-center px-5 gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-red-600 to-red-700 flex items-center justify-center text-white shadow-md">
                  <User className="w-6 h-6" />
                </div>
                <div>
                  <div className="text-base font-bold text-blue-900">{user?.full_name || 'Usuario'}</div>
                  <div className="text-sm text-gray-600">{user?.email || 'usuario@toka.com'}</div>
                </div>
              </div>
              <div className="mt-3 space-y-1 px-2">
                <button className="w-full text-left rounded-lg px-3 py-2 text-base font-medium text-blue-900 hover:bg-yellow-100">
                  Tu perfil
                </button>
                <button className="w-full text-left rounded-lg px-3 py-2 text-base font-medium text-blue-900 hover:bg-yellow-100">
                  Configuración
                </button>
                <button 
                  onClick={handleLogout}
                  className="w-full text-left rounded-lg px-3 py-2 text-base font-bold text-red-600 hover:bg-red-50"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main>
        {currentPage === 'users' && <UserListPage />}
      </main>
    </div>
  );
};

export default App;