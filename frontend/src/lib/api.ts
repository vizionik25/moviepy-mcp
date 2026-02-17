import axios from 'axios';
import { listMcpTools, callMcpTool, ChatMessage } from './mcp';

// Since the frontend only talks to its own backend (Next.js API routes),
// we use relative paths for all MCP operations and chat.

export interface ChatRequest {
  messages: ChatMessage[];
  model: string;
  api_base?: string;
  api_key?: string;
  temperature?: number;
}

/**
 * Proxy chat completions through the Next.js API route to avoid CORS issues
 * and keep API keys secure.
 */
export const chatCompletion = async (request: ChatRequest) => {
  try {
    const response = await axios.post('/api/chat', {
      model: request.model,
      messages: request.messages,
      temperature: request.temperature || 0.7,
      api_key: request.api_key,
      api_base: request.api_base,
    });
    
    return {
      content: response.data.content,
      model: response.data.model
    };
  } catch (error: any) {
    console.error("LLM Connection Error:", error);
    const detail = error.response?.data?.error || error.message;
    throw new Error(`LLM Error: ${detail}`);
  }
};

/**
 * All MCP tool discovery and execution now uses the proper MCP SDK implementation
 */
export const listTools = async () => {
  return await listMcpTools();
};

export const callTool = async (toolName: string, args: any) => {
  return await callMcpTool(toolName, args);
};

export default axios.create({ baseURL: '/' });
export type { ChatMessage };
