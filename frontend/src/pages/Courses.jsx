import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiBook } from 'react-icons/fi';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const difficultyColor = {
  beginner: 'bg-green-100 text-green-700',
  intermediate: 'bg-yellow-100 text-yellow-700',
  advanced: 'bg-red-100 text-red-700',
};

const Courses = () => {
  const [courses, setCourses] = useState([]);
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [courseQuizzes, setCourseQuizzes] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

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
      // Fetch quizzes for each course
      res.data.forEach(async (course) => {
        try {
          const quizRes = await api.get(`/quiz/course/${course.id}`);
          if (quizRes.data.length > 0) {
            setCourseQuizzes(prev => ({ ...prev, [course.id]: quizRes.data[0] }));
          }
        } catch {}
      });
    } catch {
      toast.error('Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  const fetchEnrollments = async () => {
    try {
      const res = await api.get('/courses/my/enrollments');
      setEnrolledCourses(res.data.map(e => e.course_id));
    } catch {}
  };

  const handleEnroll = async (courseId) => {
    try {
      await api.post(`/courses/${courseId}/enroll`);
      toast.success('Enrolled successfully!');
      setEnrolledCourses([...enrolledCourses, courseId]);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Enrollment failed');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Browse Courses</h1>
        <p className="text-gray-500 mb-8">Explore our AI-curated learning paths</p>

        {loading ? (
          <div className="text-center py-20 text-gray-400">Loading courses...</div>
        ) : courses.length === 0 ? (
          <div className="text-center py-20">
            <FiBook className="text-6xl text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No courses available yet.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map((course) => {
              const isEnrolled = enrolledCourses.includes(course.id);
              const quiz = courseQuizzes[course.id];
              return (
                <div key={course.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition">
                  <div className="bg-gradient-to-r from-blue-500 to-indigo-600 h-36 flex items-center justify-center">
                    <FiBook className="text-white text-5xl" />
                  </div>
                  <div className="p-5">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-gray-800 text-lg">{course.title}</h3>
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${difficultyColor[course.difficulty_level] || 'bg-gray-100 text-gray-600'}`}>
                        {course.difficulty_level}
                      </span>
                    </div>
                    <p className="text-gray-500 text-sm mb-4 line-clamp-2">
                      {course.description || 'No description available'}
                    </p>

                    {/* ✅ Updated bottom section */}
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
                        {course.category || 'General'}
                      </span>
                      <div className="flex gap-2">
                        <button
                          onClick={() => navigate(`/course/${course.id}/learn`)}
                          className="bg-gray-100 text-gray-700 px-3 py-2 rounded-lg text-sm font-semibold hover:bg-gray-200 transition"
                        >
                          View
                        </button>
                        {isEnrolled ? (
                          <span className="bg-green-100 text-green-700 px-4 py-2 rounded-lg text-sm font-semibold">
                            ✅ Enrolled
                          </span>
                        ) : (
                          <button
                            onClick={() => handleEnroll(course.id)}
                            className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition"
                          >
                            Enroll
                          </button>
                        )}
                      </div>
                    </div>

                    {isEnrolled && quiz && (
                      <button
                        onClick={() => navigate(`/quiz/${quiz.id}`)}
                        className="w-full mt-3 bg-purple-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-purple-700 transition"
                      >
                        🎯 Take Quiz
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default Courses;