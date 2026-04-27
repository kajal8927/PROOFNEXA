import React, { useState, useCallback } from 'react';
import { CloudUpload, X } from 'lucide-react';
import FilePreviewCard from './FilePreviewCard';

const MAX_SIZE_MB = 50;
const ALLOWED_TYPES = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = 2;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

const UploadDropzone = ({ selectedFile, setSelectedFile, setError }) => {
  const [isDragActive, setIsDragActive] = useState(false);

  const validateFile = (file) => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError('Unsupported file type. Allowed: PDF, DOCX, TXT');
      return false;
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`File exceeds ${MAX_SIZE_MB} MB size limit`);
      return false;
    }
    setError('');
    return true;
  };

  const handleFiles = (files) => {
    const file = files[0];
    if (file && validateFile(file)) {
      // Attach formatted size for preview
      const preview = {
        name: file.name,
        size: formatBytes(file.size),
        raw: file,
      };
      setSelectedFile(preview);
    }
  };

  const onDrop = useCallback(
    (e) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragActive(false);
      if (e.dataTransfer.files && e.dataTransfer.files.length) {
        handleFiles(e.dataTransfer.files);
      }
    },
    []
  );

  const onDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  };

  const onDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  };

  const onFileChange = (e) => {
    if (e.target.files && e.target.files.length) {
      handleFiles(e.target.files);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setError('');
  };

  return (
    <div className="space-y-4">
      {selectedFile ? (
        <FilePreviewCard file={selectedFile} onRemove={clearFile} />
      ) : (
        <div
          className={`border-2 border-dashed rounded-2xl p-8 text-center transition-colors ${
            isDragActive ? 'border-brand-purple bg-purple-50' : 'border-gray-300 bg-gray-50'
          }`}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
        >
          <CloudUpload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-sm text-gray-600">
            Drag & drop your file here or{' '}
            <span className="text-brand-purple underline cursor-pointer" onClick={() => document.getElementById('fileInput')?.click()}>
              browse
            </span>
          </p>
          <p className="mt-1 text-xs text-gray-500">PDF, DOCX, TXT (max {MAX_SIZE_MB} MB)</p>
          <input
            id="fileInput"
            type="file"
            accept={ALLOWED_TYPES.map((t) => t.split('/')[1]).join(',')}
            className="hidden"
            onChange={onFileChange}
          />
        </div>
      )}
    </div>
  );
};

export default UploadDropzone;
