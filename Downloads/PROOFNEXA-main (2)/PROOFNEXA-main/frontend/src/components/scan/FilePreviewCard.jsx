import React from 'react';
import { FileText, X, CheckCircle, Info } from 'lucide-react';

const FilePreviewCard = ({ file, onRemove }) => {
  // Helper to format bytes
  const formatFileSize = (bytes) => {
    if (!bytes) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const fileName = typeof file === 'string' ? file : (file.name || 'Selected File');
  const fileSize = typeof file === 'string' ? 'Unknown' : (file.size ? formatFileSize(file.size) : 'Unknown');

  return (
    <div className="w-full p-4 bg-brand-purple/5 border border-brand-purple/20 rounded-2xl flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <div className="p-3 bg-white rounded-xl shadow-sm text-brand-purple">
          <FileText className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-gray-900 truncate max-w-[200px]">
            {fileName}
          </h3>
          <p className="text-xs text-gray-500">{fileSize}</p>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <div className="flex items-center text-green-600 bg-green-50 px-3 py-1.5 rounded-full text-xs font-medium border border-green-100">
          <CheckCircle className="w-3 h-3 mr-1.5" />
          Ready to scan
        </div>
        <button
          onClick={onRemove}
          className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all"
          title="Remove file"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default FilePreviewCard;
