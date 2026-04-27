import React from 'react';
import { Zap } from 'lucide-react';
import Button from '../common/Button';

const UpgradeCard = () => {
  return (
    <div className="bg-gradient-to-br from-brand-purple/20 to-brand-dark border border-brand-purple/30 rounded-xl p-4 mt-6">
      <div className="flex items-center space-x-2 mb-2">
        <div className="p-1.5 bg-brand-light/20 rounded-lg">
          <Zap className="w-5 h-5 text-brand-light" />
        </div>
        <h4 className="text-white font-medium text-sm">Upgrade to Pro</h4>
      </div>
      <p className="text-xs text-gray-400 mb-4 leading-relaxed">
        Get unlimited document scans, priority support, and advanced reporting features.
      </p>
      <Button variant="primary" className="w-full text-xs py-2">
        Upgrade Now
      </Button>
    </div>
  );
};

export default UpgradeCard;
