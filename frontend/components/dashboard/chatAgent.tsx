"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const ChatAgent = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error("Error fetching data:", error);
      setAnswer("❌ Failed to connect to the backend server. Please check if FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  // Allows pressing "Enter" to search
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="w-full max-w-3xl flex flex-col gap-6">
      <div className="relative group">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask AI a question about your data..."
          className="w-full p-5 bg-slate-900 border-2 border-slate-700 rounded-2xl text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-all shadow-2xl"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="absolute right-3 top-3 bottom-3 px-6 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 text-white font-bold rounded-xl transition-colors"
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>

    
      {answer && (
        <div className={`mt-4 p-6 rounded-2xl shadow-xl border animate-in fade-in slide-in-from-bottom-4 duration-500 ${
          answer.toLowerCase().includes("not allowed") 
            ? "bg-red-950/30 border-red-500/50" 
            : "bg-slate-900/80 border-blue-500/30"
        }`}>
          <h2 className={`text-xs uppercase tracking-widest font-bold mb-4 ${
            answer.toLowerCase().includes("not allowed") ? "text-red-400" : "text-blue-400"
          }`}>
            {answer.toLowerCase().includes("not allowed") ? "⚠️ Security Guardrail" : "⚓ AI Response"}
          </h2>
          
          <div className="text-lg leading-relaxed text-slate-200 prose prose-invert max-w-none">
            <ReactMarkdown>
              {answer}
            </ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatAgent;