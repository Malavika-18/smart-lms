import { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiSend, FiUser } from 'react-icons/fi';
import { MdSmartToy } from 'react-icons/md';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/layout/Navbar';

const Chatbot = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm SmartBot 🤖 Your AI learning assistant. Ask me anything about your courses, study tips, or any academic topic!"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/login'); return; }
    fetchSuggestions();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchSuggestions = async () => {
    try {
      const res = await api.get('/chatbot/suggestions');
      setSuggestions(res.data.suggestions);
    } catch {
      console.error('Failed to load suggestions');
    }
  };

  const sendMessage = async (text) => {
    const messageText = text || input.trim();
    if (!messageText) return;

    const userMessage = { role: 'user', content: messageText };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      // Only send actual conversation history, not the first bot greeting
      const historyToSend = messages
        .slice(1)  // Skip the initial greeting
        .slice(-10)
        .map(m => ({ role: m.role, content: m.content }));

      const res = await api.post('/chatbot/chat', {
        message: messageText,
        history: historyToSend
      });

      setMessages([
        ...newMessages,
        { role: 'assistant', content: res.data.response }
      ]);
    } catch {
      toast.error('Failed to get response');
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: "Sorry, I'm having trouble connecting. Please try again! 🔄"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />
      <div className="max-w-4xl mx-auto w-full px-4 py-6 flex flex-col flex-1">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="bg-blue-600 p-2 rounded-xl">
            <MdSmartToy className="text-white text-2xl" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-800">SmartBot</h1>
            <p className="text-green-500 text-sm font-medium flex items-center gap-1">
              <span className="w-2 h-2 bg-green-500 rounded-full inline-block" />
              AI Assistant Online
            </p>
          </div>
        </div>

        {/* Suggestions */}
        {messages.length === 1 && (
          <div className="mb-4">
            <p className="text-gray-500 text-sm mb-2">Try asking:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(s)}
                  className="bg-white border border-gray-200 text-gray-600 text-sm px-3 py-2 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 bg-white rounded-2xl shadow-sm p-4 mb-4 overflow-y-auto max-h-[500px]">
          <div className="space-y-4">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  msg.role === 'user'
                    ? 'bg-blue-600'
                    : 'bg-gradient-to-br from-purple-500 to-blue-600'
                }`}>
                  {msg.role === 'user'
                    ? <FiUser className="text-white text-sm" />
                    : <MdSmartToy className="text-white text-sm" />
                  }
                </div>

                {/* Bubble */}
                <div className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-gray-100 text-gray-800 rounded-tl-none'
                }`}>
                  {msg.content}
                </div>
              </div>
            ))}

            {/* Typing indicator */}
            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center">
                  <MdSmartToy className="text-white text-sm" />
                </div>
                <div className="bg-gray-100 px-4 py-3 rounded-2xl rounded-tl-none">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask SmartBot anything... (Press Enter to send)"
            rows={1}
            className="flex-1 border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            className="bg-blue-600 text-white px-5 py-3 rounded-xl hover:bg-blue-700 transition disabled:opacity-50 flex items-center gap-2"
          >
            <FiSend />
          </button>
        </div>
        <p className="text-xs text-gray-400 text-center mt-2">
          Powered by Claude AI • Press Enter to send, Shift+Enter for new line
        </p>
      </div>
    </div>
  );
};

export default Chatbot;