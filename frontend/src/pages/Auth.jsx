import React from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Shield, ArrowLeft } from 'lucide-react';
import AuthForm from '../components/auth/AuthForm';

const Auth = () => {
  const [searchParams] = useSearchParams();
  const mode = searchParams.get('mode') || 'login';

  return (
    <div className="min-h-screen flex bg-brand-dark">
      {/* Left side - Branding (Hidden on mobile) */}
      <div className="hidden lg:flex lg:w-1/2 flex-col justify-between p-12 bg-gradient-to-br from-brand-darker to-brand-purple/20 relative overflow-hidden">
        {/* Decorative background elements */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-brand-purple/20 blur-[100px] rounded-full pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-500/10 blur-[100px] rounded-full pointer-events-none" />
        
        <div className="relative z-10">
          <Link to="/" className="flex items-center space-x-2 w-max">
            <Shield className="w-10 h-10 text-brand-light" />
            <span className="text-3xl font-bold text-white tracking-tight">Proof<span className="text-brand-light">Nexa</span></span>
          </Link>
        </div>

        <div className="relative z-10 my-auto">
          <div className="glass-card p-10 rounded-2xl border-l-4 border-l-brand-light max-w-lg">
            <h2 className="text-3xl font-bold text-white mb-6">Verify Originality with Confidence</h2>
            <p className="text-lg text-gray-300 leading-relaxed mb-8">
              Join thousands of professionals and educators who trust ProofNexa to ensure the authenticity of their documents through advanced text matching technology.
            </p>
            <div className="flex items-center space-x-4">
              <div className="flex -space-x-4">
                <div className="w-10 h-10 rounded-full border-2 border-brand-dark bg-purple-500"></div>
                <div className="w-10 h-10 rounded-full border-2 border-brand-dark bg-blue-500"></div>
                <div className="w-10 h-10 rounded-full border-2 border-brand-dark bg-pink-500"></div>
              </div>
              <div className="text-sm text-gray-400">
                <span className="text-white font-semibold">500k+</span> users worldwide
              </div>
            </div>
          </div>
        </div>

        <div className="relative z-10 text-sm text-gray-500">
          &copy; {new Date().getFullYear()} ProofNexa. All rights reserved.
        </div>
      </div>

      {/* Right side - Auth Form */}
      <div className="w-full lg:w-1/2 flex flex-col items-center justify-center p-8 sm:p-12 bg-white relative overflow-y-auto">
        {/* Mobile Header (Hidden on Desktop) */}
        <div className="lg:hidden absolute top-8 left-8">
          <Link to="/" className="flex items-center text-gray-500 hover:text-gray-900 transition-colors">
            <ArrowLeft className="w-5 h-5 mr-2" /> Back to home
          </Link>
        </div>
        
        <div className="lg:hidden mb-12 flex justify-center w-full mt-12">
          <Link to="/" className="flex items-center space-x-2">
            <Shield className="w-8 h-8 text-brand-purple" />
            <span className="text-2xl font-bold text-gray-900 tracking-tight">Proof<span className="text-brand-purple">Nexa</span></span>
          </Link>
        </div>

        <div className="w-full max-w-md mx-auto">
          <AuthForm initialMode={mode} />
        </div>
      </div>
    </div>
  );
};

export default Auth;
