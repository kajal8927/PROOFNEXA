import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Search } from "lucide-react";
import api from "../services/api"; // axios instance

const getColor = (score) => {
  if (score <= 15) return "bg-green-100 text-green-700";
  if (score <= 25) return "bg-orange-100 text-orange-700";
  return "bg-red-100 text-red-700";
};

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // 🔗 Fetch from backend
  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await api.get("/history");
        setReports(res.data || []);
      } catch (err) {
        setError("Failed to load reports");
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  // 🔍 Filter
  const filtered = reports.filter((r) =>
    r.fileName?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6">
      {/* Header */}
      <h1 className="text-2xl font-semibold text-slate-900 mb-1">Reports</h1>
      <p className="text-sm text-slate-500 mb-6">
        View and manage all your scan reports
      </p>

      {/* Search */}
      <div className="flex items-center bg-white shadow rounded-xl px-4 py-2 mb-6 border">
        <Search size={18} className="text-gray-400 mr-2" />
        <input
          type="text"
          placeholder="Search reports..."
          className="outline-none w-full text-sm text-slate-800"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* States */}
      {loading && (
        <div className="text-center py-10 text-gray-400">
          Loading reports...
        </div>
      )}

      {error && (
        <div className="text-center py-10 text-red-500">{error}</div>
      )}

      {!loading && !error && reports.length === 0 && (
        <div className="text-center py-10 text-gray-400">
          No reports available
        </div>
      )}

      {/* Table */}
      {!loading && !error && reports.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow overflow-hidden border"
        >
          <table className="w-full text-sm">
            <thead className="bg-gray-100 text-gray-600">
              <tr>
                <th className="text-left p-4">Document</th>
                <th className="text-left p-4">Date</th>
                <th className="text-left p-4">Similarity</th>
                <th className="text-right p-4">Action</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map((report, i) => (
                <tr key={i} className="border-t hover:bg-gray-50">
                  <td className="p-4 text-slate-900 font-medium">
                    {report.fileName || "Untitled"}
                  </td>

                  <td className="p-4 text-slate-600">
                    {new Date(report.createdAt).toDateString()}
                  </td>

                  <td className="p-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${getColor(
                        report.similarityScore
                      )}`}
                    >
                      {report.similarityScore}%
                    </span>
                  </td>

                  <td className="p-4 text-right">
                    <button className="text-indigo-600 hover:underline text-sm">
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      )}
    </div>
  );
}