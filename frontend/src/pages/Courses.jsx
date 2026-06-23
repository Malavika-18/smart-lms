import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiBook, FiLock } from 'react-icons/fi';
import { MdVerified } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';
import useTimeTracker from '../hooks/useTimeTracker';

const difficultyColor = {
  beginner: 'bg-green-100 text-green-700',
  intermediate: 'bg-yellow-100 text-yellow-700',
  advanced: 'bg-red-100 text-red-700',
};

const Courses = () => {
  const [courses, setCourses] = useState([]);
  const [enrolledIds, setEnrolledIds] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [buyingId, setBuyingId] = useState(null);
  const navigate = useNavigate();
  useTimeTracker('courses');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) navigate('/login');
    fetchCourses();
    fetchEnrollments();
  }, []);

  const fetchCourses = async () => {
    try {
      const res = await api.get('/courses/');
      setCourses(res.data);
    } catch {
      toast.error('Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  const fetchEnrollments = async () => {
    try {
      const res = await api.get('/courses/my/enrollments');
      setEnrolledIds(new Set(res.data.map(e => e.course_id)));
    } catch {
      console.error('Failed to load enrollments');
    }
  };

  const handleEnroll = async (courseId) => {
    try {
      await api.post(`/courses/${courseId}/enroll`);
      toast.success('Enrolled successfully!');
      setEnrolledIds(prev => new Set([...prev, courseId]));
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (detail === 'PREMIUM_REQUIRED') {
        toast.error('This is a premium course. Please purchase it!');
      } else {
        toast.error(detail || 'Enrollment failed');
      }
    }
  };

  const handleBuy = async (course) => {
    setBuyingId(course.id);
    try {
      const res = await api.post(`/courses/${course.id}/buy`);
      toast.success(`🎉 ${res.data.message}`);
      setEnrolledIds(prev => new Set([...prev, course.id]));
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Purchase failed');
    } finally {
      setBuyingId(null);
    }
  };

  const freeCourses = courses.filter(c => !c.is_premium);
  const premiumCourses = courses.filter(c => c.is_premium);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">

        <h1 className="text-3xl font-bold text-gray-800 mb-2">Browse Courses</h1>
        <p className="text-gray-500 mb-8">Explore our AI-curated learning paths</p>

        {loading ? (
          <div className="text-center py-20 text-gray-400">Loading courses...</div>
        ) : (
          <>
            {/* Free Courses */}
            <div className="mb-10">
              <div className="flex items-center gap-2 mb-4">
                <FiBook className="text-blue-600 text-xl" />
                <h2 className="text-xl font-bold text-gray-700">Free Courses</h2>
                <span className="bg-green-100 text-green-700 text-xs px-2 py-1 rounded-full font-medium">
                  {freeCourses.length} Available
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {freeCourses.map(course => (
                  <CourseCard
                    key={course.id}
                    course={course}
                    isEnrolled={enrolledIds.has(course.id)}
                    onEnroll={() => handleEnroll(course.id)}
                    onBuy={() => handleBuy(course)}
                    onView={() => navigate(`/course/${course.id}/learn`)}
                    buying={buyingId === course.id}
                  />
                ))}
              </div>
            </div>

            {/* Premium Courses */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <FiLock className="text-yellow-500 text-xl" />
                <h2 className="text-xl font-bold text-gray-700">Premium Courses</h2>
                <span className="bg-yellow-100 text-yellow-700 text-xs px-2 py-1 rounded-full font-medium">
                  {premiumCourses.length} Available
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {premiumCourses.map(course => (
                  <CourseCard
                    key={course.id}
                    course={course}
                    isEnrolled={enrolledIds.has(course.id)}
                    onEnroll={() => handleEnroll(course.id)}
                    onBuy={() => handleBuy(course)}
                    onView={() => navigate(`/course/${course.id}/learn`)}
                    buying={buyingId === course.id}
                  />
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

// Course Card Component
const CourseCard = ({ course, isEnrolled, onEnroll, onBuy, onView, buying }) => {
  const diffColor = difficultyColor[course.difficulty_level] || 'bg-gray-100 text-gray-600';

  return (
    <div className={`bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition ${
      course.is_premium ? 'border-2 border-yellow-300' : ''
    }`}>
      {/* Thumbnail */}
      <div className={`h-36 flex items-center justify-center relative ${
        course.is_premium
          ? 'bg-gradient-to-r from-yellow-400 to-orange-500'
          : 'bg-gradient-to-r from-blue-500 to-indigo-600'
      }`}>
        <FiBook className="text-white text-5xl" />
        {course.is_premium && (
          <div className="absolute top-3 right-3 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1">
            <MdVerified /> PREMIUM
          </div>
        )}
        {isEnrolled && (
          <div className="absolute top-3 left-3 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full">
            ✅ Enrolled
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-5">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-bold text-gray-800 text-lg leading-tight">
            {course.title}
          </h3>
          <span className={`text-xs px-2 py-1 rounded-full font-medium ml-2 flex-shrink-0 ${diffColor}`}>
            {course.difficulty_level}
          </span>
        </div>

        <p className="text-gray-500 text-sm mb-4 line-clamp-2">
          {course.description || 'No description available'}
        </p>

        <div className="flex items-center justify-between mb-4">
          <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
            {course.category || 'General'}
          </span>
          {course.is_premium && (
            <span className="text-lg font-bold text-orange-600">
              ₹{parseFloat(course.price).toFixed(0)}
            </span>
          )}
          {!course.is_premium && (
            <span className="text-sm font-bold text-green-600">FREE</span>
          )}
        </div>

        {/* Action Buttons */}
        {isEnrolled ? (
          <button
            onClick={onView}
            className="w-full bg-green-600 text-white py-2 rounded-lg text-sm font-semibold hover:bg-green-700 transition"
          >
            Continue Learning →
          </button>
        ) : course.is_premium ? (
          <div className="flex gap-2">
            <button
              onClick={onBuy}
              disabled={buying}
              className="flex-1 bg-gradient-to-r from-yellow-500 to-orange-500 text-white py-2 rounded-lg text-sm font-semibold hover:from-yellow-600 hover:to-orange-600 transition disabled:opacity-50"
            >
              {buying ? 'Processing...' : `Buy ₹${parseFloat(course.price).toFixed(0)}`}
            </button>
            <button
              onClick={onView}
              className="px-3 py-2 border-2 border-gray-200 rounded-lg text-gray-600 text-sm hover:border-gray-300 transition"
            >
              Preview
            </button>
          </div>
        ) : (
          <div className="flex gap-2">
            <button
              onClick={onEnroll}
              className="flex-1 bg-blue-600 text-white py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition"
            >
              Enroll Free
            </button>
            <button
              onClick={onView}
              className="px-3 py-2 border-2 border-gray-200 rounded-lg text-gray-600 text-sm hover:border-gray-300 transition"
            >
              Preview
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Courses;