import { Link, useNavigate } from 'react-router-dom';
import { FiLogOut } from 'react-icons/fi';
import { MdSchool, MdAutoAwesome } from 'react-icons/md';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
      <div className="flex items-center gap-2">
        <MdSchool className="text-blue-600 text-3xl" />
        <span className="text-xl font-bold text-blue-600">Smart LMS</span>
      </div>
      <div className="flex items-center gap-4">
        <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 font-medium">
          Dashboard
        </Link>
        <Link to="/courses" className="text-gray-600 hover:text-blue-600 font-medium">
          Courses
        </Link>
        <Link to="/recommendations" className="flex items-center gap-1 text-gray-600 hover:text-blue-600 font-medium">
          <MdAutoAwesome className="text-yellow-500" />
          AI Picks
        </Link>
        <button
          onClick={handleLogout}
          className="flex items-center gap-1 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
        >
          <FiLogOut />
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;