"use client";
import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";

export default function Analytics() {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    const result = await apiClient.get("/advanced/analytics");
    if (result.success) {
      setAnalytics(result.data);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Task Analytics</h1>
      {analytics ? (
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold">Total Tasks</h2>
            <p className="text-3xl mt-2">{analytics.total_tasks}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold">Completion Rate</h2>
            <p className="text-3xl mt-2">{(analytics.completion_rate * 100).toFixed(1)}%</p>
          </div>
        </div>
      ) : (
        <p>Loading analytics...</p>
      )}
    </div>
  );
}
