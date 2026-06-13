import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiStar, FiBook, FiTrendingUp } from 'react-icons/fi';
import { MdAutoAwesome } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const difficultyColor = {
  beginner: 'bg-green-100 text-green-700',
  intermediate: 'bg-yellow-100 text-yellow-700',
  advanced: 'bg-red-100 text-red-700',
};

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [popular, setPopular] = useState([]);
  const [loading, setLoading] = useState(true);
  const [studentName, setStudentName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) navigate('/login');
    fetchRecommendations();
    fetchPopular();
  }, []);

  const fetchRecommendations = async () => {
    try {
      const res = await api.get('/recommendations/');
      setRecommendations(res.data.recommendations);
      setStudentName(res.data.student_name);
    } catch {
      toast.error('Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const fetchPopular = async () => {
    try {
      const res = await api.get('/recommendations/popular');
      setPopular(res.data);
    } catch {
      console.error('Failed to load popular courses');
    }
  };

  const handleEnroll = async (courseId) => {
    try {
      await api.post(`/courses/${courseId}/enroll`);
      toast.success('Enrolled successfully!');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Enrollment failed');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">

        {/* Header */}
        <div className="flex items-center gap-3 mb-2">
          <MdAutoAwesome className="text-blue-600 text-3xl" />
          <h1 className="text-3xl font-bold text-gray-800">AI Recommendations</h1>
        </div>
        <p className="text-gray-500 mb-8">
          Personalized course suggestions for <span className="font-semibold text-blue-600">{studentName}</span>
        </p>

        {/* AI Recommendations */}
        <div className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <FiStar className="text-yellow-500 text-xl" />
            <h2 className="text-xl font-bold text-gray-700">Recommended For You</h2>
            <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full font-medium ml-2">
              AI Powered
            </span>
          </div>

          {loading ? (
            <div className="text-center py-12 text-gray-400">Analyzing your learning pattern...</div>
          ) : recommendations.length === 0 ? (
            <div className="bg-white rounded-xl p-8 text-center shadow-sm">
              <FiBook className="text-4xl text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">Enroll in more courses to get personalized recommendations!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.map((course) => (
                <div key={course.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition border-l-4 border-blue-500">
                  <div className="p-5">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-gray-800">{course.title}</h3>
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${difficultyColor[course.difficulty_level] || 'bg-gray-100 text-gray-600'}`}>
                        {course.difficulty_level}
                      </span>
                    </div>
                    <p className="text-gray-500 text-sm mb-3 line-clamp-2">
                      {course.description || 'No description'}
                    </p>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
                        {course.category || 'General'}
                      </span>
                      <div className="flex items-center gap-1">
                        <FiStar className="text-yellow-400 text-xs" />
                        <span className="text-xs text-gray-500 font-medium">
                          {(course.recommendation_score * 100).toFixed(0)}% match
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleEnroll(course.id)}
                      className="w-full bg-blue-600 text-white py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition"
                    >
                      Enroll Now
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Popular Courses */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <FiTrendingUp className="text-green-500 text-xl" />
            <h2 className="text-xl font-bold text-gray-700">Trending Courses</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {popular.map((course) => (
              <div key={course.id} className="bg-white rounded-xl shadow-sm p-4 flex items-center gap-4 hover:shadow-md transition">
                <div className="bg-green-100 rounded-lg p-3">
                  <FiTrendingUp className="text-green-600 text-xl" />
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-800 text-sm">{course.title}</h4>
                  <p className="text-xs text-gray-400">
                    {course.enrollment_count} students enrolled
                  </p>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${difficultyColor[course.difficulty_level] || 'bg-gray-100 text-gray-600'}`}>
                  {course.difficulty_level}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Recommendations;