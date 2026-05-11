import React from 'react';
import { motion } from 'framer-motion';

const FeatureCard = ({ icon: Icon, title, description, delay = 0 }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      className="glass-card p-8 rounded-2xl hover:-translate-y-2 transition-transform duration-300 group"
    >
      <div className="w-14 h-14 rounded-xl bg-brand-purple/20 flex items-center justify-center mb-6 group-hover:bg-brand-purple/40 transition-colors duration-300">
        <Icon className="w-7 h-7 text-brand-light" />
      </div>
      <h3 className="text-xl font-semibold text-white mb-3">{title}</h3>
      <p className="text-gray-400 leading-relaxed">
        {description}
      </p>
    </motion.div>
  );
};

export default FeatureCard;
