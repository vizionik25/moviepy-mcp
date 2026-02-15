import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// API instance for MoviePy backend tools
const api = axios.create({
  baseURL: API_BASE_URL,
});

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatRequest {
  messages: ChatMessage[];
  model: string;
  api_base?: string;
  api_key?: string;
  temperature?: number;
}

export const chatCompletion = async (request: ChatRequest) => {
  // Use the provided api_base (e.g., LM Studio, Ollama, OpenAI)
  let baseURL = request.api_base || 'https://api.openai.com/v1';
  
  // Normalize baseURL by removing trailing slash
  if (baseURL.endsWith('/')) {
    baseURL = baseURL.slice(0, -1);
  }
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  };
  
  if (request.api_key) {
    headers['Authorization'] = `Bearer ${request.api_key}`;
  }

  // The user specified /chat/completions and /responses as the required endpoints
  // We'll try /chat/completions first as it's the standard OpenAI path
  try {
    const response = await axios.post(`${baseURL}/chat/completions`, {
      model: request.model,
      messages: request.messages,
      temperature: request.temperature || 0.7,
    }, { headers });
    
    return {
      content: response.data.choices[0].message.content,
      model: response.data.model
    };
  } catch (error: any) {
    // If /chat/completions fails, try the /responses endpoint mentioned by the user
    // This format is used by some local LLM servers as shown in the user's example
    try {
      const systemMessage = request.messages.find(m => m.role === 'system')?.content || '';
      const lastUserMessage = request.messages.filter(m => m.role === 'user').pop()?.content || '';

      const response = await axios.post(`${baseURL}/responses`, {
        model: request.model,
        system_prompt: systemMessage,
        input: lastUserMessage,
      }, { headers });
      
      return {
        content: response.data.content || response.data.choices?.[0]?.message?.content || response.data.text || response.data.response,
        model: response.data.model
      };
    } catch (innerError: any) {
      console.error("Failed to call external LLM:", innerError);
      // Prefer throwing the error that might be more specific to the local server
      if (innerError.response?.status === 401) {
        throw innerError;
      }
      throw error; // Throw the original error if fallback also failed generically
    }
  }
};

export const listTools = async () => {
  return [
    { name: 'generate_video', description: 'Generates a simple video with text' },
    { name: 'cut_video', description: 'Cuts a video' },
    { name: 'concatenate_videos', description: 'Concatenates videos' },
    { name: 'resize_video', description: 'Resizes a video' },
    { name: 'speed_video', description: 'Changes video speed' },
    { name: 'volume_video', description: 'Changes video volume' },
    { name: 'extract_audio', description: 'Extracts audio' },
    { name: 'text_overlay', description: 'Overlays text' },
    { name: 'image_overlay', description: 'Overlays an image' },
    { name: 'color_effect', description: 'Applies color effects' },
    { name: 'detect_scenes', description: 'Detects scenes' },
    { name: 'save_frame', description: 'Saves a frame' },
    { name: 'write_gif', description: 'Writes a GIF' },
  ];
};

export const callTool = async (toolName: string, args: any) => {
  const mapping: Record<string, string> = {
    'generate_video': '/video/generate',
    'cut_video': '/video-edits/cut',
    'concatenate_videos': '/video-edits/concatenate',
    'resize_video': '/video-edits/resize',
    'speed_video': '/video-edits/speed',
    'volume_video': '/audio/volume',
    'extract_audio': '/audio/extract',
    'text_overlay': '/compositing/text-overlay',
    'image_overlay': '/compositing/image-overlay',
    'color_effect': '/video-edits/color-effect',
    'detect_scenes': '/video-edits/detect-scenes',
    'save_frame': '/video/save-frame',
    'write_gif': '/video/write-gif',
  };

  const endpoint = mapping[toolName];
  if (!endpoint) throw new Error(`Unknown tool: ${toolName}`);

  const response = await api.post(endpoint, args);
  return response.data;
};

export default api;
