import { Link } from 'react-router-dom';
import { MdSchool } from 'react-icons/md';
import { FiArrowRight } from 'react-icons/fi';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center justify-center px-4">
      <div className="text-center max-w-3xl">
        <div className="flex justify-center mb-6">
          <MdSchool className="text-blue-600 text-8xl" />
        </div>
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          Smart <span className="text-blue-600">LMS</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-Powered Learning Management System — Personalized, Intelligent, Effective
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/login"
            className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition flex items-center gap-2"
          >
            Get Started <FiArrowRight />
          </Link>
          <Link
            to="/register"
            className="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-50 transition"
          >
            Register
          </Link>
        </div>
        <div className="mt-16 grid grid-cols-3 gap-8">
          {[
            { title: "AI Recommendations", desc: "Personalized learning paths" },
            { title: "Smart Analytics", desc: "Track your progress in real-time" },
            { title: "Live Assessments", desc: "Instant AI-powered feedback" },
          ].map((feature, i) => (
            <div key={i} className="bg-white p-6 rounded-xl shadow-md">
              <h3 className="font-bold text-gray-800 mb-2">{feature.title}</h3>
              <p className="text-gray-500 text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;