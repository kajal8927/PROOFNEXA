import React from 'react';
import { UploadCloud, Search, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

const HowItWorks = () => {
  const steps = [
    {
      icon: UploadCloud,
      title: "1. Upload Document",
      description: "Securely upload your document in various formats including PDF, DOCX, or TXT."
    },
    {
      icon: Search,
      title: "2. Scan & Analyze",
      description: "Our system quickly compares your text against billions of sources to detect any similarities."
    },
    {
      icon: FileText,
      title: "3. Review Report",
      description: "Get a detailed similarity report with highlighted text and links to the matched sources."
    }
  ];

  return (
    <section id="how-it-works" className="py-24 bg-brand-darker relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-sm font-bold text-brand-light tracking-wide uppercase mb-3">How It Works</h2>
          <h3 className="text-3xl md:text-4xl font-bold text-white mb-6">Three simple steps to verify originality</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
          {steps.map((step, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.2 }}
              className="flex flex-col items-center relative"
            >
              <div className="w-20 h-20 rounded-full bg-brand-dark border-2 border-brand-purple/50 flex items-center justify-center mb-6 z-10 shadow-[0_0_30px_rgba(109,40,217,0.3)]">
                <step.icon className="w-10 h-10 text-brand-light" />
              </div>
              <h4 className="text-xl font-semibold text-white mb-3">{step.title}</h4>
              <p className="text-gray-400">{step.description}</p>
              
              {/* Connector line for desktop */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-10 left-[60%] w-full h-[2px] bg-gradient-to-r from-brand-purple/50 to-transparent" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
      
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3/4 h-3/4 bg-brand-purple/10 blur-[100px] rounded-full pointer-events-none" />
    </section>
  );
};

export default HowItWorks;
