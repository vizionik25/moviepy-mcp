import axios from 'axios';

// Since the frontend only talks to its own backend (Next.js API routes),
// we use relative paths for all MCP operations and chat.

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
  try {
    const apiBase = request.api_base || process.env.LLM_API_BASE || 'https://api.openai.com/v1';
    const apiKey = request.api_key || process.env.LLM_API_KEY;

    if (!apiKey) {
      throw new Error('LLM API key is not configured. Please add it in the settings tab.');
    }

    // Normalize baseURL
    let baseURL = apiBase;
    if (baseURL.endsWith('/')) {
      baseURL = baseURL.slice(0, -1);
    }

    const response = await axios.post(`${baseURL}/chat/completions`, {
      model: request.model,
      messages: request.messages,
      temperature: request.temperature || 0.7,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      }
    });
    
    return {
      content: response.data.choices[0].message.content,
      model: response.data.model
    };
  } catch (error: any) {
    console.error("LLM Connection Error:", error);
    const detail = error.response?.data?.error?.message || error.message;
    throw new Error(`LLM Error: ${detail}`);
  }
};

// All MCP tool discovery and execution goes through the Next.js API route proxy
export const listTools = async () => {
  const response = await axios.get('/api/mcp/tools');
  return response.data;
};

export const callTool = async (toolName: string, args: any) => {
  const response = await axios.post('/api/mcp/call', {
    name: toolName,
    arguments: args,
  });
  return response.data;
};

export default axios.create({ baseURL: '/' });
