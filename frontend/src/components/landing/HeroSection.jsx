import React from 'react';
import { motion } from 'framer-motion';
import { Play, ArrowRight, CheckCircle2, Shield } from 'lucide-react';
import Button from '../common/Button';
import { Link } from 'react-router-dom';

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center pt-24 pb-12 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[800px] bg-brand-purple/20 blur-[120px] rounded-full pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* Left Content */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div className="inline-flex items-center px-3 py-1 rounded-full glass-card border-brand-purple/30 text-brand-accent text-sm font-medium mb-4">
              <span className="w-2 h-2 rounded-full bg-brand-light mr-2 animate-pulse"></span>
              Now with 98.7% Accuracy
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
              Detect Plagiarism with <span className="text-gradient">Precision</span>
            </h1>
            
            <p className="text-lg md:text-xl text-gray-300 max-w-lg">
              ProofNexa helps students, educators, and professionals verify originality with fast and accurate document scanning. Ensure your work is truly yours.
            </p>
            
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
              <Link to="/auth?mode=signup">
                <Button variant="primary" className="w-full sm:w-auto gap-2">
                  Scan Now <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
              <Button variant="secondary" className="w-full sm:w-auto gap-2">
                <Play className="w-4 h-4" /> Watch Demo
              </Button>
            </div>
            
            <div className="flex items-center space-x-6 text-sm text-gray-400 pt-4">
              <div className="flex items-center"><CheckCircle2 className="w-4 h-4 text-brand-light mr-2"/> No credit card required</div>
              <div className="flex items-center"><CheckCircle2 className="w-4 h-4 text-brand-light mr-2"/> Free 14-day trial</div>
            </div>
          </motion.div>

          {/* Right Content - Mock Report Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative lg:h-[600px] flex items-center justify-center"
          >
            {/* Main Card */}
            <div className="glass-card w-full max-w-md rounded-2xl p-6 relative z-20 transform transition-transform hover:scale-105 duration-500">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h3 className="text-white font-semibold text-lg">Document Scan Report</h3>
                  <p className="text-sm text-gray-400">research_paper_v2.pdf</p>
                </div>
                <div className="bg-brand-purple/20 p-2 rounded-lg">
                  <Shield className="w-6 h-6 text-brand-light" />
                </div>
              </div>
              
              <div className="flex flex-col items-center justify-center py-8">
                <div className="relative w-40 h-40 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="80" cy="80" r="70" fill="none" stroke="#ffffff1a" strokeWidth="12" />
                    <circle cx="80" cy="80" r="70" fill="none" stroke="#8b5cf6" strokeWidth="12" strokeDasharray="440" strokeDashoffset="35" strokeLinecap="round" className="animate-[spin_2s_ease-in-out]" />
                  </svg>
                  <div className="absolute flex flex-col items-center">
                    <span className="text-4xl font-bold text-white">92%</span>
                    <span className="text-xs text-brand-light uppercase tracking-wider mt-1">Original</span>
                  </div>
                </div>
              </div>
              
              <div className="space-y-4 mt-4">
                <div className="bg-white/5 rounded-lg p-3 flex justify-between items-center">
                  <div className="flex items-center text-sm text-gray-300">
                    <div className="w-3 h-3 rounded-full bg-red-500 mr-3"></div>
                    Matched Sources
                  </div>
                  <span className="text-white font-medium">8%</span>
                </div>
                <div className="bg-white/5 rounded-lg p-3 flex justify-between items-center">
                  <div className="flex items-center text-sm text-gray-300">
                    <div className="w-3 h-3 rounded-full bg-green-500 mr-3"></div>
                    Citations Found
                  </div>
                  <span className="text-white font-medium">24</span>
                </div>
              </div>
            </div>
            
            {/* Decorative elements */}
            <div className="absolute top-10 right-0 w-32 h-32 bg-blue-500/20 rounded-full blur-3xl" />
            <div className="absolute bottom-10 left-0 w-40 h-40 bg-brand-purple/30 rounded-full blur-3xl" />
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
