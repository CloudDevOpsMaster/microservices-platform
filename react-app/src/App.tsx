import { useState } from 'react';
import { Menu, X, Bell, User, Users } from 'lucide-react';
import UserListPage from './components/UserListPage';
import { PageType } from './types/pages'
import './App.css';

const App = () => {
  const [currentPage, setCurrentPage] = useState<PageType>('users');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);

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
                        className={`rounded-lg px-3 py-2 text-sm font-bold transition-all flex items-center gap-2 ${item.current
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
                  className="flex items-center gap-2 rounded-full p-1 hover:bg-yellow-100 transition-colors"
                >
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
                    <button className="block w-full text-left px-4 py-2 text-sm text-blue-900 hover:bg-yellow-50 font-medium">
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
                    className={`w-full text-left flex items-center gap-2 rounded-lg px-3 py-2 text-base font-bold ${item.current
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
                  <div className="text-base font-bold text-blue-900">Admin</div>
                  <div className="text-sm text-gray-600">admin@pmimail.com</div>
                </div>
              </div>
              <div className="mt-3 space-y-1 px-2">
                <button className="w-full text-left rounded-lg px-3 py-2 text-base font-medium text-blue-900 hover:bg-yellow-100">
                  Tu perfil
                </button>
                <button className="w-full text-left rounded-lg px-3 py-2 text-base font-medium text-blue-900 hover:bg-yellow-100">
                  Configuración
                </button>
                <button className="w-full text-left rounded-lg px-3 py-2 text-base font-medium text-blue-900 hover:bg-yellow-100">
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