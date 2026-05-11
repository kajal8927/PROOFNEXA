import React from 'react';
import { motion } from 'framer-motion';

const StatCard = ({ title, value, change, isPositive, icon: Icon, delay = 0 }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-300"
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
          <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
        </div>
        <div className="p-3 bg-brand-purple/10 rounded-xl">
          <Icon className="w-6 h-6 text-brand-purple" />
        </div>
      </div>
      
      <div className="flex items-center text-sm">
        <span className={`font-medium px-2 py-0.5 rounded-full ${isPositive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {change}
        </span>
        <span className="text-gray-500 ml-2">from last week</span>
      </div>
    </motion.div>
  );
};

export default StatCard;
