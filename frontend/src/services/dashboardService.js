import api from "./api";

export const getDashboardStats = async () => {
  const res = await api.get("/dashboard/stats");
  return res.data;
};

export const getScanActivity = async () => {
  const res = await api.get("/dashboard/activity");
  return res.data;
};

export const getRecentScans = async () => {
  const res = await api.get("/history");
  return res.data;
};