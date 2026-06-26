import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer
} from 'recharts';
import { FiTrendingUp, FiAward, FiAlertTriangle, FiCheckCircle } from 'react-icons/fi';
import { MdPsychology } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const predictionConfig = {
  at_risk: {
    color: '#ef4444',
    bg: 'rgba(239,68,68,0.1)',
    border: '1px solid rgba(239,68,68,0.3)',
    icon: <FiAlertTriangle style={{ color: '#ef4444', fontSize: '32px' }} />,
    label: '⚠️ At Risk'
  },
  on_track: {
    color: '#f59e0b',
    bg: 'rgba(245,158,11,0.1)',
    border: '1px solid rgba(245,158,11,0.3)',
    icon: <FiCheckCircle style={{ color: '#f59e0b', fontSize: '32px' }} />,
    label: '✅ On Track'
  },
  excelling: {
    color: '#10b981',
    bg: 'rgba(16,185,129,0.1)',
    border: '1px solid rgba(16,185,129,0.3)',
    icon: <FiAward style={{ color: '#10b981', fontSize: '32px' }} />,
    label: '🌟 Excelling'
  }
};

const Performance = () => {
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) navigate('/login');
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [summaryRes, historyRes] = await Promise.all([
        api.get('/performance/summary'),
        api.get('/performance/history')
      ]);
      setSummary(summaryRes.data);
      setHistory(historyRes.data.slice(0, 7));

      try {
        const enrollRes = await api.get('/courses/my/enrollments');
        if (enrollRes.data.length > 0) {
          const courseId = enrollRes.data[0].course_id;
          const predRes = await api.get(`/performance/predict/${courseId}`);
          setPrediction(predRes.data);
        }
      } catch {
        console.log('No enrollments for prediction');
      }

    } catch {
      toast.error('Failed to load performance data');
    } finally {
      setLoading(false);
    }
  };

  const chartData = history.map((h, i) => ({
    name: `Quiz ${i + 1}`,
    score: h.percentage,
    passed: h.passed ? 100 : 0
  }));

  const config = prediction ? predictionConfig[prediction.prediction] : null;

  const stats = [
    { label: 'Courses Enrolled',   value: summary?.total_courses_enrolled, color: '#6366f1' },
    { label: 'Quizzes Attempted',  value: summary?.total_quiz_attempts,    color: '#8b5cf6' },
    { label: 'Quizzes Passed',     value: summary?.quizzes_passed,         color: '#10b981' },
    { label: 'Avg Score',          value: `${summary?.average_score ?? 0}%`, color: '#f59e0b' },
  ];

  return (
    <div className="bg-mesh" style={{ minHeight: '100vh' }}>
      <Navbar />
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '32px 24px' }}>

        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '40px' }}>
          <div style={{
            width: '52px', height: '52px', borderRadius: '14px',
            background: 'rgba(99,102,241,0.2)', border: '1px solid rgba(99,102,241,0.3)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: '#6366f1', fontSize: '28px'
          }}>
            <MdPsychology />
          </div>
          <div>
            <h1 style={{ fontSize: '32px', fontWeight: '900', color: '#f1f5f9' }}>
              Performance{' '}
              <span style={{
                background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
              }}>Analytics</span>
            </h1>
            <p style={{ color: '#64748b', marginTop: '4px' }}>
              AI-powered insights into your learning journey
            </p>
          </div>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '80px 0', color: '#475569' }}>
            Analyzing your performance...
          </div>
        ) : (
          <>
            {/* Stats Cards */}
            <div style={{
              display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '16px', marginBottom: '32px'
            }}>
              {stats.map((stat, i) => (
                <div key={i} className="glass" style={{ borderRadius: '16px', padding: '24px', textAlign: 'center' }}>
                  <p style={{ fontSize: '32px', fontWeight: '800', color: stat.color, marginBottom: '4px' }}>
                    {stat.value ?? 0}
                  </p>
                  <p style={{ color: '#64748b', fontSize: '13px' }}>{stat.label}</p>
                </div>
              ))}
            </div>

            {/* AI Prediction Card */}
            {prediction && config && (
              <div style={{
                background: config.bg, border: config.border,
                borderRadius: '20px', padding: '28px', marginBottom: '32px'
              }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                  {config.icon}
                  <div style={{ flex: 1 }}>
                    <h2 style={{ fontSize: '24px', fontWeight: '800', color: config.color, marginBottom: '8px' }}>
                      {config.label}
                    </h2>
                    <p style={{ color: '#94a3b8', marginBottom: '8px' }}>
                      Confidence:{' '}
                      <span style={{ fontWeight: '700', color: '#f1f5f9' }}>
                        {prediction.confidence}%
                      </span>
                    </p>
                    <div style={{ display: 'flex', gap: '20px', fontSize: '13px', marginBottom: '16px' }}>
                      <span style={{ color: '#ef4444' }}>At Risk: {prediction.probabilities.at_risk}%</span>
                      <span style={{ color: '#f59e0b' }}>On Track: {prediction.probabilities.on_track}%</span>
                      <span style={{ color: '#10b981' }}>Excelling: {prediction.probabilities.excelling}%</span>
                    </div>
                    <div>
                      <p style={{ fontWeight: '700', color: '#cbd5e1', marginBottom: '8px' }}>
                        AI Recommendations:
                      </p>
                      <ul style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        {prediction.recommendations.map((rec, i) => (
                          <li key={i} style={{ color: '#94a3b8', fontSize: '14px' }}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Quiz Score History Chart */}
            {chartData.length > 0 && (
              <div className="glass" style={{ borderRadius: '20px', padding: '28px', marginBottom: '32px' }}>
                <h3 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '16px', marginBottom: '20px' }}>
                  📊 Quiz Score History
                </h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="name" stroke="#475569" tick={{ fill: '#64748b', fontSize: 12 }} />
                    <YAxis domain={[0, 100]} stroke="#475569" tick={{ fill: '#64748b', fontSize: 12 }} />
                    <Tooltip
                      contentStyle={{
                        background: '#0f0f1a', border: '1px solid rgba(245,158,11,0.3)',
                        borderRadius: '10px', color: '#f1f5f9'
                      }}
                    />
                    <Bar dataKey="score" fill="#f59e0b" radius={[6, 6, 0, 0]} name="Score %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Recent Attempts Table */}
            {history.length > 0 && (
              <div className="glass" style={{ borderRadius: '20px', padding: '28px' }}>
                <h3 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '16px', marginBottom: '20px' }}>
                  📋 Recent Quiz Attempts
                </h3>
                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
                    <thead>
                      <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                        {['Quiz', 'Score', 'Percentage', 'Status', 'Date'].map(col => (
                          <th key={col} style={{
                            padding: '0 0 12px 0', textAlign: 'left',
                            color: '#475569', fontWeight: '600', fontSize: '12px',
                            textTransform: 'uppercase', letterSpacing: '1px'
                          }}>
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {history.map((h, i) => (
                        <tr key={i} style={{ borderBottom: i < history.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
                          <td style={{ padding: '14px 0', color: '#cbd5e1' }}>Quiz #{h.quiz_id}</td>
                          <td style={{ padding: '14px 0', color: '#cbd5e1' }}>{h.score}/{h.total_marks}</td>
                          <td style={{ padding: '14px 0', color: '#cbd5e1' }}>{h.percentage}%</td>
                          <td style={{ padding: '14px 0' }}>
                            <span style={{
                              padding: '4px 10px', borderRadius: '20px',
                              fontSize: '12px', fontWeight: '600',
                              background: h.passed ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)',
                              color: h.passed ? '#10b981' : '#ef4444',
                              border: h.passed ? '1px solid rgba(16,185,129,0.3)' : '1px solid rgba(239,68,68,0.3)'
                            }}>
                              {h.passed ? 'Passed' : 'Failed'}
                            </span>
                          </td>
                          <td style={{ padding: '14px 0', color: '#475569' }}>
                            {new Date(h.attempted_at).toLocaleDateString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Performance;