import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  FiBook, FiClock, FiChevronRight,
  FiChevronLeft, FiExternalLink, FiPlay
} from 'react-icons/fi';
import {
  SiGeeksforgeeks, SiYoutube
} from 'react-icons/si';
import { MdArticle, MdCode } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const resourceConfig = {
  youtube: {
    icon: <SiYoutube className="text-red-500" />,
    bg: 'bg-red-50 border-red-200 hover:bg-red-100',
    label: 'YouTube'
  },
  article: {
    icon: <MdArticle className="text-green-600" />,
    bg: 'bg-green-50 border-green-200 hover:bg-green-100',
    label: 'Article'
  },
  docs: {
    icon: <MdCode className="text-blue-600" />,
    bg: 'bg-blue-50 border-blue-200 hover:bg-blue-100',
    label: 'Official Docs'
  }
};

const LESSON_RESOURCES = {
  "Introduction to Python": [
    { title: "Python Introduction - GeeksForGeeks", url: "https://www.geeksforgeeks.org/python-programming-language/", type: "article" },
    { title: "Python Official Documentation", url: "https://docs.python.org/3/tutorial/", type: "docs" },
    { title: "W3Schools Python Tutorial", url: "https://www.w3schools.com/python/", type: "article" }
  ],
  "Variables and Data Types": [
    { title: "Python Variables - GFG", url: "https://www.geeksforgeeks.org/python-variables/", type: "article" },
    { title: "Data Types in Python - GFG", url: "https://www.geeksforgeeks.org/python-data-types/", type: "article" },
    { title: "W3Schools Data Types", url: "https://www.w3schools.com/python/python_datatypes.asp", type: "article" }
  ],
  "Loops and Functions": [
    { title: "Python Loops - GFG", url: "https://www.geeksforgeeks.org/loops-in-python/", type: "article" },
    { title: "Python Functions - GFG", url: "https://www.geeksforgeeks.org/python-functions/", type: "article" },
    { title: "W3Schools Functions", url: "https://www.w3schools.com/python/python_functions.asp", type: "article" }
  ],
  "What is Machine Learning?": [
    { title: "Intro to ML - GFG", url: "https://www.geeksforgeeks.org/machine-learning/", type: "article" },
    { title: "Scikit-learn Getting Started", url: "https://scikit-learn.org/stable/getting_started.html", type: "docs" },
    { title: "ML Tutorial - W3Schools", url: "https://www.w3schools.com/python/python_ml_getting_started.asp", type: "article" }
  ],
  "Supervised Learning Algorithms": [
    { title: "Supervised Learning - GFG", url: "https://www.geeksforgeeks.org/supervised-unsupervised-learning/", type: "article" },
    { title: "Random Forest - GFG", url: "https://www.geeksforgeeks.org/random-forest-classifier-using-scikit-learn/", type: "article" },
    { title: "Decision Trees - GFG", url: "https://www.geeksforgeeks.org/decision-tree/", type: "article" }
  ],
  "Model Evaluation and Tuning": [
    { title: "Model Evaluation - GFG", url: "https://www.geeksforgeeks.org/metrics-for-machine-learning-model/", type: "article" },
    { title: "Cross Validation - GFG", url: "https://www.geeksforgeeks.org/cross-validation-machine-learning/", type: "article" },
    { title: "Scikit-learn Metrics", url: "https://scikit-learn.org/stable/modules/model_evaluation.html", type: "docs" }
  ],
  "React Fundamentals": [
    { title: "React Tutorial - GFG", url: "https://www.geeksforgeeks.org/reactjs/", type: "article" },
    { title: "React Official Docs", url: "https://react.dev/learn", type: "docs" },
    { title: "W3Schools React", url: "https://www.w3schools.com/react/", type: "article" }
  ],
  "State and Hooks": [
    { title: "React Hooks - GFG", url: "https://www.geeksforgeeks.org/reactjs-hooks/", type: "article" },
    { title: "useState Hook Docs", url: "https://react.dev/reference/react/useState", type: "docs" },
    { title: "useEffect Hook Docs", url: "https://react.dev/reference/react/useEffect", type: "docs" }
  ],
  "Introduction to SQL": [
    { title: "SQL Tutorial - GFG", url: "https://www.geeksforgeeks.org/sql-tutorial/", type: "article" },
    { title: "W3Schools SQL", url: "https://www.w3schools.com/sql/", type: "article" },
    { title: "PostgreSQL Tutorial", url: "https://www.postgresql.org/docs/current/tutorial.html", type: "docs" }
  ],
  "Introduction to Pandas": [
    { title: "Pandas Tutorial - GFG", url: "https://www.geeksforgeeks.org/pandas-tutorial/", type: "article" },
    { title: "Pandas Official Docs", url: "https://pandas.pydata.org/docs/getting_started/", type: "docs" },
    { title: "W3Schools Pandas", url: "https://www.w3schools.com/python/pandas/default.asp", type: "article" }
  ],
  "Neural Networks Basics": [
    { title: "Neural Networks - GFG", url: "https://www.geeksforgeeks.org/neural-networks-a-beginners-guide/", type: "article" },
    { title: "TensorFlow Tutorials", url: "https://www.tensorflow.org/tutorials", type: "docs" },
    { title: "Backpropagation - GFG", url: "https://www.geeksforgeeks.org/backpropagation-in-neural-network/", type: "article" }
  ],
  "Introduction to Docker": [
    { title: "Docker Tutorial - GFG", url: "https://www.geeksforgeeks.org/docker-tutorial/", type: "article" },
    { title: "Docker Official Docs", url: "https://docs.docker.com/get-started/", type: "docs" },
    { title: "W3Schools Docker", url: "https://www.w3schools.com/docker/", type: "article" }
  ],
  "Git Basics": [
    { title: "Git Tutorial - GFG", url: "https://www.geeksforgeeks.org/git-tutorial/", type: "article" },
    { title: "Git Official Docs", url: "https://git-scm.com/doc", type: "docs" },
    { title: "W3Schools Git", url: "https://www.w3schools.com/git/", type: "article" }
  ],
};

const getYouTubeId = (url) => {
  if (!url) return null;
  const match = url.match(/embed\/([^?]+)/);
  return match ? match[1] : null;
};

const LessonViewer = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [activeLesson, setActiveLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('content');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/login'); return; }
    fetchCourseData();
  }, [courseId]);

  const fetchCourseData = async () => {
    try {
      const [courseRes, lessonsRes, quizzesRes] = await Promise.all([
        api.get(`/courses/${courseId}`),
        api.get(`/courses/${courseId}/lessons`),
        api.get(`/quiz/course/${courseId}`)
      ]);
      setCourse(courseRes.data);
      setLessons(lessonsRes.data);
      setQuizzes(quizzesRes.data);
      if (lessonsRes.data.length > 0) {
        setActiveLesson(lessonsRes.data[0]);
      }
    } catch {
      toast.error('Failed to load course');
      navigate('/courses');
    } finally {
      setLoading(false);
    }
  };

  const currentIndex = lessons.findIndex(l => l.id === activeLesson?.id);
  const prevLesson = currentIndex > 0 ? lessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < lessons.length - 1 ? lessons[currentIndex + 1] : null;

  const lessonResources = activeLesson
    ? (LESSON_RESOURCES[activeLesson.title] || [
        { title: "GeeksForGeeks", url: "https://www.geeksforgeeks.org/", type: "article" },
        { title: "W3Schools", url: "https://www.w3schools.com/", type: "article" },
        { title: "MDN Web Docs", url: "https://developer.mozilla.org/", type: "docs" }
      ])
    : [];

  if (loading) return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex justify-center items-center h-64 text-gray-400">
        Loading course...
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-6">

        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-4">
          <Link to="/courses" className="hover:text-blue-600">Courses</Link>
          <FiChevronRight />
          <span className="text-gray-800 font-medium">{course?.title}</span>
          {activeLesson && (
            <>
              <FiChevronRight />
              <span className="text-blue-600">{activeLesson.title}</span>
            </>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

          {/* LEFT — Lesson Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-4">
                <h2 className="text-white font-bold text-sm">{course?.title}</h2>
                <p className="text-blue-200 text-xs mt-1">
                  {lessons.length} Lessons • {quizzes.length} Quizzes
                </p>
              </div>

              <div className="p-2">
                <p className="text-xs font-semibold text-gray-400 uppercase px-2 py-2">
                  Lessons
                </p>
                {lessons.map((lesson, i) => (
                  <button
                    key={lesson.id}
                    onClick={() => { setActiveLesson(lesson); setActiveTab('content'); }}
                    className={`w-full text-left px-3 py-3 rounded-xl mb-1 transition flex items-start gap-3 ${
                      activeLesson?.id === lesson.id
                        ? 'bg-blue-50 border-l-4 border-blue-500'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <span className={`text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${
                      activeLesson?.id === lesson.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-600'
                    }`}>
                      {i + 1}
                    </span>
                    <div>
                      <p className={`text-sm font-medium ${
                        activeLesson?.id === lesson.id ? 'text-blue-700' : 'text-gray-700'
                      }`}>
                        {lesson.title}
                      </p>
                      <p className="text-xs text-gray-400 mt-0.5 flex items-center gap-1">
                        <FiClock className="text-xs" /> {lesson.duration_minutes} min
                      </p>
                    </div>
                  </button>
                ))}

                {/* Quizzes List */}
                {quizzes.length > 0 && (
                  <>
                    <p className="text-xs font-semibold text-gray-400 uppercase px-2 py-2 mt-2">
                      Quizzes
                    </p>
                    {quizzes.map((quiz) => (
                      <button
                        key={quiz.id}
                        onClick={() => navigate(`/quiz/${quiz.id}`)}
                        className="w-full text-left px-3 py-3 rounded-xl mb-1 hover:bg-yellow-50 transition flex items-center gap-3"
                      >
                        <span className="text-yellow-500">📝</span>
                        <div>
                          <p className="text-sm font-medium text-gray-700">{quiz.title}</p>
                          <p className="text-xs text-gray-400">{quiz.total_marks} marks</p>
                        </div>
                      </button>
                    ))}
                  </>
                )}

                {/* Certificate Button in Sidebar */}
                <div className="px-2 pt-3 pb-2 mt-2 border-t border-gray-100">
                  <Link
                    to={`/certificate/${courseId}`}
                    className="flex items-center justify-center gap-2 w-full px-3 py-3 rounded-xl bg-gradient-to-r from-yellow-400 to-orange-400 text-white font-semibold text-sm hover:from-yellow-500 hover:to-orange-500 transition"
                  >
                    🎓 Get Certificate
                  </Link>
                </div>

              </div>
            </div>
          </div>

          {/* RIGHT — Main Content */}
          <div className="lg:col-span-3 space-y-4">

            {activeLesson && (
              <>
                {/* Video Player */}
                {activeLesson.video_url && (
                  <div className="bg-black rounded-2xl overflow-hidden shadow-lg">
                    <div className="relative" style={{ paddingBottom: '56.25%' }}>
                      <iframe
                        src={activeLesson.video_url}
                        title={activeLesson.title}
                        className="absolute inset-0 w-full h-full"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                      />
                    </div>
                  </div>
                )}

                {/* Lesson Title + Tabs */}
                <div className="bg-white rounded-2xl shadow-sm p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h1 className="text-2xl font-bold text-gray-800">
                        {activeLesson.title}
                      </h1>
                      <p className="text-gray-400 text-sm mt-1 flex items-center gap-1">
                        <FiClock /> {activeLesson.duration_minutes} minutes
                      </p>
                    </div>
                  </div>

                  {/* Tabs */}
                  <div className="flex gap-2 mb-6 border-b">
                    {['content', 'resources'].map((tab) => (
                      <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`px-4 py-2 text-sm font-medium capitalize border-b-2 transition ${
                          activeTab === tab
                            ? 'border-blue-600 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                        }`}
                      >
                        {tab === 'content' ? '📖 Lesson Notes' : '🔗 Resources'}
                      </button>
                    ))}
                  </div>

                  {/* Tab Content */}
                  {activeTab === 'content' && (
                    <div className="prose max-w-none">
                      <p className="text-gray-700 leading-relaxed text-base">
                        {activeLesson.content}
                      </p>
                    </div>
                  )}

                  {activeTab === 'resources' && (
                    <div className="space-y-3">
                      <p className="text-gray-500 text-sm mb-4">
                        📚 Curated resources to deepen your understanding of this topic:
                      </p>
                      {lessonResources.map((resource, i) => {
                        const config = resourceConfig[resource.type] || resourceConfig.article;
                        return (
                          <a
                            key={i}
                            href={resource.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`flex items-center gap-3 p-4 rounded-xl border-2 transition ${config.bg}`}
                          >
                            <span className="text-xl">{config.icon}</span>
                            <div className="flex-1">
                              <p className="font-semibold text-gray-800 text-sm">
                                {resource.title}
                              </p>
                              <p className="text-xs text-gray-500 mt-0.5">
                                {config.label} • Click to open
                              </p>
                            </div>
                            <FiExternalLink className="text-gray-400" />
                          </a>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Navigation Buttons */}
                <div className="flex justify-between items-center">
                  <button
                    onClick={() => prevLesson && setActiveLesson(prevLesson)}
                    disabled={!prevLesson}
                    className="flex items-center gap-2 px-5 py-3 rounded-xl border-2 border-gray-200 text-gray-600 hover:border-blue-400 hover:text-blue-600 transition disabled:opacity-40 disabled:cursor-not-allowed font-medium"
                  >
                    <FiChevronLeft /> Previous Lesson
                  </button>

                  <div className="flex gap-3">
                    {quizzes.length > 0 && !nextLesson && (
                      <button
                        onClick={() => navigate(`/quiz/${quizzes[0].id}`)}
                        className="flex items-center gap-2 px-5 py-3 rounded-xl bg-yellow-500 text-white hover:bg-yellow-600 transition font-semibold"
                      >
                        📝 Take Quiz
                      </button>
                    )}

                    {!nextLesson && (
                      <Link
                        to={`/certificate/${courseId}`}
                        className="flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-yellow-400 to-orange-400 text-white hover:from-yellow-500 hover:to-orange-500 transition font-semibold"
                      >
                        🎓 Get Certificate
                      </Link>
                    )}

                    <button
                      onClick={() => nextLesson && setActiveLesson(nextLesson)}
                      disabled={!nextLesson}
                      className="flex items-center gap-2 px-5 py-3 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition disabled:opacity-40 disabled:cursor-not-allowed font-semibold"
                    >
                      Next Lesson <FiChevronRight />
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LessonViewer;