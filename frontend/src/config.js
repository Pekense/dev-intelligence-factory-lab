export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const DASHBOARD_REFRESH_INTERVAL_SECONDS = Number(
  import.meta.env.VITE_DASHBOARD_REFRESH_INTERVAL_SECONDS || 60
);
