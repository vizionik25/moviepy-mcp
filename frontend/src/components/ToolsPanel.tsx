'use client';

import React, { useState } from 'react';
import { Video, Scissors, Layers, Volume2, Type, Image as ImageIcon, Wand2, RefreshCw, Save, Film, Settings } from 'lucide-react';
import { callTool } from '@/lib/api';

const tools = [
  { id: 'generate_video', name: 'Generate', icon: Video, color: 'text-green-400', args: { text: 'Hello MoviePy', duration: 3.0 } },
  { id: 'cut_video', name: 'Cut', icon: Scissors, color: 'text-red-400', args: { video_path: '', start_time: 0, end_time: 5 } },
  { id: 'text_overlay', name: 'Text Overlay', icon: Type, color: 'text-blue-400', args: { video_path: '', text: 'Overlay Text', position: 'center' } },
  { id: 'concatenate_videos', name: 'Concat', icon: Layers, color: 'text-purple-400', args: { video_paths: [] } },
  { id: 'color_effect', name: 'Effect', icon: Wand2, color: 'text-yellow-400', args: { video_path: '', effect_type: 'blackwhite' } },
  { id: 'write_gif', name: 'GIF', icon: Film, color: 'text-orange-400', args: { video_path: '' } },
];

export default function ToolsPanel() {
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState<string | null>(null);

  const handleToolCall = async (tool: any) => {
    setLoading(tool.id);
    try {
      const res = await callTool(tool.id, tool.args);
      setResults(prev => [res, ...prev]);
    } catch (error: any) {
      alert(`Error calling ${tool.id}: ${error.message}`);
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 p-4 shadow-xl">
      <h3 className="text-slate-100 font-semibold mb-4 flex items-center gap-2">
        <Settings size={18} /> Tools Quick Actions
      </h3>
      
      <div className="grid grid-cols-2 gap-2 mb-6">
        {tools.map(t => (
          <button
            key={t.id}
            onClick={() => handleToolCall(t)}
            disabled={loading !== null}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 p-2 rounded border border-slate-700 text-left transition-colors group"
          >
            <t.icon size={16} className={t.color} />
            <span className="text-xs text-slate-300 group-hover:text-slate-100">{t.name}</span>
            {loading === t.id && <RefreshCw size={12} className="animate-spin ml-auto text-slate-500" />}
          </button>
        ))}
      </div>

      <h4 className="text-slate-400 text-xs font-bold uppercase mb-2 tracking-wider">Results</h4>
      <div className="space-y-2 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
        {results.length === 0 && <div className="text-slate-600 text-xs italic">No actions performed yet.</div>}
        {results.map((r, i) => (
          <div key={i} className="bg-slate-800 p-2 rounded border border-slate-700 text-[10px] font-mono break-all text-slate-400">
            <div className="text-green-500 mb-1 font-bold">{r.status}</div>
            {r.output_path || r.file_path || JSON.stringify(r.data)}
          </div>
        ))}
      </div>
    </div>
  );
}
