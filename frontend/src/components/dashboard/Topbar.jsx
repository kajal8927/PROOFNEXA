import React, { useState, useEffect } from 'react';
import { Search, Bell, Settings, Menu } from 'lucide-react';

const Topbar = ({ toggleSidebar, searchQuery, setSearchQuery }) => {
  const [userInitial, setUserInitial] = useState('U');

  useEffect(() => {
    const name = localStorage.getItem('proofnexa_user') || 'User';
    setUserInitial(name.charAt(0).toUpperCase());
  }, []);
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4 sm:px-6 lg:px-8 sticky top-0 z-30">
      
      {/* Mobile Menu Button & Search */}
      <div className="flex items-center flex-1">
        <button 
          onClick={toggleSidebar}
          className="lg:hidden p-2 -ml-2 mr-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md focus:outline-none"
        >
          <Menu className="w-6 h-6" />
        </button>
        
        <div className="max-w-md w-full hidden sm:block relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="block w-full pl-10 pr-3 py-2 border border-gray-200 rounded-lg leading-5 bg-gray-50 text-gray-900 placeholder-gray-500 focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-purple/20 focus:border-brand-purple sm:text-sm transition-colors"
            placeholder="Search recent scans..."
          />
        </div>
      </div>

      {/* Right Icons & Avatar */}
      <div className="flex items-center space-x-3 sm:space-x-5">
        <button className="text-gray-400 hover:text-gray-600 transition-colors relative">
          <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
          <Bell className="w-6 h-6" />
        </button>
        
        <button className="text-gray-400 hover:text-gray-600 transition-colors hidden sm:block">
          <Settings className="w-6 h-6" />
        </button>

        <div className="h-8 w-px bg-gray-200 hidden sm:block"></div>

        <button className="flex items-center focus:outline-none">
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-brand-purple to-brand-light flex items-center justify-center text-white font-bold text-sm shadow-sm">
            {userInitial}
          </div>
        </button>
      </div>
    </header>
  );
};

export default Topbar;
