import { useState, useEffect, useRef } from 'react';
import { MdSmartToy, MdClose, MdSend } from 'react-icons/md';
import { FiUser } from 'react-icons/fi';
import api from '../services/api';

const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm SmartBot 🤖 Your AI learning assistant powered by Groq AI. Ask me anything!"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Don't show if not logged in
  if (!isLoggedIn) return null;

  const sendMessage = async (text) => {
    const messageText = text || input.trim();
    if (!messageText || loading) return;

    const userMessage = { role: 'user', content: messageText };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/chatbot/chat', {
        message: messageText,
        history: messages.slice(1).slice(-10)
      });
      setMessages([
        ...newMessages,
        { role: 'assistant', content: res.data.response }
      ]);
    } catch {
      setMessages([
        ...newMessages,
        { role: 'assistant', content: "Sorry, I'm having trouble right now. Please try again! 🔄" }
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

  const quickQuestions = [
    "Study tips? 📚",
    "Quiz help? 📝",
    "Motivate me! 💪"
  ];

  return (
    <>
      {/* Chat Window */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '24px',
            width: '360px',
            height: '500px',
            zIndex: 9999,
            display: 'flex',
            flexDirection: 'column',
            borderRadius: '20px',
            overflow: 'hidden',
            boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
            border: '1px solid #e2e8f0'
          }}
        >
          {/* Header */}
          <div style={{
            background: 'linear-gradient(135deg, #3b82f6, #6366f1)',
            padding: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{
                background: 'rgba(255,255,255,0.2)',
                borderRadius: '50%',
                padding: '6px',
                display: 'flex'
              }}>
                <MdSmartToy style={{ color: 'white', fontSize: '20px' }} />
              </div>
              <div>
                <p style={{ color: 'white', fontWeight: '700', fontSize: '15px', margin: 0 }}>
                  SmartBot
                </p>
                <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '11px', margin: 0 }}>
                  ● Powered by Groq AI
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              style={{
                background: 'rgba(255,255,255,0.2)',
                border: 'none',
                borderRadius: '50%',
                padding: '6px',
                cursor: 'pointer',
                display: 'flex',
                color: 'white'
              }}
            >
              <MdClose style={{ fontSize: '18px' }} />
            </button>
          </div>

          {/* Messages */}
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '16px',
            background: '#f8fafc',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px'
          }}>
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  display: 'flex',
                  gap: '8px',
                  flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
                }}
              >
                {/* Avatar */}
                <div style={{
                  width: '30px',
                  height: '30px',
                  borderRadius: '50%',
                  background: msg.role === 'user'
                    ? 'linear-gradient(135deg, #3b82f6, #6366f1)'
                    : 'linear-gradient(135deg, #10b981, #059669)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  {msg.role === 'user'
                    ? <FiUser style={{ color: 'white', fontSize: '14px' }} />
                    : <MdSmartToy style={{ color: 'white', fontSize: '14px' }} />
                  }
                </div>

                {/* Bubble */}
                <div style={{
                  maxWidth: '75%',
                  padding: '10px 14px',
                  borderRadius: msg.role === 'user'
                    ? '18px 4px 18px 18px'
                    : '4px 18px 18px 18px',
                  background: msg.role === 'user'
                    ? 'linear-gradient(135deg, #3b82f6, #6366f1)'
                    : 'white',
                  color: msg.role === 'user' ? 'white' : '#1e293b',
                  fontSize: '13px',
                  lineHeight: '1.5',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                  whiteSpace: 'pre-wrap'
                }}>
                  {msg.content}
                </div>
              </div>
            ))}

            {/* Typing Indicator */}
            {loading && (
              <div style={{ display: 'flex', gap: '8px' }}>
                <div style={{
                  width: '30px', height: '30px', borderRadius: '50%',
                  background: 'linear-gradient(135deg, #10b981, #059669)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                  <MdSmartToy style={{ color: 'white', fontSize: '14px' }} />
                </div>
                <div style={{
                  background: 'white', padding: '12px 16px',
                  borderRadius: '4px 18px 18px 18px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                  display: 'flex', gap: '4px', alignItems: 'center'
                }}>
                  {[0, 1, 2].map(i => (
                    <div key={i} style={{
                      width: '8px', height: '8px',
                      borderRadius: '50%', background: '#94a3b8',
                      animation: 'bounce 1.4s infinite',
                      animationDelay: `${i * 0.2}s`
                    }} />
                  ))}
                </div>
              </div>
            )}

            {/* Quick Questions */}
            {messages.length === 1 && !loading && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '4px' }}>
                {quickQuestions.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(q)}
                    style={{
                      background: 'white',
                      border: '1px solid #e2e8f0',
                      borderRadius: '20px',
                      padding: '6px 12px',
                      fontSize: '12px',
                      cursor: 'pointer',
                      color: '#3b82f6',
                      fontWeight: '500'
                    }}
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div style={{
            background: 'white',
            padding: '12px',
            borderTop: '1px solid #e2e8f0',
            display: 'flex',
            gap: '8px'
          }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask SmartBot anything..."
              style={{
                flex: 1,
                border: '1px solid #e2e8f0',
                borderRadius: '20px',
                padding: '8px 14px',
                fontSize: '13px',
                outline: 'none',
                fontFamily: 'inherit'
              }}
            />
            <button
              onClick={() => sendMessage()}
              disabled={loading || !input.trim()}
              style={{
                background: loading || !input.trim()
                  ? '#cbd5e1'
                  : 'linear-gradient(135deg, #3b82f6, #6366f1)',
                border: 'none',
                borderRadius: '50%',
                width: '36px',
                height: '36px',
                cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0
              }}
            >
              <MdSend style={{ color: 'white', fontSize: '16px' }} />
            </button>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: isOpen
            ? '#ef4444'
            : 'linear-gradient(135deg, #3b82f6, #6366f1)',
          border: 'none',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 8px 25px rgba(59,130,246,0.5)',
          zIndex: 9999,
          transition: 'all 0.3s ease',
          transform: isOpen ? 'rotate(0deg)' : 'rotate(0deg)'
        }}
      >
        {isOpen
          ? <MdClose style={{ color: 'white', fontSize: '28px' }} />
          : <MdSmartToy style={{ color: 'white', fontSize: '28px' }} />
        }

        {/* Pulse animation when closed */}
        {!isOpen && (
          <span style={{
            position: 'absolute',
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            background: 'rgba(59,130,246,0.4)',
            animation: 'ping 2s infinite'
          }} />
        )}
      </button>

      {/* CSS Animations */}
      <style>{`
        @keyframes ping {
          0% { transform: scale(1); opacity: 0.8; }
          100% { transform: scale(1.8); opacity: 0; }
        }
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-6px); }
        }
      `}</style>
    </>
  );
};

export default FloatingChatbot;