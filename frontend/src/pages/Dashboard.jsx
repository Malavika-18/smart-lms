import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MdSchool } from 'react-icons/md';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (!stored) {
      navigate('/login');
    } else {
      setUser(JSON.parse(stored));
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <MdSchool className="text-blue-600 text-6xl mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-gray-800">
          Welcome, {user?.full_name}! 👋
        </h1>
        <p className="text-gray-500 mt-2">Role: {user?.role}</p>
        <p className="text-blue-600 mt-4 font-medium">
          Dashboard coming in next phase!
        </p>
      </div>
    </div>
  );
};

export default Dashboard;