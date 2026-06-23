import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  CartesianGrid, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { FiClock, FiTrendingUp, FiActivity } from 'react-icons/fi';
import { MdTimer } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';
import useTimeTracker from '../hooks/useTimeTracker';

const COLORS = [
  '#3b82f6', '#10b981', '#f59e0b',
  '#ef4444', '#8b5cf6', '#ec4899',
  '#14b8a6', '#f97316'
];

const PAGE_LABELS = {
  dashboard: '🏠 Dashboard',
  courses: '📚 Courses',
  lesson: '📖 Lessons',
  quiz: '📝 Quizzes',
  performance: '📊 Performance',
  recommendations: '⭐ AI Picks',
  chatbot: '🤖 SmartBot',
  leaderboard: '🏆 Leaderboard',
  time_analytics: '⏱️ Time',
};

const TimeAnalytics = () => {
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  useTimeTracker('time_analytics');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/login'); return; }
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    try {
      const res = await api.get('/timelog/summary');
      setSummary(res.data);
    } catch {
      toast.error('Failed to load time data');
    } finally {
      setLoading(false);
    }
  };

  const pieData = summary?.page_breakdown?.map(p => ({
    name: PAGE_LABELS[p.page] || p.page,
    value: p.minutes
  })) || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">

        <div className="flex items-center gap-3 mb-8">
          <MdTimer className="text-blue-600 text-4xl" />
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Time Analytics</h1>
            <p className="text-gray-500">Track how you spend your learning time</p>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-20 text-gray-400">
            Loading your time data...
          </div>
        ) : (
          <>
            {/* Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              {[
                {
                  label: 'Total Time',
                  value: summary?.formatted || '0s',
                  icon: <FiClock className="text-blue-500 text-2xl" />,
                  bg: 'bg-blue-50'
                },
                {
                  label: 'Total Sessions',
                  value: summary?.total_sessions || 0,
                  icon: <FiActivity className="text-green-500 text-2xl" />,
                  bg: 'bg-green-50'
                },
                {
                  label: 'Avg Session',
                  value: `${summary?.avg_session_minutes || 0}m`,
                  icon: <FiTrendingUp className="text-purple-500 text-2xl" />,
                  bg: 'bg-purple-50'
                },
                {
                  label: 'Hours Learned',
                  value: `${summary?.total_hours || 0}h`,
                  icon: <MdTimer className="text-orange-500 text-2xl" />,
                  bg: 'bg-orange-50'
                },
              ].map((stat, i) => (
                <div key={i} className={`${stat.bg} rounded-2xl p-5`}>
                  {stat.icon}
                  <p className="text-3xl font-bold text-gray-800 mt-2">
                    {stat.value}
                  </p>
                  <p className="text-gray-500 text-sm mt-1">{stat.label}</p>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

              {/* Daily Activity */}
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-4">
                  📅 Daily Activity (Last 7 Days)
                </h3>
                {summary?.daily_activity?.some(d => d.minutes > 0) ? (
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={summary.daily_activity}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" />
                      <YAxis unit="m" />
                      <Tooltip
                        formatter={(val) => [`${val} mins`, 'Time Spent']}
                      />
                      <Bar
                        dataKey="minutes"
                        fill="#3b82f6"
                        radius={[6, 6, 0, 0]}
                        name="Minutes"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="flex flex-col items-center justify-center h-48 text-gray-300">
                    <FiClock className="text-5xl mb-2" />
                    <p>No activity yet — start exploring!</p>
                  </div>
                )}
              </div>

              {/* Pie Chart */}
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-4">
                  🍩 Time by Section
                </h3>
                {pieData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={220}>
                    <PieChart>
                      <Pie
                        data={pieData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={90}
                        paddingAngle={3}
                        dataKey="value"
                      >
                        {pieData.map((_, i) => (
                          <Cell
                            key={i}
                            fill={COLORS[i % COLORS.length]}
                          />
                        ))}
                      </Pie>
                      <Tooltip
                        formatter={(val) => [`${val} mins`, 'Time']}
                      />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="flex flex-col items-center justify-center h-48 text-gray-300">
                    <FiActivity className="text-5xl mb-2" />
                    <p>No data yet — browse some pages!</p>
                  </div>
                )}
              </div>
            </div>

            {/* Breakdown Table */}
            {summary?.page_breakdown?.length > 0 && (
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-4">
                  📋 Detailed Breakdown
                </h3>
                <div className="space-y-3">
                  {summary.page_breakdown.map((item, i) => {
                    const maxMinutes = summary.page_breakdown[0]?.minutes || 1;
                    const pct = (item.minutes / maxMinutes) * 100;
                    return (
                      <div key={i} className="flex items-center gap-4">
                        <div className="w-36 text-sm text-gray-600 font-medium">
                          {PAGE_LABELS[item.page] || item.page}
                        </div>
                        <div className="flex-1 bg-gray-100 rounded-full h-3">
                          <div
                            className="h-3 rounded-full transition-all"
                            style={{
                              width: `${pct}%`,
                              backgroundColor: COLORS[i % COLORS.length]
                            }}
                          />
                        </div>
                        <div className="text-sm font-bold text-gray-700 w-16 text-right">
                          {item.minutes}m
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Empty State */}
            {summary?.total_sessions === 0 && (
              <div className="bg-white rounded-2xl shadow-sm p-12 text-center">
                <MdTimer className="text-6xl text-gray-200 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-400 mb-2">
                  No time tracked yet!
                </h3>
                <p className="text-gray-400">
                  Browse courses, take quizzes, and explore the app.
                  Your time will be tracked automatically! ⏱️
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default TimeAnalytics;