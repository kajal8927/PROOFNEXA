import React from 'react';
import { Search, Target, Zap, Lock } from 'lucide-react';
import FeatureCard from './FeatureCard';

const FeaturesSection = () => {
  const features = [
    {
      icon: Search,
      title: "Deep Text Matching",
      description: "Our advanced scanning engine compares your document against billions of web pages and academic papers to find exact and fuzzy matches."
    },
    {
      icon: Target,
      title: "Accurate Results",
      description: "Get precise similarity scores with detailed reports highlighting matching text segments and direct links to original sources."
    },
    {
      icon: Zap,
      title: "Fast Processing",
      description: "Scan lengthy documents and research papers in seconds. Our optimized infrastructure ensures you never have to wait long for results."
    },
    {
      icon: Lock,
      title: "Secure & Private",
      description: "Your documents are encrypted and never added to our database without your explicit permission. We prioritize your data privacy."
    }
  ];

  return (
    <section id="features" className="py-24 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-sm font-bold text-brand-light tracking-wide uppercase mb-3">Core Features</h2>
          <h3 className="text-3xl md:text-4xl font-bold text-white mb-6">Built for thorough analysis</h3>
          <p className="text-gray-400 text-lg">
            Everything you need to ensure the originality of your content, packaged in an intuitive and powerful platform.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <FeatureCard 
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              delay={index * 0.1}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
