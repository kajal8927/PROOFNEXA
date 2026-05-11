import React from 'react';

const Input = ({ label, id, type = 'text', error, ...props }) => {
  return (
    <div className="flex flex-col space-y-2 w-full">
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-gray-300">
          {label}
        </label>
      )}
      <input
        id={id}
        type={type}
        className={`bg-white/5 border ${error ? 'border-red-500' : 'border-white/10'} rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-brand-purple focus:border-transparent transition-all duration-300`}
        {...props}
      />
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
};

export default Input;
