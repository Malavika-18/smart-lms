import { Link, useLocation, useNavigate } from 'react-router-dom';
import { FiLogOut, FiAward, FiClock } from 'react-icons/fi';
import {
  MdSchool, MdAutoAwesome, MdPsychology,
  MdLeaderboard, MdSmartToy, MdDashboard,
  MdMenuBook
} from 'react-icons/md';

const navLinks = [
  { to: '/dashboard', label: 'Dashboard', icon: <MdDashboard /> },
  { to: '/courses', label: 'Courses', icon: <MdMenuBook /> },
  { to: '/recommendations', label: 'AI Picks', icon: <MdAutoAwesome /> },
  { to: '/performance', label: 'Performance', icon: <MdPsychology /> },
  { to: '/leaderboard', label: 'Leaderboard', icon: <MdLeaderboard /> },
  { to: '/my-certificates', label: 'Certificates', icon: <FiAward /> },
  { to: '/time', label: 'Time', icon: <FiClock /> },
  { to: '/chatbot', label: 'SmartBot', icon: <MdSmartToy /> },
];

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <nav style={{
      background: 'rgba(10,10,15,0.95)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(245,158,11,0.2)',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
      boxShadow: '0 4px 30px rgba(0,0,0,0.5)'
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '0 24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '64px'
      }}>

        {/* Logo */}
        <Link to="/dashboard" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          textDecoration: 'none'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
            borderRadius: '10px',
            padding: '6px',
            display: 'flex',
            boxShadow: '0 0 20px rgba(245,158,11,0.4)'
          }}>
            <MdSchool style={{ color: '#0a0a0f', fontSize: '20px' }} />
          </div>
          <span style={{
            fontSize: '18px',
            fontWeight: '800',
            background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '-0.5px'
          }}>
            Smart LMS
          </span>
        </Link>

        {/* Nav Links */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px'
        }}>
          {navLinks.map((link) => {
            const isActive = location.pathname === link.to;
            return (
              <Link
                key={link.to}
                to={link.to}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  padding: '6px 10px',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  fontSize: '13px',
                  fontWeight: isActive ? '700' : '500',
                  color: isActive ? '#f59e0b' : '#94a3b8',
                  background: isActive ? 'rgba(245,158,11,0.1)' : 'transparent',
                  border: isActive ? '1px solid rgba(245,158,11,0.3)' : '1px solid transparent',
                  transition: 'all 0.2s ease',
                  textShadow: isActive ? '0 0 15px rgba(245,158,11,0.5)' : 'none'
                }}
                onMouseEnter={e => {
                  if (!isActive) {
                    e.currentTarget.style.color = '#e2e8f0';
                    e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                  }
                }}
                onMouseLeave={e => {
                  if (!isActive) {
                    e.currentTarget.style.color = '#94a3b8';
                    e.currentTarget.style.background = 'transparent';
                  }
                }}
              >
                <span style={{ fontSize: '15px' }}>{link.icon}</span>
                {link.label}
              </Link>
            );
          })}
        </div>

        {/* Logout */}
        <button
          onClick={handleLogout}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '8px 16px',
            borderRadius: '8px',
            border: '1px solid rgba(239,68,68,0.3)',
            background: 'rgba(239,68,68,0.1)',
            color: '#ef4444',
            cursor: 'pointer',
            fontSize: '13px',
            fontWeight: '600',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={e => {
            e.currentTarget.style.background = 'rgba(239,68,68,0.2)';
            e.currentTarget.style.boxShadow = '0 0 20px rgba(239,68,68,0.3)';
          }}
          onMouseLeave={e => {
            e.currentTarget.style.background = 'rgba(239,68,68,0.1)';
            e.currentTarget.style.boxShadow = 'none';
          }}
        >
          <FiLogOut /> Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;