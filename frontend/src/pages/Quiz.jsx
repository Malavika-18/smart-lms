import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const Quiz = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchQuiz();
  }, [quizId]);

  const fetchQuiz = async () => {
    try {
      const res = await api.get(`/quiz/${quizId}`);
      setQuiz(res.data);
    } catch {
      toast.error('Failed to load quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, option) => {
    setAnswers({ ...answers, [questionId]: option });
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length < quiz.questions.length) {
      toast.error('Please answer all questions!');
      return;
    }
    setSubmitting(true);
    try {
      const submission = {
        answers: Object.entries(answers).map(([question_id, selected_option]) => ({
          question_id: parseInt(question_id),
          selected_option
        }))
      };
      const res = await api.post(`/quiz/${quizId}/submit`, submission);
      setResult(res.data);
      toast.success('Quiz submitted!');
    } catch {
      toast.error('Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="flex justify-center items-center h-64 text-gray-400">Loading quiz...</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-3xl mx-auto px-4 py-8">
        {result ? (
          // Result Screen
          <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
            <div className={`text-6xl mb-4 ${result.passed ? '🎉' : '😔'}`}>
              {result.passed ? '🎉' : '😔'}
            </div>
            <h2 className="text-3xl font-bold mb-2">
              {result.passed ? 'You Passed!' : 'Keep Trying!'}
            </h2>
            <p className="text-gray-500 mb-6">Here are your results</p>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-blue-50 rounded-xl p-4">
                <p className="text-3xl font-bold text-blue-600">{result.score}/{result.total_marks}</p>
                <p className="text-gray-500 text-sm">Score</p>
              </div>
              <div className="bg-green-50 rounded-xl p-4">
                <p className="text-3xl font-bold text-green-600">{result.percentage}%</p>
                <p className="text-gray-500 text-sm">Percentage</p>
              </div>
              <div className="bg-emerald-50 rounded-xl p-4">
                <p className="text-3xl font-bold text-emerald-600">{result.correct_count}</p>
                <p className="text-gray-500 text-sm">Correct</p>
              </div>
              <div className="bg-red-50 rounded-xl p-4">
                <p className="text-3xl font-bold text-red-500">{result.wrong_count}</p>
                <p className="text-gray-500 text-sm">Wrong</p>
              </div>
            </div>
            <button
              onClick={() => navigate('/courses')}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Back to Courses
            </button>
          </div>
        ) : (
          // Quiz Screen
          <>
            <div className="bg-white rounded-2xl shadow-md p-6 mb-6">
              <h1 className="text-2xl font-bold text-gray-800">{quiz?.title}</h1>
              <p className="text-gray-500 mt-1">
                {quiz?.questions?.length} Questions • {quiz?.total_marks} Marks
              </p>
            </div>

            <div className="space-y-6">
              {quiz?.questions?.map((q, index) => (
                <div key={q.id} className="bg-white rounded-xl shadow-md p-6">
                  <p className="font-semibold text-gray-800 mb-4">
                    Q{index + 1}. {q.question_text}
                  </p>
                  <div className="space-y-3">
                    {['a', 'b', 'c', 'd'].map((opt) => (
                      <button
                        key={opt}
                        onClick={() => handleAnswer(q.id, opt)}
                        className={`w-full text-left px-4 py-3 rounded-lg border-2 transition font-medium ${
                          answers[q.id] === opt
                            ? 'border-blue-500 bg-blue-50 text-blue-700'
                            : 'border-gray-200 hover:border-blue-300 text-gray-700'
                        }`}
                      >
                        <span className="uppercase font-bold mr-2">{opt}.</span>
                        {q[`option_${opt}`]}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="w-full mt-8 bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : 'Submit Quiz'}
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default Quiz;