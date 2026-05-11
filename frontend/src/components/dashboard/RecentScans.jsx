import React from 'react';
import { motion } from 'framer-motion';
import { FileText, ArrowRight, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';

// Helper to determine badge color based on similarity percentage
const getBadgeColor = (similarity) => {
  if (similarity < 15) return 'bg-green-100 text-green-700 border-green-200';
  if (similarity < 25) return 'bg-orange-100 text-orange-700 border-orange-200';
  return 'bg-red-100 text-red-700 border-red-200';
};

/**
 * RecentScans component – displays a list of recent scan results.
 * Props:
 *   scans        – array of scan objects { id, name, similarity, time }
 *   searchQuery  – string used to filter scans by file name (case‑insensitive)
 */
const RecentScans = ({ scans = [], searchQuery = '' }) => {
  const filteredScans = scans.filter((scan) =>
    scan.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.5 }}
      className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col h-full"
    >
      {/* Header with title and "View All" link */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-lg font-bold text-gray-900">Recent Scans</h3>
          <p className="text-sm text-gray-500">Your latest verified documents</p>
        </div>
        <Link
          to="/history"
          className="text-sm font-medium text-brand-purple hover:text-brand-light transition-colors flex items-center"
        >
          View All <ArrowRight className="w-4 h-4 ml-1" />
        </Link>
      </div>

      {/* Scan list or empty state */}
      <div className="flex-1">
        {filteredScans.length > 0 ? (
          <ul className="space-y-4">
            {filteredScans.map((scan) => (
              <li
                key={scan.id}
                className="group flex items-center justify-between p-3 hover:bg-gray-50 rounded-xl transition-colors border border-transparent hover:border-gray-100"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-gray-500 group-hover:bg-white group-hover:text-brand-purple transition-colors">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900 line-clamp-1">
                      {scan.name}
                    </p>
                    <p className="text-xs text-gray-500">{scan.time}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <span
                    className={`px-2.5 py-1 text-xs font-semibold rounded-md border ${getBadgeColor(
                      scan.similarity
                    )}`}
                  >
                    {scan.similarity}% Match
                  </span>
                  <button className="text-gray-400 hover:text-brand-purple opacity-0 group-hover:opacity-100 transition-opacity">
                    <ExternalLink className="w-4 h-4" />
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center py-8">
            <FileText className="w-10 h-10 text-gray-300 mb-3" />
            <p className="text-gray-500 font-medium">No recent scans found</p>
            {searchQuery && (
              <p className="text-sm text-gray-400 mt-1">
                Try adjusting your search
              </p>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default RecentScans;
