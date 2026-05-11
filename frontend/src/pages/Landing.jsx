import React from 'react';
import Navbar from '../components/common/Navbar';
import Footer from '../components/common/Footer';
import HeroSection from '../components/landing/HeroSection';
import FeaturesSection from '../components/landing/FeaturesSection';
import HowItWorks from '../components/landing/HowItWorks';
import StatsSection from '../components/landing/StatsSection';

const Landing = () => {
  return (
    <div className="min-h-screen flex flex-col bg-brand-dark">
      <Navbar />
      <main className="flex-grow">
        <HeroSection />
        <FeaturesSection />
        <HowItWorks />
        <StatsSection />
        {/* Testimonials section could go here */}
      </main>
      <Footer />
    </div>
  );
};

export default Landing;
