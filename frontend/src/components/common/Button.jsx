import React from 'react';
import { motion } from 'framer-motion';

const Button = ({ children, variant = 'primary', className = '', onClick, type = 'button', ...props }) => {
  const baseStyles = "px-6 py-3 rounded-lg font-medium transition-all duration-300 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-brand-dark focus:ring-brand-purple";
  
  const variants = {
    primary: "bg-gradient-primary text-white shadow-lg shadow-brand-purple/25",
    secondary: "bg-white/10 text-white hover:bg-white/20 border border-white/10",
    outline: "border-2 border-brand-purple text-brand-accent hover:bg-brand-purple/10",
    ghost: "text-gray-300 hover:text-white hover:bg-white/10",
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      type={type}
      className={`${baseStyles} ${variants[variant]} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default Button;
