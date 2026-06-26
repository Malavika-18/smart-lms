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
      const historyToSend = messages
        .slice(1)
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
    <div className="bg-mesh" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar />
      <div style={{ maxWidth: '900px', margin: '0 auto', width: '100%', padding: '24px', display: 'flex', flexDirection: 'column', flex: 1 }}>

        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
          <div style={{
            width: '52px', height: '52px', borderRadius: '14px',
            background: 'linear-gradient(135deg, #f59e0b, #d97706)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 30px rgba(245,158,11,0.4)'
          }}>
            <MdSmartToy style={{ color: '#0a0a0f', fontSize: '28px' }} />
          </div>
          <div>
            <h1 style={{ fontSize: '24px', fontWeight: '800', color: '#f1f5f9' }}>SmartBot</h1>
            <p style={{ color: '#10b981', fontSize: '13px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ width: '8px', height: '8px', background: '#10b981', borderRadius: '50%', display: 'inline-block' }} />
              AI Assistant Online
            </p>
          </div>
        </div>

        {/* Suggestions */}
        {messages.length === 1 && (
          <div style={{ marginBottom: '16px' }}>
            <p style={{ color: '#64748b', fontSize: '13px', marginBottom: '8px' }}>Try asking:</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  onClick={() => sendMessage(s)}
                  style={{
                    background: 'rgba(255,255,255,0.04)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    color: '#94a3b8', fontSize: '13px',
                    padding: '8px 14px', borderRadius: '20px',
                    cursor: 'pointer', transition: 'all 0.2s ease'
                  }}
                  onMouseEnter={e => {
                    e.currentTarget.style.background = 'rgba(245,158,11,0.1)';
                    e.currentTarget.style.borderColor = 'rgba(245,158,11,0.3)';
                    e.currentTarget.style.color = '#f59e0b';
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.04)';
                    e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)';
                    e.currentTarget.style.color = '#94a3b8';
                  }}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="glass" style={{ flex: 1, borderRadius: '20px', padding: '16px', marginBottom: '16px', overflowY: 'auto', maxHeight: '500px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  display: 'flex', gap: '10px',
                  flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
                }}
              >
                {/* Avatar */}
                <div style={{
                  width: '32px', height: '32px', borderRadius: '50%',
                  background: msg.role === 'user'
                    ? 'linear-gradient(135deg, #f59e0b, #d97706)'
                    : 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  flexShrink: 0
                }}>
                  {msg.role === 'user'
                    ? <FiUser style={{ color: '#0a0a0f', fontSize: '14px' }} />
                    : <MdSmartToy style={{ color: 'white', fontSize: '14px' }} />
                  }
                </div>

                {/* Bubble */}
                <div style={{
                  maxWidth: '75%', padding: '12px 16px', fontSize: '14px', lineHeight: 1.6,
                  borderRadius: msg.role === 'user' ? '18px 4px 18px 18px' : '4px 18px 18px 18px',
                  background: msg.role === 'user'
                    ? 'linear-gradient(135deg, #f59e0b, #d97706)'
                    : 'rgba(255,255,255,0.06)',
                  color: msg.role === 'user' ? '#0a0a0f' : '#cbd5e1',
                  border: msg.role === 'user' ? 'none' : '1px solid rgba(255,255,255,0.08)',
                  whiteSpace: 'pre-wrap'
                }}>
                  {msg.content}
                </div>
              </div>
            ))}

            {/* Typing indicator */}
            {loading && (
              <div style={{ display: 'flex', gap: '10px' }}>
                <div style={{
                  width: '32px', height: '32px', borderRadius: '50%',
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                  <MdSmartToy style={{ color: 'white', fontSize: '14px' }} />
                </div>
                <div style={{
                  background: 'rgba(255,255,255,0.06)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  padding: '12px 16px', borderRadius: '4px 18px 18px 18px',
                  display: 'flex', gap: '4px', alignItems: 'center'
                }}>
                  {[0, 1, 2].map(i => (
                    <span key={i} style={{
                      width: '8px', height: '8px', borderRadius: '50%',
                      background: '#475569', display: 'inline-block',
                      animation: 'bounce 1.4s infinite',
                      animationDelay: `${i * 150}ms`
                    }} />
                  ))}
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <div style={{ display: 'flex', gap: '12px' }}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask SmartBot anything... (Press Enter to send)"
            rows={1}
            className="input-dark"
            style={{
              flex: 1, borderRadius: '14px',
              padding: '14px 18px', fontSize: '14px',
              resize: 'none', fontFamily: 'inherit'
            }}
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            className="btn-gold"
            style={{
              padding: '14px 20px', borderRadius: '14px',
              border: 'none', cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              display: 'flex', alignItems: 'center', gap: '8px',
              opacity: loading || !input.trim() ? 0.5 : 1
            }}
          >
            <FiSend />
          </button>
        </div>
        <p style={{ textAlign: 'center', color: '#334155', fontSize: '12px', marginTop: '8px' }}>
          Powered by Groq AI • Press Enter to send, Shift+Enter for new line
        </p>

        <style>{`
          @keyframes bounce {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-6px); }
          }
        `}</style>
      </div>
    </div>
  );
};

export default Chatbot;