'use client';

import React, { useState, useEffect } from 'react';
import { Video, Scissors, Layers, Volume2, Type, Image as ImageIcon, Wand2, RefreshCw, Save, Film, Settings, Box } from 'lucide-react';
import { listTools, callTool } from '@/lib/api';

export default function ToolsPanel() {
  const [tools, setTools] = useState<any[]>([]);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    async function loadTools() {
      try {
        const discoveredTools = await listTools();
        setTools(discoveredTools);
      } catch (error) {
        console.error("Failed to load tools from MCP server:", error);
      } finally {
        setIsInitializing(false);
      }
    }
    loadTools();
  }, []);

  const handleToolCall = async (tool: any) => {
    setLoading(tool.name);
    try {
      // For quick actions, we still need some default args or a way to prompt
      // For now, let's use some smart defaults based on tool name or just empty
      const args = tool.inputSchema?.properties ? {} : {};
      
      const res = await callTool(tool.name, args);
      setResults(prev => [{ status: 'success', name: tool.name, ...res }, ...prev]);
    } catch (error: any) {
      alert(`Error calling ${tool.name}: ${error.message}`);
    } finally {
      setLoading(null);
    }
  };

  const getIcon = (name: string) => {
    if (name.includes('video')) return <Video size={16} className="text-green-400" />;
    if (name.includes('audio')) return <Volume2 size={16} className="text-blue-400" />;
    if (name.includes('cut') || name.includes('crop')) return <Scissors size={16} className="text-red-400" />;
    if (name.includes('composite') || name.includes('concatenate')) return <Layers size={16} className="text-purple-400" />;
    if (name.includes('effect') || name.includes('kaleidoscope') || name.includes('dissolve')) return <Wand2 size={16} className="text-yellow-400" />;
    return <Box size={16} className="text-slate-400" />;
  };

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 p-4 shadow-xl">
      <h3 className="text-slate-100 font-semibold mb-4 flex items-center gap-2">
        <Settings size={18} /> MCP Tools Discovery
      </h3>
      
      {isInitializing ? (
        <div className="flex items-center gap-2 p-4 text-slate-500 text-sm">
          <RefreshCw size={16} className="animate-spin" />
          <span>Connecting to MCP server...</span>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-2 mb-6">
          {tools.map(t => (
            <button
              key={t.name}
              onClick={() => handleToolCall(t)}
              disabled={loading !== null}
              title={t.description}
              className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 p-2 rounded border border-slate-700 text-left transition-colors group"
            >
              {getIcon(t.name)}
              <span className="text-[10px] text-slate-300 group-hover:text-slate-100 truncate flex-1">{t.name}</span>
              {loading === t.name && <RefreshCw size={12} className="animate-spin ml-auto text-slate-500" />}
            </button>
          ))}
        </div>
      )}

      <h4 className="text-slate-400 text-xs font-bold uppercase mb-2 tracking-wider">Activity Log</h4>
      <div className="space-y-2 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
        {results.length === 0 && <div className="text-slate-600 text-xs italic">No actions performed yet.</div>}
        {results.map((r, i) => (
          <div key={i} className="bg-slate-800 p-2 rounded border border-slate-700 text-[10px] font-mono break-all text-slate-400">
            <div className="text-green-500 mb-1 font-bold">{r.name} - {r.status}</div>
            {r.output_path || r.file_path || (r.content && r.content[0]?.text) || JSON.stringify(r)}
          </div>
        ))}
      </div>
    </div>
  );
}
