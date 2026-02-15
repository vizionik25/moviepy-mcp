'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { chatCompletion, callTool, ChatMessage } from '@/lib/api';
import ReactMarkdown from 'react-markdown';

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: 'Hello! I am your MoviePy AI assistant. How can I help you with your video today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Load settings from localStorage
      const savedSettings = localStorage.getItem('moviepy-mcp-settings');
      let config = {
        model: 'gpt-4o',
        apiBase: 'http://localhost:1234/v1',
        apiKey: ''
      };

      if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        config = {
          model: settings.modelName || 'gpt-4o',
          apiBase: settings.apiBaseUrl || 'http://localhost:1234/v1',
          apiKey: settings.apiKey || ''
        };
      }

      // 1. Get AI response (including potential tool calls)
      const response = await chatCompletion({
        messages: [...messages, userMessage],
        model: config.model,
        api_base: config.apiBase,
        api_key: config.apiKey,
      });

      const assistantMessage: ChatMessage = { role: 'assistant', content: response.content };
      setMessages(prev => [...prev, assistantMessage]);

      // Check for tool call keywords in AI response (very basic demo logic)
      if (response.content.toLowerCase().includes('generate a video')) {
        // Mocking a tool call for the demo
      }

    } catch (error: any) {
      console.error("Chat error:", error);
      const errorMessage = error.response?.status === 401 
        ? "Unauthorized: Please check your API Key in Settings." 
        : error.message;
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${errorMessage}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-slate-900 rounded-lg overflow-hidden border border-slate-700 shadow-xl">
      {/* Header */}
      <div className="p-4 bg-slate-800 border-b border-slate-700 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Bot className="text-blue-400" />
          <h2 className="font-semibold text-slate-100">Video AI Assistant</h2>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg flex gap-3 ${
              m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-200 border border-slate-700'
            }`}>
              {m.role === 'assistant' ? <Bot size={20} className="shrink-0 mt-1" /> : <User size={20} className="shrink-0 mt-1" />}
              <div className="prose prose-invert text-sm prose-p:leading-relaxed">
                <ReactMarkdown>{m.content}</ReactMarkdown>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 text-slate-200 p-3 rounded-lg border border-slate-700 flex items-center gap-2">
              <Loader2 className="animate-spin" size={20} />
              <span className="text-sm">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-slate-800 border-t border-slate-700">
        <div className="flex gap-2">
          <input
            type="text"
            className="flex-1 bg-slate-700 text-slate-100 px-4 py-2 rounded-lg border border-slate-600 outline-none focus:border-blue-500 transition-colors"
            placeholder="Describe the video you want to create or edit..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <button
            onClick={handleSend}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 text-white p-2 rounded-lg transition-colors"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
