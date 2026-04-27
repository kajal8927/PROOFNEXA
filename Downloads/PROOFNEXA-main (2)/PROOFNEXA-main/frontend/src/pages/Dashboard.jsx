import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Search, Percent, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import StatCard from '../components/dashboard/StatCard';
import ScanActivityChart from '../components/dashboard/ScanActivityChart';
import RecentScans from '../components/dashboard/RecentScans';
import { getDashboardStats, getScanActivity, getRecentScans } from '../services/dashboardService';

const iconMap = {
  search: Search,
  percent: Percent,
  file: FileText,
  check: CheckCircle
};

const Dashboard = () => {
  const { searchQuery } = useOutletContext();
  const [userName, setUserName] = useState('User');
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [stats, setStats] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [chartPeriod, setChartPeriod] = useState('This Week');
  const [recentScans, setRecentScans] = useState([]);

  useEffect(() => {
    const name = localStorage.getItem('proofnexa_user');
    if (name) {
      setUserName(name);
    }
  }, []);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [statsRes, chartRes, scansRes] = await Promise.all([
        getDashboardStats(),
        getScanActivity(chartPeriod),
        getRecentScans()
      ]);
      setStats(statsRes);
      setChartData(chartRes);
      setRecentScans(scansRes);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Unable to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []); // Initial load

  const handlePeriodChange = async (period) => {
    setChartPeriod(period);
    try {
      const newChartData = await getScanActivity(period);
      setChartData(newChartData);
    } catch (err) {
      console.error('Failed to fetch chart data:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="mb-8">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/3"></div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-32">
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
              <div className="h-8 bg-gray-200 rounded w-1/3"></div>
            </div>
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-80"></div>
          <div className="lg:col-span-1 bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-80"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh]">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center max-w-md w-full text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">{error}</h2>
          <p className="text-gray-500 mb-6">Please check your connection and try again.</p>
          <button 
            onClick={fetchDashboardData}
            className="px-6 py-2 bg-brand-purple text-white rounded-lg hover:bg-brand-light transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Welcome back, {userName}! 👋</h1>
        <p className="text-gray-500">Here’s what’s happening with your scans today.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = iconMap[stat.iconType] || Search;
          return (
            <StatCard 
              key={index}
              title={stat.title}
              value={stat.value}
              change={stat.change}
              isPositive={stat.isPositive}
              icon={Icon}
              delay={index * 0.1}
            />
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <ScanActivityChart 
            data={chartData} 
            period={chartPeriod} 
            onPeriodChange={handlePeriodChange} 
          />
        </div>
        <div className="lg:col-span-1">
          <RecentScans 
            scans={recentScans} 
            searchQuery={searchQuery} 
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
