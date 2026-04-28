import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Search,
  FileText,
  Percent,
  FileCheck,
  CheckCircle,
  RefreshCw,
} from "lucide-react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  getDashboardStats,
  getScanActivity,
  getRecentScans,
} from "../services/dashboardService";

const getScoreClass = (score) => {
  if (score <= 15) return "bg-green-100 text-green-700";
  if (score <= 25) return "bg-orange-100 text-orange-700";
  return "bg-red-100 text-red-700";
};

const StatCard = ({ title, value, change, icon: Icon }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <h3 className="mt-2 text-2xl font-bold text-slate-900">{value}</h3>
        </div>

        <div className="rounded-xl bg-purple-100 p-3 text-purple-600">
          <Icon className="h-5 w-5" />
        </div>
      </div>

      {change && (
        <p className="mt-4 text-sm text-slate-500">
          <span className="rounded-full bg-green-100 px-2 py-1 text-green-700">
            {change}
          </span>{" "}
          from last week
        </p>
      )}
    </motion.div>
  );
};

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [activity, setActivity] = useState([]);
  const [recentScans, setRecentScans] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const userName = localStorage.getItem("proofnexa_user") || "User";

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError("");

      const [statsData, activityData, scansData] = await Promise.all([
        getDashboardStats(),
        getScanActivity(),
        getRecentScans(),
      ]);

      setStats(statsData || null);
      setActivity(activityData || []);
      setRecentScans(scansData || []);
    } catch (err) {
      setError("Unable to load dashboard data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const filteredScans = recentScans.filter((scan) =>
    (scan.fileName || scan.name || "")
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 w-72 rounded bg-slate-200" />
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            {[1, 2, 3, 4].map((item) => (
              <div key={item} className="h-32 rounded-2xl bg-slate-200" />
            ))}
          </div>
          <div className="h-80 rounded-2xl bg-slate-200" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="rounded-2xl border border-red-100 bg-white p-10 text-center shadow-sm">
          <h2 className="text-xl font-semibold text-red-600">{error}</h2>
          <p className="mt-2 text-sm text-slate-500">
            Backend API connect hone ke baad real dashboard data show hoga.
          </p>

          <button
            onClick={fetchDashboardData}
            className="mt-6 inline-flex items-center gap-2 rounded-xl bg-purple-600 px-5 py-3 text-sm font-semibold text-white hover:bg-purple-700"
          >
            <RefreshCw className="h-4 w-4" />
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="p-8">
        <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center shadow-sm">
          <h2 className="text-xl font-semibold text-slate-800">
            No dashboard data available
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Backend se data aane ke baad dashboard update hoga.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 lg:p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">
          Welcome back, {userName}! 👋
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          Here’s what’s happening with your scans today.
        </p>
      </div>

      <div className="mb-8 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Total Scans"
          value={stats.totalScans ?? 0}
          change={stats.totalScansChange}
          icon={Search}
        />

        <StatCard
          title="Avg. Similarity"
          value={`${stats.avgSimilarity ?? 0}%`}
          change={stats.avgSimilarityChange}
          icon={Percent}
        />

        <StatCard
          title="Documents Uploaded"
          value={stats.documentsUploaded ?? 0}
          change={stats.documentsUploadedChange}
          icon={FileText}
        />

        <StatCard
          title="Accuracy"
          value={`${stats.accuracy ?? 0}%`}
          change={stats.accuracyChange}
          icon={CheckCircle}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm xl:col-span-2">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Scan Activity
              </h2>
              <p className="text-sm text-slate-500">
                Documents verified over time
              </p>
            </div>
          </div>

          {activity.length === 0 ? (
            <div className="flex h-72 items-center justify-center text-sm text-slate-400">
              No activity data available
            </div>
          ) : (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={activity}>
                  <defs>
                    <linearGradient id="scanColor" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#7c3aed" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#7c3aed" stopOpacity={0} />
                    </linearGradient>
                  </defs>

                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="scans"
                    stroke="#7c3aed"
                    strokeWidth={3}
                    fill="url(#scanColor)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Recent Scans
              </h2>
              <p className="text-sm text-slate-500">
                Your latest verified documents
              </p>
            </div>
          </div>

          <div className="mb-4 rounded-xl border border-slate-200 px-3 py-2">
            <input
              type="text"
              placeholder="Search recent scans..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
            />
          </div>

          {filteredScans.length === 0 ? (
            <div className="py-10 text-center text-sm text-slate-400">
              No recent scans available
            </div>
          ) : (
            <div className="space-y-4">
              {filteredScans.map((scan, index) => (
                <div
                  key={scan._id || index}
                  className="flex items-center justify-between rounded-xl p-3 transition hover:bg-slate-50"
                >
                  <div className="flex items-center gap-3">
                    <div className="rounded-xl bg-slate-100 p-3 text-slate-500">
                      <FileCheck className="h-5 w-5" />
                    </div>

                    <div>
                      <p className="text-sm font-semibold text-slate-900">
                        {scan.fileName || scan.name || "Untitled document"}
                      </p>
                      <p className="text-xs text-slate-500">
                        {scan.createdAt
                          ? new Date(scan.createdAt).toDateString()
                          : "Unknown date"}
                      </p>
                    </div>
                  </div>

                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${getScoreClass(
                      scan.similarityScore ?? 0
                    )}`}
                  >
                    {scan.similarityScore ?? 0}%
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}