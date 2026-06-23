import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { FiAward, FiDownload, FiCheck, FiX } from 'react-icons/fi';
import { MdVerified, MdSchool } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const Certificate = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const certRef = useRef();
  const [eligibility, setEligibility] = useState(null);
  const [certData, setCertData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/login'); return; }
    checkEligibility();
  }, [courseId]);

  const checkEligibility = async () => {
    try {
      const res = await api.get(`/certificate/check/${courseId}`);
      setEligibility(res.data);
      if (res.data.certificate_issued) {
        // Load existing cert data
        const certs = await api.get('/certificate/my-certificates');
        const cert = certs.data.find(c => c.course_id === parseInt(courseId));
        if (cert) setCertData(cert);
      }
    } catch {
      toast.error('Failed to check eligibility');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const res = await api.post(`/certificate/generate/${courseId}`);
      setCertData(res.data);
      setEligibility(prev => ({ ...prev, certificate_issued: true }));
      toast.success('🎓 Certificate Generated!');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to generate');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = () => {
    // Print the certificate
    const printContent = certRef.current.innerHTML;
    const win = window.open('', '_blank');
    win.document.write(`
      <html>
        <head>
          <title>Certificate - ${certData?.course_title}</title>
          <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600&display=swap');
            body { margin: 0; background: #0f172a; }
          </style>
        </head>
        <body>${printContent}</body>
      </html>
    `);
    win.document.close();
    win.print();
    toast.success('Certificate sent to printer!');
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
    return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
  };

  if (loading) return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex justify-center items-center h-64 text-gray-400">
        Checking eligibility...
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">

        <div className="flex items-center gap-3 mb-8">
          <FiAward className="text-yellow-500 text-4xl" />
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Course Certificate</h1>
            <p className="text-gray-500">Complete the course to earn your certificate</p>
          </div>
        </div>

        {/* Eligibility Card */}
        {!certData && (
          <div className="bg-white rounded-2xl shadow-sm p-6 mb-6">
            <h2 className="text-lg font-bold text-gray-800 mb-4">
              📋 Certificate Requirements
            </h2>
            <div className="space-y-3 mb-6">
              <div className={`flex items-center gap-3 p-3 rounded-xl ${
                eligibility?.quiz_passed ? 'bg-green-50' : 'bg-red-50'
              }`}>
                {eligibility?.quiz_passed
                  ? <FiCheck className="text-green-500 text-xl" />
                  : <FiX className="text-red-500 text-xl" />
                }
                <div>
                  <p className="font-semibold text-gray-800">
                    Quiz Score ≥ 70%
                  </p>
                  <p className="text-sm text-gray-500">
                    Your best score: <span className="font-bold">
                      {eligibility?.quiz_best_score || 0}%
                    </span>
                    {!eligibility?.quiz_passed && (
                      <span className="text-red-500 ml-2">
                        (Need {eligibility?.required_score}%)
                      </span>
                    )}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 rounded-xl bg-blue-50">
                <FiCheck className="text-blue-500 text-xl" />
                <div>
                  <p className="font-semibold text-gray-800">Enrolled in Course</p>
                  <p className="text-sm text-gray-500">✅ Confirmed</p>
                </div>
              </div>
            </div>

            {eligibility?.eligible && !eligibility?.certificate_issued ? (
              <button
                onClick={handleGenerate}
                disabled={generating}
                className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 text-white py-4 rounded-xl font-bold text-lg hover:from-yellow-600 hover:to-orange-600 transition disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <FiAward />
                {generating ? 'Generating...' : '🎓 Generate My Certificate!'}
              </button>
            ) : !eligibility?.eligible ? (
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4 text-center">
                <p className="text-red-600 font-semibold">{eligibility?.reason}</p>
                <Link
                  to={`/course/${courseId}/learn`}
                  className="mt-3 inline-block bg-blue-600 text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition"
                >
                  Go Back to Course →
                </Link>
              </div>
            ) : null}
          </div>
        )}

        {/* Certificate Display */}
        {(certData || eligibility?.certificate_issued) && certData && (
          <div>
            {/* Download Button */}
            <div className="flex justify-end mb-4">
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
              >
                <FiDownload /> Download Certificate
              </button>
            </div>

            {/* Dark Premium Certificate */}
            <div ref={certRef}>
              <div style={{
                background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)',
                border: '3px solid #f59e0b',
                borderRadius: '16px',
                padding: '60px',
                textAlign: 'center',
                position: 'relative',
                overflow: 'hidden',
                minHeight: '500px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 60px rgba(245,158,11,0.2)'
              }}>
                {/* Corner decorations */}
                {['top-4 left-4', 'top-4 right-4', 'bottom-4 left-4', 'bottom-4 right-4'].map((pos, i) => (
                  <div key={i} style={{
                    position: 'absolute',
                    [pos.includes('top') ? 'top' : 'bottom']: '16px',
                    [pos.includes('left') ? 'left' : 'right']: '16px',
                    width: '40px',
                    height: '40px',
                    border: '2px solid #f59e0b',
                    borderRadius: '4px'
                  }} />
                ))}

                {/* Header */}
                <div style={{ marginBottom: '24px' }}>
                  <div style={{
                    fontSize: '48px',
                    marginBottom: '8px'
                  }}>🎓</div>
                  <p style={{
                    color: '#f59e0b',
                    fontSize: '14px',
                    letterSpacing: '6px',
                    textTransform: 'uppercase',
                    fontWeight: '600',
                    fontFamily: 'sans-serif'
                  }}>
                    Smart Learning Management System
                  </p>
                </div>

                {/* Certificate of Completion */}
                <h1 style={{
                  color: '#ffffff',
                  fontSize: '42px',
                  fontWeight: '700',
                  marginBottom: '8px',
                  fontFamily: 'Georgia, serif',
                  textShadow: '0 0 30px rgba(245,158,11,0.5)'
                }}>
                  Certificate of Completion
                </h1>

                <div style={{
                  width: '200px',
                  height: '2px',
                  background: 'linear-gradient(90deg, transparent, #f59e0b, transparent)',
                  margin: '16px auto'
                }} />

                <p style={{
                  color: '#94a3b8',
                  fontSize: '16px',
                  marginBottom: '24px',
                  fontFamily: 'sans-serif'
                }}>
                  This is to certify that
                </p>

                {/* Student Name */}
                <h2 style={{
                  color: '#f59e0b',
                  fontSize: '48px',
                  fontWeight: '700',
                  marginBottom: '16px',
                  fontFamily: 'Georgia, serif',
                  textShadow: '0 0 20px rgba(245,158,11,0.4)'
                }}>
                  {certData.student_name}
                </h2>

                <p style={{
                  color: '#94a3b8',
                  fontSize: '16px',
                  marginBottom: '12px',
                  fontFamily: 'sans-serif'
                }}>
                  has successfully completed the course
                </p>

                {/* Course Name */}
                <h3 style={{
                  color: '#e2e8f0',
                  fontSize: '28px',
                  fontWeight: '700',
                  marginBottom: '24px',
                  fontFamily: 'Georgia, serif',
                  padding: '12px 32px',
                  border: '1px solid #334155',
                  borderRadius: '8px',
                  background: 'rgba(255,255,255,0.05)'
                }}>
                  {certData.course_title}
                </h3>

                {/* Score Badge */}
                <div style={{
                  background: 'linear-gradient(135deg, #f59e0b, #ef4444)',
                  borderRadius: '50px',
                  padding: '10px 28px',
                  marginBottom: '32px',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '8px'
                }}>
                  <span style={{ fontSize: '20px' }}>⭐</span>
                  <span style={{
                    color: '#ffffff',
                    fontWeight: '700',
                    fontSize: '18px',
                    fontFamily: 'sans-serif'
                  }}>
                    Score: {certData.quiz_score}%
                  </span>
                </div>

                {/* Footer */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  width: '100%',
                  marginTop: '16px',
                  paddingTop: '24px',
                  borderTop: '1px solid #1e293b'
                }}>
                  <div style={{ textAlign: 'left' }}>
                    <p style={{
                      color: '#f59e0b',
                      fontWeight: '700',
                      fontSize: '14px',
                      fontFamily: 'sans-serif'
                    }}>
                      Dr. Sarah Johnson
                    </p>
                    <p style={{
                      color: '#64748b',
                      fontSize: '12px',
                      fontFamily: 'sans-serif'
                    }}>
                      Course Instructor
                    </p>
                  </div>
                  <div style={{ textAlign: 'center' }}>
                    <p style={{
                      color: '#64748b',
                      fontSize: '12px',
                      fontFamily: 'sans-serif'
                    }}>
                      Certificate ID
                    </p>
                    <p style={{
                      color: '#94a3b8',
                      fontSize: '13px',
                      fontWeight: '600',
                      fontFamily: 'monospace'
                    }}>
                      {certData.certificate_id}
                    </p>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <p style={{
                      color: '#64748b',
                      fontSize: '12px',
                      fontFamily: 'sans-serif'
                    }}>
                      Date of Completion
                    </p>
                    <p style={{
                      color: '#94a3b8',
                      fontSize: '13px',
                      fontWeight: '600',
                      fontFamily: 'sans-serif'
                    }}>
                      {formatDate(certData.issued_at)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Certificate;