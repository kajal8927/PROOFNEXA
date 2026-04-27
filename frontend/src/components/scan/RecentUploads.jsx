import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FileText, Clock, AlertCircle, CheckCircle, ExternalLink } from 'lucide-react';

const RecentUploads = () => {
  const navigate = useNavigate();

  const mockUploads = [
    {
      id: 1,
      name: 'Research_Paper.pdf',
      time: '2 min ago',
      score: 18,
      type: 'pdf'
    },
    {
      id: 2,
      name: 'Assignment.docx',
      time: '1 hour ago',
      score: 22,
      type: 'docx'
    },
    {
      id: 3,
      name: 'Thesis_Final.pdf',
      time: '3 hours ago',
      score: 9,
      type: 'pdf'
    },
    {
      id: 4,
      name: 'Article_Content.txt',
      time: 'Yesterday',
      score: 31,
      type: 'txt'
    }
  ];

  const getScoreColor = (score) => {
    if (score <= 15) return 'text-green-600 bg-green-50 border-green-100';
    if (score <= 25) return 'text-orange-600 bg-orange-50 border-orange-100';
    return 'text-red-600 bg-red-50 border-red-100';
  };

  const getScoreLabel = (score) => {
    if (score <= 15) return 'Low';
    if (score <= 25) return 'Medium';
    return 'High';
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-bold text-gray-900">Recent Uploads</h2>
        <button 
          onClick={() => navigate('/dashboard/history')}
          className="text-brand-purple hover:text-brand-light text-sm font-medium flex items-center transition-colors"
        >
          View All
          <ExternalLink className="w-4 h-4 ml-1" />
        </button>
      </div>

      <div className="space-y-4 flex-1 overflow-y-auto">
        {mockUploads.map((upload, index) => (
          <motion.div
            key={upload.id}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="p-3 rounded-xl border border-gray-50 hover:border-brand-purple/20 hover:bg-brand-purple/5 transition-all group"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gray-100 rounded-lg group-hover:bg-white transition-colors">
                  <FileText className="w-5 h-5 text-gray-500" />
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-900 truncate max-w-[120px]">
                    {upload.name}
                  </h3>
                  <div className="flex items-center text-xs text-gray-400 mt-1">
                    <Clock className="w-3 h-3 mr-1" />
                    {upload.time}
                  </div>
                </div>
              </div>
              <div className={`px-2 py-1 rounded text-[10px] font-bold border uppercase tracking-wider ${getScoreColor(upload.score)}`}>
                {upload.score}% {getScoreLabel(upload.score)}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default RecentUploads;
