import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CloudUpload, FileText, ArrowRight } from 'lucide-react';
import UploadTabs from '../components/scan/UploadTabs';
import UploadDropzone from '../components/scan/UploadDropzone';
import PasteTextBox from '../components/scan/PasteTextBox';
import RecentUploads from '../components/scan/RecentUploads';

const Scan = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('file'); // 'file' or 'text'
  const [selectedFile, setSelectedFile] = useState(null);
  const [pasteText, setPasteText] = useState('');
  const [error, setError] = useState('');

  const handleScan = () => {
    if (activeTab === 'file') {
      if (!selectedFile) {
        setError('Please select a file to scan');
        return;
      }
      navigate('/scan-progress', { state: { file: selectedFile } });
    } else {
      if (pasteText.trim().length < 50) {
        setError('Please enter at least 50 characters');
        return;
      }
      navigate('/scan-progress', { state: { text: pasteText } });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col lg:flex-row gap-6"
    >
      {/* Left side - main upload area */}
      <div className="flex-1 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Scan Document</h1>
        <p className="text-gray-500 mb-6">
          Upload your document or paste text to check originality.
        </p>
        <UploadTabs activeTab={activeTab} setActiveTab={setActiveTab} />
        {activeTab === 'file' ? (
          <UploadDropzone
            selectedFile={selectedFile}
            setSelectedFile={setSelectedFile}
            setError={setError}
          />
        ) : (
          <PasteTextBox
            pasteText={pasteText}
            setPasteText={setPasteText}
            setError={setError}
          />
        )}
        {error && (
          <div className="mt-2 text-sm text-red-600" role="alert">
            {error}
          </div>
        )}
        <button
          onClick={handleScan}
          className="mt-4 w-full sm:w-auto px-6 py-2 bg-brand-purple text-white rounded-lg hover:bg-brand-light transition-colors flex items-center justify-center"
        >
          {activeTab === 'file' ? 'Scan Now' : 'Scan Text'}
        </button>
      </div>

      {/* Right side - recent uploads */}
      <div className="lg:w-80">
        <RecentUploads />
      </div>
    </motion.div>
  );
};

export default Scan;
