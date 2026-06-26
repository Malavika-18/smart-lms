import { Link } from 'react-router-dom';
import { MdSchool, MdAutoAwesome, MdPsychology } from 'react-icons/md';
import { FiArrowRight, FiBook, FiAward, FiTrendingUp } from 'react-icons/fi';

const features = [
  { icon: <MdAutoAwesome />, title: 'AI Recommendations', desc: 'Personalized course suggestions powered by collaborative filtering ML', color: '#f59e0b' },
  { icon: <MdPsychology />, title: 'Performance Prediction', desc: 'Random Forest model trained on 4,424 real students predicts your success', color: '#6366f1' },
  { icon: <FiBook />, title: 'Rich Course Content', desc: 'YouTube videos, GeeksForGeeks articles, and official docs for every lesson', color: '#10b981' },
  { icon: <FiAward />, title: 'Completion Certificates', desc: 'Earn verified certificates by scoring 70%+ on course quizzes', color: '#8b5cf6' },
  { icon: <FiTrendingUp />, title: 'Smart Analytics', desc: 'Track time spent, quiz history, and progress with beautiful charts', color: '#06b6d4' },
  { icon: <MdSchool />, title: 'AI SmartBot', desc: 'Groq-powered LLaMA AI assistant available on every page', color: '#f43f5e' },
];

const Home = () => {
  return (
    <div className="bg-mesh" style={{ minHeight: '100vh' }}>

      {/* Orbs */}
      <div style={{ position: 'fixed', top: '5%', left: '10%', width: '400px', height: '400px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(99,102,241,0.12), transparent)', pointerEvents: 'none' }} />
      <div style={{ position: 'fixed', bottom: '10%', right: '5%', width: '350px', height: '350px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(245,158,11,0.08), transparent)', pointerEvents: 'none' }} />

      {/* Navbar */}
      <nav style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '20px 48px',
        background: 'rgba(10,10,15,0.8)', backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        position: 'sticky', top: 0, zIndex: 100
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px', height: '36px', borderRadius: '10px',
            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 20px rgba(245,158,11,0.4)'
          }}>
            <MdSchool style={{ color: '#0a0a0f', fontSize: '20px' }} />
          </div>
          <span style={{
            fontSize: '18px', fontWeight: '800',
            background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
          }}>Smart LMS</span>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <Link to="/login" style={{
            padding: '10px 24px', borderRadius: '10px',
            border: '1px solid rgba(255,255,255,0.1)',
            color: '#94a3b8', textDecoration: 'none',
            fontSize: '14px', fontWeight: '600',
            background: 'rgba(255,255,255,0.03)',
            transition: 'all 0.2s'
          }}>
            Sign In
          </Link>
          <Link to="/register" style={{
            padding: '10px 24px', borderRadius: '10px',
            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
            color: '#0a0a0f', textDecoration: 'none',
            fontSize: '14px', fontWeight: '700',
            boxShadow: '0 0 20px rgba(245,158,11,0.3)'
          }}>
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '100px 48px 80px', textAlign: 'center' }}>
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '8px',
          padding: '8px 20px', borderRadius: '100px',
          background: 'rgba(245,158,11,0.1)',
          border: '1px solid rgba(245,158,11,0.3)',
          marginBottom: '32px'
        }}>
          <MdAutoAwesome style={{ color: '#f59e0b', fontSize: '16px' }} />
          <span style={{ color: '#f59e0b', fontSize: '13px', fontWeight: '600' }}>
            AI-Powered Learning Platform
          </span>
        </div>

        <h1 style={{
          fontSize: '72px', fontWeight: '900', lineHeight: 1.1,
          marginBottom: '24px', letterSpacing: '-2px'
        }}>
          <span style={{ color: '#f1f5f9' }}>Learn Smarter</span>
          <br />
          <span style={{
            background: 'linear-gradient(135deg, #f59e0b, #6366f1, #f59e0b)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            backgroundSize: '200% auto'
          }}>
            with AI Guidance
          </span>
        </h1>

        <p style={{ color: '#64748b', fontSize: '20px', maxWidth: '600px', margin: '0 auto 48px', lineHeight: 1.6 }}>
          Personalized recommendations, ML-powered performance prediction, and an AI assistant — all in one platform.
        </p>

        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
          <Link to="/register" style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '16px 36px', borderRadius: '14px',
            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
            color: '#0a0a0f', textDecoration: 'none',
            fontSize: '16px', fontWeight: '800',
            boxShadow: '0 0 40px rgba(245,158,11,0.4)',
            transition: 'all 0.3s ease'
          }}>
            Start Learning Free <FiArrowRight />
          </Link>
          <Link to="/login" style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '16px 36px', borderRadius: '14px',
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(255,255,255,0.1)',
            color: '#e2e8f0', textDecoration: 'none',
            fontSize: '16px', fontWeight: '600'
          }}>
            Sign In
          </Link>
        </div>

        {/* Stats */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '24px', maxWidth: '600px', margin: '80px auto 0'
        }}>
          {[
            { value: '10+', label: 'Expert Courses' },
            { value: '4,424', label: 'Students Analyzed' },
            { value: '100%', label: 'AI Powered' },
          ].map((stat, i) => (
            <div key={i} className="glass" style={{ borderRadius: '16px', padding: '20px' }}>
              <p style={{
                fontSize: '32px', fontWeight: '900',
                background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
              }}>
                {stat.value}
              </p>
              <p style={{ color: '#64748b', fontSize: '13px', marginTop: '4px' }}>{stat.label}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 48px 100px' }}>
        <h2 style={{
          textAlign: 'center', fontSize: '40px', fontWeight: '800',
          color: '#f1f5f9', marginBottom: '48px'
        }}>
          Everything you need to{' '}
          <span style={{
            background: 'linear-gradient(135deg, #f59e0b, #6366f1)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
          }}>excel</span>
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
          {features.map((f, i) => (
            <div key={i} className="glass card-hover" style={{ borderRadius: '20px', padding: '28px' }}>
              <div style={{
                width: '48px', height: '48px', borderRadius: '14px',
                background: `${f.color}20`, border: `1px solid ${f.color}40`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '24px', color: f.color, marginBottom: '16px'
              }}>
                {f.icon}
              </div>
              <h3 style={{ color: '#f1f5f9', fontWeight: '700', fontSize: '16px', marginBottom: '8px' }}>
                {f.title}
              </h3>
              <p style={{ color: '#64748b', fontSize: '14px', lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;