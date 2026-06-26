import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  CartesianGrid, ResponsiveContainer
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
import useTimeTracker from '../hooks/useTimeTracker';

const difficultyStyle = {
  beginner:     { background: 'rgba(16,185,129,0.15)', color: '#10b981', border: '1px solid rgba(16,185,129,0.3)' },
  intermediate: { background: 'rgba(245,158,11,0.15)', color: '#f59e0b', border: '1px solid rgba(245,158,11,0.3)' },
  advanced:     { background: 'rgba(239,68,68,0.15)',  color: '#ef4444', border: '1px solid rgba(239,68,68,0.3)'  },
};

const Dashboard = () => {
  const navigate = useNavigate();
  const [overview, setOverview] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  useTimeTracker('dashboard');

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

  const stats = [
    { label: 'Total Points',   value: overview?.stats?.total_points ?? 0,                                          icon: <FiStar />,        color: '#f59e0b' },
    { label: 'Avg Score',      value: `${overview?.stats?.avg_score ?? 0}%`,                                       icon: <FiTrendingUp />,  color: '#6366f1' },
    { label: 'Quizzes Passed', value: overview?.stats?.quizzes_passed ?? 0,                                        icon: <FiCheckCircle />, color: '#10b981' },
    { label: 'Total Attempts', value: overview?.stats?.total_attempts ?? 0,                                        icon: <FiClock />,       color: '#8b5cf6' },
    { label: 'Courses',        value: overview?.stats?.courses_enrolled ?? 0,                                      icon: <FiBook />,        color: '#06b6d4' },
    { label: 'Rank',           value: overview?.stats?.leaderboard_rank ? `#${overview.stats.leaderboard_rank}` : '#1', icon: <FiAward />, color: '#f59e0b' },
  ];

  const quickActions = [
    { to: '/courses',         icon: <MdSchool />,      label: 'Browse Courses',    color: '#6366f1' },
    { to: '/recommendations', icon: <MdAutoAwesome />, label: 'AI Recommendations',color: '#f59e0b' },
    { to: '/performance',     icon: <MdPsychology />,  label: 'View Performance',  color: '#8b5cf6' },
    { to: '/leaderboard',     icon: <MdLeaderboard />, label: 'Leaderboard',       color: '#10b981' },
  ];

  if (loading) return (
    <div className="bg-mesh" style={{ minHeight: '100vh' }}>
      <Navbar />
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '50px', height: '50px', borderRadius: '50%',
            border: '3px solid rgba(245,158,11,0.3)',
            borderTop: '3px solid #f59e0b',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 16px'
          }} />
          <p style={{ color: '#64748b' }}>Loading your dashboard...</p>
        </div>
      </div>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );

  return (
    <div className="bg-mesh" style={{ minHeight: '100vh' }}>
      <Navbar />
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '32px 24px' }}>

        {/* Welcome Banner */}
        <div style={{
          background: 'linear-gradient(135deg, rgba(99,102,241,0.2), rgba(245,158,11,0.1))',
          border: '1px solid rgba(245,158,11,0.3)',
          borderRadius: '20px',
          padding: '32px',
          marginBottom: '32px',
          position: 'relative',
          overflow: 'hidden',
          boxShadow: '0 0 40px rgba(245,158,11,0.1)'
        }}>
          <div style={{
            position: 'absolute', right: '-50px', top: '-50px',
            width: '200px', height: '200px', borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(245,158,11,0.15), transparent)',
            pointerEvents: 'none'
          }} />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <p style={{ color: '#f59e0b', fontSize: '13px', fontWeight: '600', letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '8px' }}>
                Welcome Back
              </p>
              <h1 style={{ fontSize: '32px', fontWeight: '800', color: '#f1f5f9', marginBottom: '8px' }}>
                {overview?.student?.full_name || 'Student'} 👋
              </h1>
              <p style={{ color: '#94a3b8', fontSize: '15px' }}>
                Ready to continue your learning journey?
              </p>
            </div>
            <div style={{ textAlign: 'right' }}>
              <p style={{ color: '#64748b', fontSize: '12px', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '1px' }}>
                Leaderboard Rank
              </p>
              <p style={{
                fontSize: '56px', fontWeight: '900',
                background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                lineHeight: 1
              }}>
                {overview?.stats?.leaderboard_rank ? `#${overview.stats.leaderboard_rank}` : '#1'}
              </p>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(6, 1fr)',
          gap: '16px',
          marginBottom: '32px'
        }}>
          {stats.map((stat, i) => (
            <div key={i} className="stat-card card-hover" style={{ borderRadius: '16px', padding: '20px', textAlign: 'center' }}>
              <div style={{
                width: '40px', height: '40px', borderRadius: '10px',
                background: `${stat.color}20`,
                border: `1px solid ${stat.color}40`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                margin: '0 auto 12px',
                fontSize: '18px', color: stat.color
              }}>
                {stat.icon}
              </div>
              <p style={{ fontSize: '24px', fontWeight: '800', color: '#f1f5f9', marginBottom: '4px' }}>
                {stat.value}
              </p>
              <p style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '1px' }}>
                {stat.label}
              </p>
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px', marginBottom: '24px' }}>

          {/* Quick Actions */}
          <div className="glass" style={{ borderRadius: '20px', padding: '24px' }}>
            <h2 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '16px', marginBottom: '16px' }}>
              ⚡ Quick Actions
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {quickActions.map((action, i) => (
                <Link key={i} to={action.to} style={{
                  display: 'flex', alignItems: 'center', gap: '12px',
                  padding: '12px 16px', borderRadius: '12px',
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  textDecoration: 'none', transition: 'all 0.2s ease'
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.background = `${action.color}15`;
                  e.currentTarget.style.borderColor = `${action.color}40`;
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                  e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)';
                }}
                >
                  <div style={{
                    width: '34px', height: '34px', borderRadius: '8px',
                    background: `${action.color}20`,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '18px', color: action.color
                  }}>
                    {action.icon}
                  </div>
                  <span style={{ color: '#cbd5e1', fontSize: '14px', fontWeight: '500' }}>
                    {action.label}
                  </span>
                </Link>
              ))}
            </div>
          </div>

          {/* Chart */}
          <div className="glass" style={{ borderRadius: '20px', padding: '24px' }}>
            <h2 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '16px', marginBottom: '20px' }}>
              📈 Recent Quiz Performance
            </h2>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="name" stroke="#475569" tick={{ fill: '#64748b', fontSize: 12 }} />
                  <YAxis domain={[0, 100]} stroke="#475569" tick={{ fill: '#64748b', fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{
                      background: '#0f0f1a', border: '1px solid rgba(245,158,11,0.3)',
                      borderRadius: '10px', color: '#f1f5f9'
                    }}
                  />
                  <Line
                    type="monotone" dataKey="score" stroke="#f59e0b"
                    strokeWidth={3} dot={{ fill: '#f59e0b', r: 5, strokeWidth: 0 }}
                    activeDot={{ r: 7, fill: '#fbbf24' }} name="Score %"
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '200px' }}>
                <FiTrendingUp style={{ fontSize: '48px', color: '#1e293b', marginBottom: '12px' }} />
                <p style={{ color: '#475569' }}>No quiz data yet. Take a quiz!</p>
              </div>
            )}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>

          {/* Enrolled Courses */}
          <div className="glass" style={{ borderRadius: '20px', padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h2 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '16px' }}>📚 My Courses</h2>
              <Link to="/courses" style={{ color: '#f59e0b', fontSize: '13px', textDecoration: 'none', fontWeight: '600' }}>
                Browse More →
              </Link>
            </div>
            {!overview?.enrolled_courses?.length ? (
              <div style={{ textAlign: 'center', padding: '32px 0' }}>
                <FiBook style={{ fontSize: '40px', color: '#1e293b', marginBottom: '12px' }} />
                <p style={{ color: '#475569' }}>No courses yet. Start learning!</p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {overview.enrolled_courses.map((course, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'center', gap: '12px',
                    padding: '12px', borderRadius: '12px',
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(255,255,255,0.06)'
                  }}>
                    <div style={{
                      width: '36px', height: '36px', borderRadius: '8px',
                      background: 'rgba(99,102,241,0.2)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      color: '#6366f1', flexShrink: 0
                    }}>
                      <FiBook />
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ color: '#cbd5e1', fontSize: '13px', fontWeight: '600', marginBottom: '6px' }}>
                        {course.title}
                      </p>
                      <div style={{ background: 'rgba(255,255,255,0.1)', borderRadius: '4px', height: '4px' }}>
                        <div style={{
                          background: 'linear-gradient(90deg, #6366f1, #f59e0b)',
                          borderRadius: '4px', height: '4px',
                          width: `${course.progress_percent}%`
                        }} />
                      </div>
                    </div>
                    <span style={{ color: '#64748b', fontSize: '12px', flexShrink: 0 }}>
                      {course.progress_percent}%
                    </span>
                    {/* ── Difficulty badge (restored from original) ── */}
                    {course.difficulty_level && (
                      <span style={{
                        fontSize: '11px',
                        fontWeight: '600',
                        padding: '3px 8px',
                        borderRadius: '6px',
                        textTransform: 'capitalize',
                        flexShrink: 0,
                        ...(difficultyStyle[course.difficulty_level] ?? {
                          background: 'rgba(100,116,139,0.15)',
                          color: '#94a3b8',
                          border: '1px solid rgba(100,116,139,0.3)'
                        })
                      }}>
                        {course.difficulty_level}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Leaderboard */}
          <div className="glass" style={{ borderRadius: '20px', padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h2 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '16px' }}>🏆 Leaderboard</h2>
              <Link to="/leaderboard" style={{ color: '#f59e0b', fontSize: '13px', textDecoration: 'none', fontWeight: '600' }}>
                View All →
              </Link>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {leaderboard.slice(0, 5).map((entry, i) => (
                <div key={i} style={{
                  display: 'flex', alignItems: 'center', gap: '12px',
                  padding: '10px 12px', borderRadius: '12px',
                  background: entry.student_id === overview?.student?.id
                    ? 'rgba(245,158,11,0.1)' : 'rgba(255,255,255,0.03)',
                  border: entry.student_id === overview?.student?.id
                    ? '1px solid rgba(245,158,11,0.3)' : '1px solid rgba(255,255,255,0.06)'
                }}>
                  <span style={{ fontSize: '18px', width: '28px', textAlign: 'center' }}>
                    {i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${entry.rank}`}
                  </span>
                  <div style={{ flex: 1 }}>
                    <p style={{ color: '#cbd5e1', fontSize: '13px', fontWeight: '600' }}>
                      {entry.full_name}
                      {entry.student_id === overview?.student?.id && (
                        <span style={{
                          marginLeft: '8px', fontSize: '10px', color: '#f59e0b',
                          background: 'rgba(245,158,11,0.2)', padding: '2px 6px', borderRadius: '4px'
                        }}>YOU</span>
                      )}
                    </p>
                    <p style={{ color: '#475569', fontSize: '11px' }}>
                      {entry.quiz_attempts} quizzes
                    </p>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <p style={{ color: '#f59e0b', fontWeight: '700', fontSize: '14px' }}>
                      {entry.total_points}
                    </p>
                    <p style={{ color: '#475569', fontSize: '11px' }}>pts</p>
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