import React from 'react';

const TabButton = ({ label, isActive, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    className={`px-4 py-2 rounded-t-lg transition-colors font-medium text-sm whitespace-nowrap ${
      isActive
        ? 'bg-brand-purple text-white'
        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
    }`}
  >
    {label}
  </button>
);

const UploadTabs = ({ activeTab, setActiveTab }) => {
  return (
    <div className="flex mb-4 border-b border-gray-200">
      <TabButton
        label="Upload File"
        isActive={activeTab === 'file'}
        onClick={() => setActiveTab('file')}
      />
      <TabButton
        label="Paste Text"
        isActive={activeTab === 'text'}
        onClick={() => setActiveTab('text')}
      />
    </div>
  );
};

export default UploadTabs;
