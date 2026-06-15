import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  CartesianGrid, ResponsiveContainer, LineChart, Line
} from 'recharts';
import {
  FiBook, FiAward, FiTrendingUp,
  FiCheckCircle, FiClock, FiStar
} from 'react-icons/fi';
import {
  MdSchool, MdAutoAwesome,
  MdPsychology, MdLeaderboard
} from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const difficultyColor = {
  beginner: 'bg-green-100 text-green-700',
  intermediate: 'bg-yellow-100 text-yellow-700',
  advanced: 'bg-red-100 text-red-700',
};

const Dashboard = () => {
  const navigate = useNavigate();
  const [overview, setOverview] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/login'); return; }
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [overviewRes, leaderboardRes] = await Promise.all([
        api.get('/analytics/overview'),
        api.get('/analytics/leaderboard')
      ]);
      setOverview(overviewRes.data);
      setLeaderboard(leaderboardRes.data);
    } catch {
      toast.error('Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  const chartData = overview?.recent_attempts?.map((a, i) => ({
    name: `Quiz ${i + 1}`,
    score: a.percentage
  })) || [];

  if (loading) return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex justify-center items-center h-64 text-gray-400 text-lg">
        Loading your dashboard...
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">

        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-6 mb-8 text-white">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold mb-1">
                Welcome back, {overview?.student?.full_name}! 👋
              </h1>
              <p className="text-blue-100">
                Ready to continue your learning journey?
              </p>
            </div>
            <div className="text-right">
              <p className="text-blue-200 text-sm">Leaderboard Rank</p>
              <p className="text-5xl font-bold">
                #{overview?.stats?.leaderboard_rank}
              </p>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          {[
            {
              label: 'Total Points',
              value: overview?.stats?.total_points,
              icon: <FiStar className="text-yellow-500" />,
              color: 'yellow'
            },
            {
              label: 'Avg Score',
              value: `${overview?.stats?.avg_score ?? 0}%`,
              icon: <FiTrendingUp className="text-blue-500" />,
              color: 'blue'
            },
            {
              label: 'Quizzes Passed',
              value: overview?.stats?.quizzes_passed,
              icon: <FiCheckCircle className="text-green-500" />,
              color: 'green'
            },
            {
              label: 'Total Attempts',
              value: overview?.stats?.total_attempts,
              icon: <FiClock className="text-purple-500" />,
              color: 'purple'
            },
            {
              label: 'Courses',
              value: overview?.stats?.courses_enrolled,
              icon: <FiBook className="text-indigo-500" />,
              color: 'indigo'
            },
            {
              label: 'Rank',
              value: `#${overview?.stats?.leaderboard_rank}`,
              icon: <FiAward className="text-red-500" />,
              color: 'red'
            },
          ].map((stat, i) => (
            <div key={i} className="bg-white rounded-xl shadow-sm p-4 text-center">
              <div className="flex justify-center text-2xl mb-2">{stat.icon}</div>
              <p className="text-2xl font-bold text-gray-800">{stat.value ?? 0}</p>
              <p className="text-gray-400 text-xs mt-1">{stat.label}</p>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

          {/* Quick Actions */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <h2 className="text-lg font-bold text-gray-800 mb-4">Quick Actions</h2>
            <div className="space-y-3">
              {[
                {
                  to: '/courses',
                  icon: <MdSchool className="text-blue-500 text-xl" />,
                  label: 'Browse Courses',
                  color: 'blue'
                },
                {
                  to: '/recommendations',
                  icon: <MdAutoAwesome className="text-yellow-500 text-xl" />,
                  label: 'AI Recommendations',
                  color: 'yellow'
                },
                {
                  to: '/performance',
                  icon: <MdPsychology className="text-purple-500 text-xl" />,
                  label: 'View Performance',
                  color: 'purple'
                },
                {
                  to: '/leaderboard',
                  icon: <MdLeaderboard className="text-green-500 text-xl" />,
                  label: 'Leaderboard',
                  color: 'green'
                },
              ].map((action, i) => (
                <Link
                  key={i}
                  to={action.to}
                  className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition border border-gray-100"
                >
                  {action.icon}
                  <span className="font-medium text-gray-700">{action.label}</span>
                </Link>
              ))}
            </div>
          </div>

          {/* Quiz Score Chart */}
          <div className="bg-white rounded-2xl shadow-sm p-6 lg:col-span-2">
            <h2 className="text-lg font-bold text-gray-800 mb-4">
              Recent Quiz Performance
            </h2>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#3b82f6"
                    strokeWidth={3}
                    dot={{ fill: '#3b82f6', r: 5 }}
                    name="Score %"
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex flex-col items-center justify-center h-48 text-gray-300">
                <FiTrendingUp className="text-5xl mb-2" />
                <p>No quiz data yet. Take a quiz!</p>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* Enrolled Courses */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-bold text-gray-800">My Courses</h2>
              <Link to="/courses" className="text-blue-600 text-sm font-medium hover:underline">
                Browse More →
              </Link>
            </div>
            {overview?.enrolled_courses?.length === 0 ? (
              <div className="text-center py-8 text-gray-300">
                <FiBook className="text-5xl mx-auto mb-2" />
                <p>No courses yet. Start learning!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {overview?.enrolled_courses?.map((course, i) => (
                  <div key={i} className="flex items-center gap-3 p-3 border rounded-xl">
                    <div className="bg-blue-100 rounded-lg p-2">
                      <FiBook className="text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-semibold text-gray-800 text-sm">
                        {course.title}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                          <div
                            className="bg-blue-500 h-1.5 rounded-full"
                            style={{ width: `${course.progress_percent}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-400">
                          {course.progress_percent}%
                        </span>
                      </div>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full ${difficultyColor[course.difficulty_level]}`}>
                      {course.difficulty_level}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Leaderboard */}
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-bold text-gray-800">🏆 Leaderboard</h2>
              <Link to="/leaderboard" className="text-blue-600 text-sm font-medium hover:underline">
                View All →
              </Link>
            </div>
            <div className="space-y-3">
              {leaderboard.slice(0, 5).map((entry, i) => (
                <div
                  key={i}
                  className={`flex items-center gap-3 p-3 rounded-xl ${
                    entry.student_id === overview?.student?.id
                      ? 'bg-blue-50 border-2 border-blue-200'
                      : 'border border-gray-100'
                  }`}
                >
                  <span className={`text-lg font-bold w-8 text-center ${
                    i === 0 ? 'text-yellow-500' :
                    i === 1 ? 'text-gray-400' :
                    i === 2 ? 'text-orange-400' : 'text-gray-500'
                  }`}>
                    {i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${entry.rank}`}
                  </span>
                  <div className="flex-1">
                    <p className="font-semibold text-gray-800 text-sm">
                      {entry.full_name}
                      {entry.student_id === overview?.student?.id && (
                        <span className="ml-2 text-xs text-blue-600">(You)</span>
                      )}
                    </p>
                    <p className="text-xs text-gray-400">
                      {entry.courses_enrolled} courses · {entry.quiz_attempts} quizzes
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-gray-800">{entry.total_points}</p>
                    <p className="text-xs text-gray-400">points</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;