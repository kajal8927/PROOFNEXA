import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

const NotFound = () => {
  return (
    <div className="min-h-screen bg-brand-dark flex flex-col items-center justify-center px-4 text-center">
      <h1 className="text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-brand-purple to-brand-light">404</h1>
      <h2 className="text-3xl font-semibold text-white mt-4 mb-6">Page Not Found</h2>
      <p className="text-gray-400 max-w-md mb-8">
        The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
      </p>
      <Link to="/">
        <Button variant="primary">Return Home</Button>
      </Link>
    </div>
  );
};

export default NotFound;
