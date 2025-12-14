import { useState, useEffect } from 'react';
import { useUserStore } from '../stores/userStore';
import { 
  Users, User, ShieldCheck, Trash2, Pencil, 
  XCircle, Search, Plus, Download, Mail, 
  Phone, Building2, Calendar, CheckCircle2 
} from 'lucide-react';
import { GlassCard } from './shared/GlassCard';
import { AnimatedCounter } from './shared/AnimatedCounter';
import { UserModal } from './UserModal';

const UserListPage = () => {
  const { 
    users, 
    loading, 
    error, 
    total, 
    fetchUsers, 
    createUser,
    deleteUser, 
    clearError 
  } = useUserStore();

  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleDelete = async (userId: string) => {
    try {
      await deleteUser(userId);
      setDeleteConfirm(null);
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  const handleCreateUser = async (userData: any) => {
    await createUser(userData);
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'admin': return 'from-red-500 to-red-600';
      case 'moderator': return 'from-yellow-500 to-orange-500';
      default: return 'from-blue-500 to-blue-600';
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    const matchesStatus = statusFilter === 'all' || 
                         (statusFilter === 'active' && user.is_active) ||
                         (statusFilter === 'inactive' && !user.is_active);
    return matchesSearch && matchesRole && matchesStatus;
  });

  const stats = {
    total,
    active: users.filter(u => u.is_active).length,
    verified: users.filter(u => u.is_verified).length,
    admins: users.filter(u => u.role === 'admin').length
  };

  if (loading && users.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-20 h-20 border-4 border-red-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-xl font-bold text-gray-600">Cargando usuarios...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-white to-blue-50 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-96 h-96 bg-red-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-yellow-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      <div className="relative z-10 p-6 md:p-8 max-w-[1800px] mx-auto">
        <header className="mb-12">
          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
            <div className="flex items-center gap-6">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-500 rounded-3xl blur-xl opacity-75 animate-pulse" />
                <div className="relative w-20 h-20 rounded-2xl overflow-hidden bg-white shadow-2xl border-4 border-white/20">
                  <img src="/logo.png" alt="Toka" className="w-full h-full object-cover" />
                </div>
              </div>
              <div>
                <h1 className="text-5xl md:text-6xl font-black mb-2">
                  <span className="bg-gradient-to-r from-red-600 via-orange-500 to-yellow-400 bg-clip-text text-transparent">
                    Usuarios
                  </span>
                </h1>
                <p className="text-gray-600 text-lg font-medium flex items-center gap-2">
                  <Users className="w-5 h-5 text-red-600" />
                  Gestión de Usuarios del Sistema
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <button className="px-6 py-3 bg-white/80 backdrop-blur-xl text-gray-700 rounded-2xl hover:bg-white transition-all shadow-lg border border-gray-200 flex items-center gap-2 font-semibold">
                <Download className="w-5 h-5" />
                Exportar
              </button>
              <button 
                onClick={() => setIsModalOpen(true)}
                className="px-6 py-3 bg-gradient-to-r from-red-600 to-orange-500 text-white rounded-2xl hover:shadow-2xl transition-all shadow-lg flex items-center gap-2 font-semibold group"
              >
                <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform" />
                Nuevo Usuario
              </button>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <GlassCard className="p-6 group hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Total Usuarios
                </p>
                <h3 className="text-4xl font-black bg-gradient-to-br from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                  <AnimatedCounter value={stats.total} />
                </h3>
              </div>
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg">
                <Users className="w-7 h-7 text-white" />
              </div>
            </div>
          </GlassCard>

          <GlassCard className="p-6 group hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Activos
                </p>
                <h3 className="text-4xl font-black bg-gradient-to-br from-green-600 to-emerald-500 bg-clip-text text-transparent">
                  <AnimatedCounter value={stats.active} />
                </h3>
              </div>
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-600 to-emerald-500 flex items-center justify-center shadow-lg">
                <CheckCircle2 className="w-7 h-7 text-white" />
              </div>
            </div>
          </GlassCard>

          <GlassCard className="p-6 group hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Verificados
                </p>
                <h3 className="text-4xl font-black bg-gradient-to-br from-purple-600 to-pink-500 bg-clip-text text-transparent">
                  <AnimatedCounter value={stats.verified} />
                </h3>
              </div>
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center shadow-lg">
                <ShieldCheck className="w-7 h-7 text-white" />
              </div>
            </div>
          </GlassCard>

          <GlassCard className="p-6 group hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Administradores
                </p>
                <h3 className="text-4xl font-black bg-gradient-to-br from-red-600 to-orange-500 bg-clip-text text-transparent">
                  <AnimatedCounter value={stats.admins} />
                </h3>
              </div>
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-red-600 to-orange-500 flex items-center justify-center shadow-lg">
                <ShieldCheck className="w-7 h-7 text-white" />
              </div>
            </div>
          </GlassCard>
        </div>

        <GlassCard className="p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Buscar por nombre o email..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-white/50 backdrop-blur-xl text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
                />
              </div>
            </div>
            <div>
              <select
                value={roleFilter}
                onChange={(e) => setRoleFilter(e.target.value)}
                className="w-full px-4 py-3 bg-white/50 backdrop-blur-xl text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
              >
                <option value="all">Todos los roles</option>
                <option value="admin">Administrador</option>
                <option value="moderator">Moderador</option>
                <option value="user">Usuario</option>
              </select>
            </div>
            <div>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-4 py-3 bg-white/50 backdrop-blur-xl text-gray-700 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all outline-none font-medium"
              >
                <option value="all">Todos los estados</option>
                <option value="active">Activos</option>
                <option value="inactive">Inactivos</option>
              </select>
            </div>
          </div>
        </GlassCard>

        {error && (
          <GlassCard className="p-4 mb-6 border-l-4 border-red-500">
            <div className="flex items-start">
              <XCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
              <div className="flex-1">
                <p className="text-sm text-red-800 font-medium">{error}</p>
              </div>
              <button onClick={clearError} className="ml-3 text-red-600 hover:text-red-800 font-bold">
                ×
              </button>
            </div>
          </GlassCard>
        )}

        <UserModal 
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSubmit={handleCreateUser}
        />

        <GlassCard className="overflow-hidden relative">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-black text-gray-700 uppercase tracking-wider">
                    Usuario
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-black text-gray-700 uppercase tracking-wider">
                    Rol
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-black text-gray-700 uppercase tracking-wider">
                    Departamento
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-black text-gray-700 uppercase tracking-wider">
                    Contacto
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-black text-gray-700 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-4 text-right text-xs font-black text-gray-700 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white/50 divide-y divide-gray-200">
                {filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-16 text-center">
                      <User className="mx-auto h-16 w-16 text-gray-300 mb-4" />
                      <p className="text-lg font-bold text-gray-400">No se encontraron usuarios</p>
                      <p className="text-sm text-gray-400 mt-2">Intenta ajustar los filtros de búsqueda</p>
                    </td>
                  </tr>
                ) : (
                  filteredUsers.map((user) => (
                    <tr key={user.id} className="hover:bg-white/80 transition-colors group">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-12 w-12">
                            <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                              <User className="h-6 w-6 text-white" />
                            </div>
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-bold text-gray-900">
                              {user.full_name}
                            </div>
                            <div className="text-sm text-gray-500 flex items-center gap-1">
                              <Mail className="w-3 h-3" />
                              {user.email}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-3 py-1.5 rounded-xl text-xs font-bold bg-gradient-to-r ${getRoleBadgeColor(user.role)} text-white shadow-lg`}>
                          {user.role === 'admin' && <ShieldCheck className="w-3 h-3 mr-1" />}
                          <span className="capitalize">{user.role}</span>
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2 text-sm text-gray-600 font-medium">
                          <Building2 className="w-4 h-4" />
                          {user.department || '—'}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {user.phone ? (
                          <div className="flex items-center gap-2 text-sm text-gray-600 font-medium">
                            <Phone className="w-4 h-4" />
                            {user.phone}
                          </div>
                        ) : (
                          <span className="text-gray-400">—</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex flex-col gap-2">
                          <span className={`inline-flex items-center text-xs font-bold ${user.is_active ? 'text-green-600' : 'text-red-600'}`}>
                            <span className="w-2 h-2 rounded-full mr-2" style={{ backgroundColor: user.is_active ? '#16a34a' : '#dc2626' }} />
                            {user.is_active ? 'Activo' : 'Inactivo'}
                          </span>
                          {user.is_verified && (
                            <span className="inline-flex items-center text-xs font-bold text-blue-600">
                              <CheckCircle2 className="w-3 h-3 mr-1" />
                              Verificado
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                            title="Editar usuario"
                          >
                            <Pencil className="h-5 w-5" />
                          </button>
                          {deleteConfirm === user.id ? (
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => handleDelete(user.id)}
                                className="px-3 py-1.5 bg-red-600 text-white rounded-lg hover:bg-red-700 text-xs font-bold transition-colors"
                              >
                                Confirmar
                              </button>
                              <button
                                onClick={() => setDeleteConfirm(null)}
                                className="px-3 py-1.5 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 text-xs font-bold transition-colors"
                              >
                                Cancelar
                              </button>
                            </div>
                          ) : (
                            <button
                              onClick={() => setDeleteConfirm(user.id)}
                              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                              title="Eliminar usuario"
                            >
                              <Trash2 className="h-5 w-5" />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {loading && (
            <div className="absolute inset-0 bg-white/75 backdrop-blur-sm flex items-center justify-center z-10">
              <div className="flex flex-col items-center gap-3">
                <div className="w-12 h-12 border-4 border-red-600 border-t-transparent rounded-full animate-spin" />
                <p className="text-sm font-bold text-gray-600">Procesando...</p>
              </div>
            </div>
          )}
        </GlassCard>

        <div className="mt-6">
          <GlassCard className="p-4">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span className="font-semibold">
                Mostrando {filteredUsers.length} de {stats.total} usuarios
              </span>
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span className="font-medium">Última actualización: Ahora</span>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};

export default UserListPage;