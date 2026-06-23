import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FiAward } from 'react-icons/fi';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const MyCertificates = () => {
  const navigate = useNavigate();
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/login'); return; }
    api.get('/certificate/my-certificates')
      .then(res => setCertificates(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-8">
          <FiAward className="text-yellow-500 text-4xl" />
          <div>
            <h1 className="text-3xl font-bold text-gray-800">My Certificates</h1>
            <p className="text-gray-500">Your earned certifications</p>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-20 text-gray-400">Loading...</div>
        ) : certificates.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-sm p-12 text-center">
            <FiAward className="text-6xl text-gray-200 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-400 mb-2">
              No certificates yet!
            </h3>
            <p className="text-gray-400 mb-6">
              Complete a course with 70%+ quiz score to earn your certificate
            </p>
            <Link
              to="/courses"
              className="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              Browse Courses →
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {certificates.map((cert, i) => (
              <div key={i} className="bg-gradient-to-br from-gray-900 to-indigo-950 rounded-2xl p-6 border-2 border-yellow-400 shadow-lg">
                <div className="flex items-start justify-between mb-4">
                  <span className="text-4xl">🎓</span>
                  <span className="bg-yellow-400 text-yellow-900 text-xs font-bold px-3 py-1 rounded-full">
                    ⭐ {cert.quiz_score}%
                  </span>
                </div>
                <h3 className="text-white font-bold text-lg mb-1">
                  {cert.course_title}
                </h3>
                <p className="text-yellow-400 text-sm font-medium mb-1">
                  {cert.student_name}
                </p>
                <p className="text-gray-400 text-xs mb-4">
                  ID: {cert.certificate_id}
                </p>
                <p className="text-gray-500 text-xs mb-4">
                  Issued: {new Date(cert.issued_at).toLocaleDateString('en-IN', {
                    day: 'numeric', month: 'long', year: 'numeric'
                  })}
                </p>
                <Link
                  to={`/certificate/${cert.course_id}`}
                  className="block text-center bg-yellow-500 text-yellow-900 py-2 rounded-lg font-semibold text-sm hover:bg-yellow-400 transition"
                >
                  View & Download →
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MyCertificates;