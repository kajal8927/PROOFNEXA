import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Shield, LayoutDashboard, FileText, BarChart2, History, Star, Users, Settings, LogOut } from 'lucide-react';
import UpgradeCard from './UpgradeCard';

const Sidebar = ({ isOpen, setIsOpen }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [userName, setUserName] = useState('User');

  useEffect(() => {
    const storedName = localStorage.getItem('proofnexa_user');
    if (storedName) {
      setUserName(storedName);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('proofnexa_auth');
    localStorage.removeItem('proofnexa_user');
    navigate('/auth?mode=login');
  };

  const navItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard' },
    { name: 'Scan Document', icon: FileText, path: '/dashboard/scan' },
    { name: 'Reports', icon: BarChart2, path: '/dashboard/reports' },
    { name: 'History', icon: History, path: '/dashboard/history' },
    { name: 'Favorites', icon: Star, path: '/dashboard/favorites' },
    { name: 'Team', icon: Users, path: '/dashboard/team' },
    { name: 'Settings', icon: Settings, path: '/dashboard/settings' },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar Content */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-brand-darker border-r border-white/10 flex flex-col transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
        
        {/* Logo */}
        <div className="h-16 flex items-center px-6 border-b border-white/10">
          <Link to="/" className="flex items-center space-x-2">
            <Shield className="w-8 h-8 text-brand-light" />
            <span className="text-xl font-bold text-white tracking-tight">Proof<span className="text-brand-light">Nexa</span></span>
          </Link>
        </div>

        {/* Navigation */}
        <div className="flex-1 overflow-y-auto py-6 px-4 no-scrollbar">
          <nav className="space-y-1.5">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path || (item.path !== '/dashboard' && location.pathname.startsWith(item.path));
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`flex items-center px-3 py-2.5 rounded-lg transition-all duration-200 group ${
                    isActive 
                      ? 'bg-gradient-to-r from-brand-purple/20 to-transparent text-brand-light border-l-2 border-brand-light' 
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <item.icon className={`w-5 h-5 mr-3 flex-shrink-0 ${isActive ? 'text-brand-light' : 'text-gray-500 group-hover:text-gray-300'}`} />
                  <span className="font-medium text-sm">{item.name}</span>
                </Link>
              );
            })}
          </nav>
          
          <UpgradeCard />
        </div>

        {/* User Profile Mini-card */}
        <div className="p-4 border-t border-white/10">
          <div 
            onClick={handleLogout}
            className="flex items-center group cursor-pointer p-2 rounded-lg hover:bg-white/5 transition-colors"
          >
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-brand-purple to-brand-light flex items-center justify-center text-white font-bold flex-shrink-0">
              {userName.charAt(0).toUpperCase()}
            </div>
            <div className="ml-3 flex-1 overflow-hidden">
              <p className="text-sm font-medium text-white truncate">{userName}</p>
              <p className="text-xs text-gray-500 truncate">user@example.com</p>
            </div>
            <LogOut className="w-5 h-5 text-gray-500 group-hover:text-red-400 transition-colors ml-2" />
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
