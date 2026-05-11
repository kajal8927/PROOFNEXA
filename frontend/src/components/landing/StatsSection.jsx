import React from 'react';
import { motion } from 'framer-motion';

const StatsSection = () => {
  const stats = [
    { value: "1M+", label: "Documents Scanned" },
    { value: "500K+", label: "Happy Users" },
    { value: "98.7%", label: "Accuracy" },
    { value: "50+", label: "Languages Supported" }
  ];

  return (
    <section className="py-20 border-y border-white/10 bg-brand-dark/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12 text-center">
          {stats.map((stat, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className="text-4xl md:text-5xl font-bold text-white mb-2">{stat.value}</div>
              <div className="text-sm md:text-base text-brand-accent font-medium uppercase tracking-wider">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;
