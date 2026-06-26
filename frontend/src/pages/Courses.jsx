import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiBook, FiLock, FiStar } from 'react-icons/fi';
import { MdVerified } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';
import useTimeTracker from '../hooks/useTimeTracker';

const difficultyConfig = {
  beginner: { color: '#10b981', bg: 'rgba(16,185,129,0.1)', border: 'rgba(16,185,129,0.3)' },
  intermediate: { color: '#f59e0b', bg: 'rgba(245,158,11,0.1)', border: 'rgba(245,158,11,0.3)' },
  advanced: { color: '#ef4444', bg: 'rgba(239,68,68,0.1)', border: 'rgba(239,68,68,0.3)' },
};

const CourseCard = ({ course, isEnrolled, onEnroll, onBuy, onView, buying }) => {
  const diff = difficultyConfig[course.difficulty_level] || difficultyConfig.beginner;

  return (
    <div className="card-hover" style={{
      background: 'rgba(255,255,255,0.03)',
      border: course.is_premium
        ? '1px solid rgba(245,158,11,0.3)'
        : '1px solid rgba(255,255,255,0.08)',
      borderRadius: '20px',
      overflow: 'hidden',
      boxShadow: course.is_premium ? '0 0 30px rgba(245,158,11,0.1)' : 'none'
    }}>
      {/* Thumbnail */}
      <div style={{
        height: '140px',
        background: course.is_premium
          ? 'linear-gradient(135deg, rgba(245,158,11,0.3), rgba(217,119,6,0.2))'
          : 'linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.2))',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        position: 'relative'
      }}>
        <FiBook style={{
          fontSize: '48px',
          color: course.is_premium ? '#f59e0b' : '#6366f1',
          opacity: 0.8
        }} />
        {course.is_premium && (
          <div style={{
            position: 'absolute', top: '12px', right: '12px',
            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
            color: '#0a0a0f', fontSize: '11px', fontWeight: '800',
            padding: '4px 10px', borderRadius: '20px',
            display: 'flex', alignItems: 'center', gap: '4px'
          }}>
            <MdVerified style={{ fontSize: '12px' }} /> PREMIUM
          </div>
        )}
        {isEnrolled && (
          <div style={{
            position: 'absolute', top: '12px', left: '12px',
            background: 'rgba(16,185,129,0.9)',
            color: 'white', fontSize: '11px', fontWeight: '700',
            padding: '4px 10px', borderRadius: '20px'
          }}>
            ✅ Enrolled
          </div>
        )}
      </div>

      {/* Content */}
      <div style={{ padding: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
          <h3 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '15px', flex: 1, marginRight: '8px', lineHeight: 1.3 }}>
            {course.title}
          </h3>
          <span style={{
            fontSize: '11px', padding: '3px 8px', borderRadius: '20px',
            background: diff.bg, border: `1px solid ${diff.border}`,
            color: diff.color, fontWeight: '600', flexShrink: 0
          }}>
            {course.difficulty_level}
          </span>
        </div>

        <p style={{ color: '#475569', fontSize: '13px', marginBottom: '16px', lineHeight: 1.5 }}
           className="line-clamp-2">
          {course.description || 'No description available'}
        </p>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <span style={{
            fontSize: '12px', padding: '3px 10px', borderRadius: '20px',
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(255,255,255,0.1)',
            color: '#64748b'
          }}>
            {course.category || 'General'}
          </span>
          {course.is_premium ? (
            <span style={{ color: '#f59e0b', fontWeight: '800', fontSize: '18px' }}>
              ₹{parseFloat(course.price).toFixed(0)}
            </span>
          ) : (
            <span style={{ color: '#10b981', fontWeight: '700', fontSize: '14px' }}>FREE</span>
          )}
        </div>

        {/* Buttons */}
        {isEnrolled ? (
          <button onClick={onView} className="btn-gold" style={{
            width: '100%', padding: '10px', borderRadius: '10px',
            border: 'none', cursor: 'pointer', fontSize: '14px'
          }}>
            Continue Learning →
          </button>
        ) : course.is_premium ? (
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={onBuy} disabled={buying} style={{
              flex: 1, padding: '10px', borderRadius: '10px',
              border: 'none', cursor: buying ? 'not-allowed' : 'pointer',
              background: 'linear-gradient(135deg, #f59e0b, #d97706)',
              color: '#0a0a0f', fontWeight: '700', fontSize: '13px',
              opacity: buying ? 0.7 : 1
            }}>
              {buying ? 'Processing...' : `Buy ₹${parseFloat(course.price).toFixed(0)}`}
            </button>
            <button onClick={onView} style={{
              padding: '10px 14px', borderRadius: '10px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#94a3b8', cursor: 'pointer', fontSize: '13px'
            }}>
              Preview
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={onEnroll} style={{
              flex: 1, padding: '10px', borderRadius: '10px',
              border: 'none', cursor: 'pointer',
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: 'white', fontWeight: '700', fontSize: '13px'
            }}>
              Enroll Free
            </button>
            <button onClick={onView} style={{
              padding: '10px 14px', borderRadius: '10px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#94a3b8', cursor: 'pointer', fontSize: '13px'
            }}>
              Preview
            </button>
          </div>
        )}
      </div>
    </div>
  );
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
    } catch { toast.error('Failed to load courses'); }
    finally { setLoading(false); }
  };

  const fetchEnrollments = async () => {
    try {
      const res = await api.get('/courses/my/enrollments');
      setEnrolledIds(new Set(res.data.map(e => e.course_id)));
    } catch {}
  };

  const handleEnroll = async (courseId) => {
    try {
      await api.post(`/courses/${courseId}/enroll`);
      toast.success('Enrolled successfully!');
      setEnrolledIds(prev => new Set([...prev, courseId]));
    } catch (err) {
      const detail = err.response?.data?.detail;
      toast.error(detail === 'PREMIUM_REQUIRED' ? 'This is a premium course. Please purchase it!' : detail || 'Enrollment failed');
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
    } finally { setBuyingId(null); }
  };

  const freeCourses = courses.filter(c => !c.is_premium);
  const premiumCourses = courses.filter(c => c.is_premium);

  const SectionHeader = ({ icon, title, count, color }) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
      <div style={{
        width: '36px', height: '36px', borderRadius: '10px',
        background: `${color}20`, border: `1px solid ${color}40`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        color: color, fontSize: '18px'
      }}>
        {icon}
      </div>
      <h2 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '20px' }}>{title}</h2>
      <span style={{
        padding: '4px 12px', borderRadius: '20px',
        background: `${color}15`, border: `1px solid ${color}30`,
        color: color, fontSize: '12px', fontWeight: '700'
      }}>
        {count} Available
      </span>
    </div>
  );

  return (
    <div className="bg-mesh" style={{ minHeight: '100vh' }}>
      <Navbar />
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '32px 24px' }}>

        {/* Header */}
        <div style={{ marginBottom: '40px' }}>
          <h1 style={{
            fontSize: '36px', fontWeight: '900', color: '#f1f5f9', marginBottom: '8px'
          }}>
            Browse <span style={{
              background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
              WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
            }}>Courses</span>
          </h1>
          <p style={{ color: '#64748b', fontSize: '16px' }}>
            Explore our AI-curated learning paths
          </p>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '80px 0', color: '#475569' }}>
            Loading courses...
          </div>
        ) : (
          <>
            {/* Free Courses */}
            <div style={{ marginBottom: '48px' }}>
              <SectionHeader icon={<FiBook />} title="Free Courses" count={freeCourses.length} color="#6366f1" />
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
                {freeCourses.map(course => (
                  <CourseCard
                    key={course.id} course={course}
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
              <SectionHeader icon={<FiLock />} title="Premium Courses" count={premiumCourses.length} color="#f59e0b" />
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
                {premiumCourses.map(course => (
                  <CourseCard
                    key={course.id} course={course}
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

export default Courses;