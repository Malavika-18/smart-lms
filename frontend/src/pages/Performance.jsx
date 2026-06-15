import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  RadialBarChart, RadialBar, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from 'recharts';
import { FiTrendingUp, FiAward, FiAlertTriangle, FiCheckCircle } from 'react-icons/fi';
import { MdPsychology } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const predictionConfig = {
  at_risk: {
    color: 'text-red-600',
    bg: 'bg-red-50',
    border: 'border-red-200',
    icon: <FiAlertTriangle className="text-red-500 text-3xl" />,
    label: '⚠️ At Risk'
  },
  on_track: {
    color: 'text-yellow-600',
    bg: 'bg-yellow-50',
    border: 'border-yellow-200',
    icon: <FiCheckCircle className="text-yellow-500 text-3xl" />,
    label: '✅ On Track'
  },
  excelling: {
    color: 'text-green-600',
    bg: 'bg-green-50',
    border: 'border-green-200',
    icon: <FiAward className="text-green-500 text-3xl" />,
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

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">

        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <MdPsychology className="text-blue-600 text-4xl" />
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Performance Analytics</h1>
            <p className="text-gray-500">AI-powered insights into your learning journey</p>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-20 text-gray-400">Analyzing your performance...</div>
        ) : (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              {[
                { label: 'Courses Enrolled', value: summary?.total_courses_enrolled, color: 'blue' },
                { label: 'Quizzes Attempted', value: summary?.total_quiz_attempts, color: 'purple' },
                { label: 'Quizzes Passed', value: summary?.quizzes_passed, color: 'green' },
                { label: 'Avg Score', value: `${summary?.average_score ?? 0}%`, color: 'yellow' },
              ].map((stat, i) => (
                <div key={i} className="bg-white rounded-xl shadow-sm p-5 text-center">
                  <p className={`text-3xl font-bold text-${stat.color}-600`}>{stat.value}</p>
                  <p className="text-gray-500 text-sm mt-1">{stat.label}</p>
                </div>
              ))}
            </div>

            {/* AI Prediction Card */}
            {prediction && config && (
              <div className={`${config.bg} border-2 ${config.border} rounded-2xl p-6 mb-8`}>
                <div className="flex items-start gap-4">
                  {config.icon}
                  <div className="flex-1">
                    <h2 className={`text-2xl font-bold ${config.color} mb-1`}>
                      {config.label}
                    </h2>
                    <p className="text-gray-600 mb-1">
                      Confidence: <span className="font-bold">{prediction.confidence}%</span>
                    </p>
                    <div className="flex gap-4 text-sm mb-4">
                      <span className="text-red-500">At Risk: {prediction.probabilities.at_risk}%</span>
                      <span className="text-yellow-500">On Track: {prediction.probabilities.on_track}%</span>
                      <span className="text-green-500">Excelling: {prediction.probabilities.excelling}%</span>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-700 mb-2">AI Recommendations:</p>
                      <ul className="space-y-1">
                        {prediction.recommendations.map((rec, i) => (
                          <li key={i} className="text-gray-600 text-sm">{rec}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Quiz Score History Chart */}
            {chartData.length > 0 && (
              <div className="bg-white rounded-2xl shadow-sm p-6 mb-8">
                <h3 className="text-lg font-bold text-gray-800 mb-4">Quiz Score History</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="score" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Score %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Recent Attempts Table */}
            {history.length > 0 && (
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-4">Recent Quiz Attempts</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-gray-500 border-b">
                        <th className="pb-3">Quiz</th>
                        <th className="pb-3">Score</th>
                        <th className="pb-3">Percentage</th>
                        <th className="pb-3">Status</th>
                        <th className="pb-3">Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.map((h, i) => (
                        <tr key={i} className="border-b last:border-0">
                          <td className="py-3">Quiz #{h.quiz_id}</td>
                          <td className="py-3">{h.score}/{h.total_marks}</td>
                          <td className="py-3">{h.percentage}%</td>
                          <td className="py-3">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              h.passed
                                ? 'bg-green-100 text-green-700'
                                : 'bg-red-100 text-red-700'
                            }`}>
                              {h.passed ? 'Passed' : 'Failed'}
                            </span>
                          </td>
                          <td className="py-3 text-gray-400">
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