import { Link, useNavigate } from 'react-router-dom';
import { FiLogOut } from 'react-icons/fi';
import {
  MdSchool, MdAutoAwesome, MdPsychology,
  MdLeaderboard, MdSmartToy, MdTimer
} from 'react-icons/md';
import { FiAward } from 'react-icons/fi';

const Navbar = () => {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md px-6 py-3 flex justify-between items-center">
      <Link to="/dashboard" className="flex items-center gap-2">
        <MdSchool className="text-blue-600 text-3xl" />
        <span className="text-xl font-bold text-blue-600">Smart LMS</span>
      </Link>
      <div className="flex items-center gap-3 text-sm flex-wrap">
        <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 font-medium">Dashboard</Link>
        <Link to="/courses" className="text-gray-600 hover:text-blue-600 font-medium">Courses</Link>
        <Link to="/recommendations" className="flex items-center gap-1 text-gray-600 hover:text-blue-600 font-medium">
          <MdAutoAwesome className="text-yellow-500" /> AI Picks
        </Link>
        <Link to="/performance" className="flex items-center gap-1 text-gray-600 hover:text-blue-600 font-medium">
          <MdPsychology className="text-purple-500" /> Performance
        </Link>
        <Link to="/leaderboard" className="flex items-center gap-1 text-gray-600 hover:text-blue-600 font-medium">
          <MdLeaderboard className="text-green-500" /> Leaderboard
        </Link>
        <Link to="/my-certificates" className="flex items-center gap-1 text-gray-600 hover:text-yellow-600 font-medium">
          <FiAward className="text-yellow-500" /> Certificates
        </Link>
        <Link to="/time" className="flex items-center gap-1 text-gray-600 hover:text-blue-600 font-medium">
          <MdTimer className="text-orange-500" /> Time
        </Link>
        <Link to="/chatbot" className="flex items-center gap-1 text-gray-600 hover:text-blue-600 font-medium">
          <MdSmartToy className="text-blue-500" /> SmartBot
        </Link>
        <button
          onClick={handleLogout}
          className="flex items-center gap-1 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
        >
          <FiLogOut /> Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
