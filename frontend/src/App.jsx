import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Courses from './pages/Courses';
import Quiz from './pages/Quiz';
import Recommendations from './pages/Recommendations';
import Performance from './pages/Performance';
import Leaderboard from './pages/Leaderboard';
import Chatbot from './pages/Chatbot';
import LessonViewer from './pages/LessonViewer';
import TimeAnalytics from './pages/TimeAnalytics';
import Certificate from './pages/Certificate';
import MyCertificates from './pages/MyCertificates';
import FloatingChatbot from './components/FloatingChatbot';

function App() {
  return (
    <Router>
      <Toaster position="top-right" />

      {/* Floating chatbot visible on ALL pages */}
      <FloatingChatbot />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/course/:courseId/learn" element={<LessonViewer />} />
        <Route path="/quiz/:quizId" element={<Quiz />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path="/performance" element={<Performance />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/time" element={<TimeAnalytics />} />
        <Route path="/certificate/:courseId" element={<Certificate />} />
        <Route path="/my-certificates" element={<MyCertificates />} />
      </Routes>
    </Router>
  );
}

export default App;