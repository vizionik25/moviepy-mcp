'use client';

import React, { useState } from 'react';
import Chat from '@/components/Chat';
import ToolsPanel from '@/components/ToolsPanel';
import Settings from '@/components/Settings';
import { Film, Clapperboard, MessageSquare, Settings as SettingsIcon } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'settings'>('chat');

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Clapperboard size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                VideoEditor-MCP Dashboard
              </h1>
              <p className="text-slate-500 text-sm">AI-Powered Video Automation Engine</p>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <nav className="flex items-center bg-slate-900 border border-slate-800 p-1 rounded-xl">
              <button
                onClick={() => setActiveTab('chat')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  activeTab === 'chat'
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <MessageSquare size={18} />
                <span className="font-medium">Chat</span>
              </button>
              <button
                onClick={() => setActiveTab('settings')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  activeTab === 'settings'
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <SettingsIcon size={18} />
                <span className="font-medium">Settings</span>
              </button>
            </nav>
            <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-full">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-[10px] text-green-500 font-bold uppercase tracking-wider">Server Connected</span>
            </div>
          </div>
        </header>

        {activeTab === 'chat' ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-in fade-in duration-500">
            <div className="lg:col-span-2">
              <Chat />
            </div>
            <div className="space-y-8">
              <ToolsPanel />
              <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-lg p-6 shadow-xl relative overflow-hidden group">
                <Film className="absolute -right-4 -bottom-4 text-white/10 w-32 h-32 rotate-12 group-hover:rotate-0 transition-transform duration-500" />
                <h3 className="text-white font-bold mb-2 relative z-10">MoviePy v2.2.1</h3>
                <p className="text-blue-100 text-sm relative z-10 leading-relaxed">
                  Experience the rewritten MoviePy library with enhanced effects, better performance, and full FastAPI integration.
                </p>
                <button className="mt-4 bg-white/20 hover:bg-white/30 text-white text-xs font-bold py-2 px-4 rounded-full transition-colors relative z-10">
                  View Documentation
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <Settings />
          </div>
        )}
      </div>
    </main>
  );
}
