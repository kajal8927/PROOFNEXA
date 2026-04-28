import React from 'react';
import { Shield, Mail, MessageCircle, Globe } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-brand-darker border-t border-white/10 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <Shield className="w-8 h-8 text-brand-light" />
              <span className="text-2xl font-bold text-white tracking-tight">Proof<span className="text-brand-light">Nexa</span></span>
            </Link>
            <p className="text-gray-400 max-w-sm mb-6">
              Empowering students, educators, and professionals to verify originality with fast and accurate document scanning.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-brand-light transition-colors"><Mail className="w-5 h-5" /></a>
              <a href="#" className="text-gray-400 hover:text-brand-light transition-colors"><MessageCircle className="w-5 h-5" /></a>
              <a href="#" className="text-gray-400 hover:text-brand-light transition-colors"><Globe className="w-5 h-5" /></a>
            </div>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-4">Product</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
              <li><a href="#pricing" className="hover:text-white transition-colors">Pricing</a></li>
              <li><a href="#" className="hover:text-white transition-colors">API</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Integrations</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
          <p>&copy; {new Date().getFullYear()} ProofNexa. All rights reserved.</p>
          <div className="mt-4 md:mt-0 space-x-4">
            <span>Designed for originality.</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
