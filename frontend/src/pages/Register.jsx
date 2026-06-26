import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { MdSchool } from 'react-icons/md';
import { FiUser, FiMail, FiLock, FiUserPlus } from 'react-icons/fi';
import toast from 'react-hot-toast';
import api from '../services/api';

const Register = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '', email: '', password: '', role: 'student'
  });

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/auth/register', formData);
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      toast.success('Account created successfully!');
      navigate('/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-mesh" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>

      <div style={{ position: 'fixed', top: '10%', right: '5%', width: '300px', height: '300px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(99,102,241,0.15), transparent)', pointerEvents: 'none' }} />
      <div style={{ position: 'fixed', bottom: '10%', left: '5%', width: '250px', height: '250px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(245,158,11,0.1), transparent)', pointerEvents: 'none' }} />

      <div style={{ width: '100%', maxWidth: '420px' }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <div style={{
            width: '64px', height: '64px', borderRadius: '18px',
            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 16px', boxShadow: '0 0 40px rgba(245,158,11,0.4)'
          }}>
            <MdSchool style={{ fontSize: '32px', color: '#0a0a0f' }} />
          </div>
          <h1 style={{
            fontSize: '28px', fontWeight: '800',
            background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
          }}>Smart LMS</h1>
          <p style={{ color: '#64748b', fontSize: '14px', marginTop: '4px' }}>Join the AI-Powered Learning Platform</p>
        </div>

        <div className="glass" style={{ borderRadius: '24px', padding: '40px', boxShadow: '0 0 60px rgba(0,0,0,0.5)' }}>
          <h2 style={{ color: '#f1f5f9', fontSize: '22px', fontWeight: '700', marginBottom: '8px' }}>
            Create Account
          </h2>
          <p style={{ color: '#64748b', fontSize: '14px', marginBottom: '32px' }}>
            Start your learning journey today
          </p>

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {[
              { name: 'full_name', label: 'Full Name', type: 'text', placeholder: 'John Doe', icon: <FiUser /> },
              { name: 'email', label: 'Email Address', type: 'email', placeholder: 'you@example.com', icon: <FiMail /> },
              { name: 'password', label: 'Password', type: 'password', placeholder: '••••••••', icon: <FiLock /> },
            ].map((field) => (
              <div key={field.name}>
                <label style={{ color: '#94a3b8', fontSize: '13px', fontWeight: '600', marginBottom: '8px', display: 'block' }}>
                  {field.label}
                </label>
                <div style={{ position: 'relative' }}>
                  <span style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: '#475569' }}>
                    {field.icon}
                  </span>
                  <input
                    type={field.type} name={field.name} placeholder={field.placeholder}
                    value={formData[field.name]} onChange={handleChange} required
                    className="input-dark"
                    style={{ width: '100%', padding: '12px 14px 12px 40px', borderRadius: '12px', fontSize: '14px' }}
                  />
                </div>
              </div>
            ))}

            <div>
              <label style={{ color: '#94a3b8', fontSize: '13px', fontWeight: '600', marginBottom: '8px', display: 'block' }}>
                I am a...
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                {['student', 'teacher'].map(role => (
                  <button
                    key={role} type="button"
                    onClick={() => setFormData({ ...formData, role })}
                    style={{
                      padding: '10px', borderRadius: '10px', border: 'none',
                      cursor: 'pointer', fontWeight: '600', fontSize: '13px',
                      textTransform: 'capitalize', transition: 'all 0.2s ease',
                      background: formData.role === role
                        ? 'linear-gradient(135deg, #f59e0b, #d97706)'
                        : 'rgba(255,255,255,0.05)',
                      color: formData.role === role ? '#0a0a0f' : '#64748b',
                      border: formData.role === role
                        ? '1px solid transparent'
                        : '1px solid rgba(255,255,255,0.1)'
                    }}
                  >
                    {role === 'student' ? '🎓 Student' : '👨‍🏫 Teacher'}
                  </button>
                ))}
              </div>
            </div>

            <button
              type="submit" disabled={loading}
              className="btn-gold"
              style={{
                width: '100%', padding: '14px', borderRadius: '12px',
                border: 'none', cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '15px', marginTop: '8px',
                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
                opacity: loading ? 0.7 : 1
              }}
            >
              <FiUserPlus />
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <p style={{ textAlign: 'center', color: '#475569', fontSize: '14px', marginTop: '24px' }}>
            Already have an account?{' '}
            <Link to="/login" style={{ color: '#f59e0b', fontWeight: '600', textDecoration: 'none' }}>
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;