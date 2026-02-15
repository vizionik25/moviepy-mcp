'use client';

import React, { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Cpu, FolderOpen, Trash2, ChevronDown, ChevronUp, Save, CheckCircle } from 'lucide-react';

interface CollapsibleSectionProps {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({ title, icon, children, defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-slate-800 rounded-lg overflow-hidden mb-4 bg-slate-900/50">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 text-left hover:bg-slate-800/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="text-blue-400">{icon}</div>
          <span className="font-semibold text-slate-200">{title}</span>
        </div>
        {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
      </button>
      {isOpen && (
        <div className="p-4 border-t border-slate-800 space-y-4 animate-in fade-in slide-in-from-top-2 duration-200">
          {children}
        </div>
      )}
    </div>
  );
};

const Settings: React.FC = () => {
  const [llmProvider, setLlmProvider] = useState('OpenAI');
  const [modelName, setModelName] = useState('gpt-4o');
  const [apiBaseUrl, setApiBaseUrl] = useState('https://api.openai.com/v1');
  const [apiKey, setApiKey] = useState('');
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    // Load settings from localStorage
    const savedSettings = localStorage.getItem('moviepy-mcp-settings');
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      setLlmProvider(settings.llmProvider || 'OpenAI');
      setModelName(settings.modelName || 'gpt-4o');
      setApiBaseUrl(settings.apiBaseUrl || 'https://api.openai.com/v1');
      setApiKey(settings.apiKey || '');
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const settings = {
      llmProvider,
      modelName,
      apiBaseUrl,
      apiKey
    };
    localStorage.setItem('moviepy-mcp-settings', JSON.stringify(settings));
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  const handleReset = () => {
    setLlmProvider('OpenAI');
    setModelName('gpt-4o');
    setApiBaseUrl('https://api.openai.com/v1');
    setApiKey('');
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-4xl mx-auto py-6">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <SettingsIcon className="text-slate-400" size={24} />
          <h2 className="text-xl font-bold">Dashboard Settings</h2>
        </div>
        {isSaved && (
          <div className="flex items-center gap-2 text-green-400 bg-green-400/10 px-3 py-1 rounded-full animate-in fade-in zoom-in duration-300">
            <CheckCircle size={16} />
            <span className="text-sm font-medium">Settings Saved</span>
          </div>
        )}
      </div>

      <CollapsibleSection title="LLM Provider Configuration" icon={<Cpu size={20} />} defaultOpen={true}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-400">Model Provider</label>
            <select 
              value={llmProvider}
              onChange={(e) => setLlmProvider(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option>OpenAI</option>
              <option>Anthropic</option>
              <option>Google Gemini</option>
              <option>Ollama (Local)</option>
              <option>LM Studio (Local)</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-400">Model Name</label>
            <input 
              type="text" 
              placeholder="gpt-4o"
              value={modelName}
              onChange={(e) => setModelName(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </div>
          <div className="md:col-span-2 space-y-2">
            <label className="text-sm font-medium text-slate-400">API Base URL</label>
            <input 
              type="text" 
              placeholder="https://api.openai.com/v1"
              value={apiBaseUrl}
              onChange={(e) => setApiBaseUrl(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </div>
          <div className="md:col-span-2 space-y-2">
            <label className="text-sm font-medium text-slate-400">API Key</label>
            <input 
              type="password" 
              placeholder="sk-..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </div>
        </div>
      </CollapsibleSection>

      <CollapsibleSection title="File Management" icon={<FolderOpen size={20} />}>
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-400">Import Directory Path</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                defaultValue="/home/nik/moviepy-mcp/storage/imports"
                className="flex-1 bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" 
              />
              <button type="button" className="bg-slate-700 hover:bg-slate-600 px-3 py-2 rounded-md transition-colors">Browse</button>
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-400">Edited Files Subdirectory</label>
            <input 
              type="text" 
              defaultValue="outputs"
              className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500" 
            />
          </div>
        </div>
      </CollapsibleSection>

      <CollapsibleSection title="Cache & Memory Cleanup" icon={<Trash2 size={20} />}>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg">
            <div>
              <p className="font-medium text-slate-200">Auto-cleanup Cache</p>
              <p className="text-xs text-slate-500">Automatically delete temporary files after 24 hours</p>
            </div>
            <input type="checkbox" className="w-5 h-5 accent-blue-600" defaultChecked />
          </div>
          <div className="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg">
            <div>
              <p className="font-medium text-slate-200">Max Cache Size</p>
              <p className="text-xs text-slate-500">Limit total storage used by temporary files</p>
            </div>
            <select className="bg-slate-800 border border-slate-700 rounded-md px-2 py-1 text-slate-200 focus:outline-none">
              <option>1 GB</option>
              <option>5 GB</option>
              <option>10 GB</option>
              <option>Unlimited</option>
            </select>
          </div>
          <button type="button" className="w-full py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 border border-red-600/30 rounded-md transition-colors text-sm font-bold">
            Clear Cache Now
          </button>
        </div>
      </CollapsibleSection>

      <div className="mt-8 flex justify-end gap-3">
        <button 
          type="button" 
          onClick={handleReset}
          className="px-6 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors font-medium"
        >
          Reset
        </button>
        <button 
          type="submit" 
          className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors font-medium shadow-lg shadow-blue-900/20"
        >
          <Save size={18} />
          Save Changes
        </button>
      </div>
    </form>
  );
};

export default Settings;
