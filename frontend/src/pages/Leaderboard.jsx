import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MdLeaderboard } from 'react-icons/md';
import { FiAward } from 'react-icons/fi';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const Leaderboard = () => {
  const navigate = useNavigate();
  const [leaderboard, setLeaderboard] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/login'); return; }
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    setCurrentUser(user);
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const res = await api.get('/analytics/leaderboard');
      setLeaderboard(res.data);
    } catch {
      toast.error('Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const medalEmoji = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-8">
          <MdLeaderboard className="text-blue-600 text-4xl" />
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Leaderboard</h1>
            <p className="text-gray-500">Top performers in Smart LMS</p>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-20 text-gray-400">Loading leaderboard...</div>
        ) : (
          <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
            {/* Top 3 Podium */}
            {leaderboard.length >= 3 && (
              <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-6 mb-0">
                <div className="flex items-end justify-center gap-4">
                  {/* 2nd Place */}
                  <div className="text-center">
                    <div className="bg-white bg-opacity-20 rounded-xl p-3 mb-2">
                      <p className="text-2xl">🥈</p>
                      <p className="text-white font-bold text-sm">
                        {leaderboard[1]?.full_name.split(' ')[0]}
                      </p>
                      <p className="text-blue-200 text-xs">
                        {leaderboard[1]?.total_points} pts
                      </p>
                    </div>
                    <div className="bg-gray-300 h-16 w-16 mx-auto rounded-t-lg" />
                  </div>

                  {/* 1st Place */}
                  <div className="text-center">
                    <div className="bg-white bg-opacity-20 rounded-xl p-3 mb-2">
                      <p className="text-3xl">🥇</p>
                      <p className="text-white font-bold">
                        {leaderboard[0]?.full_name.split(' ')[0]}
                      </p>
                      <p className="text-blue-200 text-sm">
                        {leaderboard[0]?.total_points} pts
                      </p>
                    </div>
                    <div className="bg-yellow-400 h-24 w-16 mx-auto rounded-t-lg" />
                  </div>

                  {/* 3rd Place */}
                  <div className="text-center">
                    <div className="bg-white bg-opacity-20 rounded-xl p-3 mb-2">
                      <p className="text-2xl">🥉</p>
                      <p className="text-white font-bold text-sm">
                        {leaderboard[2]?.full_name.split(' ')[0]}
                      </p>
                      <p className="text-blue-200 text-xs">
                        {leaderboard[2]?.total_points} pts
                      </p>
                    </div>
                    <div className="bg-orange-400 h-10 w-16 mx-auto rounded-t-lg" />
                  </div>
                </div>
              </div>
            )}

            {/* Full List */}
            <div className="divide-y">
              {leaderboard.map((entry, i) => (
                <div
                  key={i}
                  className={`flex items-center gap-4 px-6 py-4 ${
                    entry.student_id === currentUser?.id
                      ? 'bg-blue-50'
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <span className="text-xl w-10 text-center font-bold text-gray-500">
                    {medalEmoji(entry.rank)}
                  </span>
                  <div className="flex-1">
                    <p className="font-semibold text-gray-800">
                      {entry.full_name}
                      {entry.student_id === currentUser?.id && (
                        <span className="ml-2 text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full">
                          You
                        </span>
                      )}
                    </p>
                    <p className="text-xs text-gray-400">
                      {entry.courses_enrolled} courses enrolled ·{' '}
                      {entry.quiz_attempts} quizzes attempted
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-gray-800 text-lg">
                      {entry.total_points}
                    </p>
                    <p className="text-xs text-gray-400">points</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-blue-600">
                      {entry.avg_score}%
                    </p>
                    <p className="text-xs text-gray-400">avg score</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Leaderboard;