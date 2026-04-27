import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Landing from '../pages/Landing';
import Auth from '../pages/Auth';
import NotFound from '../pages/NotFound';
import DashboardLayout from '../layouts/DashboardLayout';
import Dashboard from '../pages/Dashboard';
import ProtectedRoute from './ProtectedRoute';

// Placeholder Pages
import Scan from '../pages/Scan';
import Reports from '../pages/Reports';
import History from '../pages/History';
import Settings from '../pages/Settings';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/auth" element={<Auth />} />
      
      {/* Protected Dashboard Routes */}
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="scan" element={<Scan />} />
          <Route path="reports" element={<Reports />} />
          <Route path="history" element={<History />} />
          <Route path="favorites" element={<div className="flex items-center justify-center h-full bg-white rounded-2xl shadow-sm border border-gray-100 p-12"><h2 className="text-2xl font-semibold text-gray-700">Favorites page coming soon</h2></div>} />
          <Route path="team" element={<div className="flex items-center justify-center h-full bg-white rounded-2xl shadow-sm border border-gray-100 p-12"><h2 className="text-2xl font-semibold text-gray-700">Team page coming soon</h2></div>} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Route>
      
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
