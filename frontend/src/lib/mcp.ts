import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { LoggingMessageNotificationSchema, CreateMessageRequestSchema } from "@modelcontextprotocol/sdk/types.js";

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

let mcpClientPromise: Promise<Client> | null = null;
let mcpClient: Client | null = null;

/**
 * Initializes and returns the MCP client singleton using a promise to handle concurrent calls.
 * Uses SSE transport, connecting via the Next.js proxy (/sse).
 */
export function getMcpClient(): Promise<Client> {
  if (mcpClientPromise) {
    return mcpClientPromise;
  }

  mcpClientPromise = (async () => {
    try {
      console.log("Initializing MCP Client...");
      
      const client = new Client(
        {
          name: "moviepy-mcp-frontend",
          version: "1.0.0",
        },
        {
          capabilities: {
            sampling: {},
          },
        }
      );

      // Set up notification handlers
      client.setNotificationHandler(LoggingMessageNotificationSchema, (notification) => {
        const { level, data } = notification.params;
        console.log(`[MCP ${level}]`, data);
      });

      // Handle server-initiated requests if any (e.g. sampling)
      client.setRequestHandler(CreateMessageRequestSchema, async (request) => {
        console.log("Sampling request received from MCP server:", request);
        // This could be integrated with the chat UI in a more complex setup
        return {
          model: "gpt-4o",
          role: "assistant",
          content: {
            type: "text",
            text: "Sampling response from frontend",
          },
        };
      });

      // Connect using Streamable HTTP transport
      // The /mcp endpoint is proxied by Next.js to http://localhost:8000/mcp
      const mcpUrl = new URL("/mcp", typeof window !== "undefined" ? window.location.origin : "http://localhost:3000");
      const transport = new StreamableHTTPClientTransport(mcpUrl);
      
      await client.connect(transport);
      console.log("MCP Client connected successfully via Streamable HTTP");
      
      mcpClient = client;
      return client;
    } catch (error) {
      console.error("Failed to connect to MCP server:", error);
      mcpClientPromise = null; // Reset promise so we can retry
      throw error;
    }
  })();

  return mcpClientPromise;
}

/**
 * Lists all tools available on the MCP server.
 */
export async function listMcpTools() {
  const client = await getMcpClient();
  const { tools } = await client.listTools();
  return tools;
}

/**
 * Calls an MCP tool by name with the provided arguments.
 */
export async function callMcpTool(name: string, args: any) {
  const client = await getMcpClient();
  const result = await client.callTool({
    name,
    arguments: args,
  });
  return result;
}

/**
 * Cleanup function to disconnect the client if needed.
 */
export async function disconnectMcp() {
  if (mcpClient) {
    // Note: The SDK Client might not have a direct disconnect method that is public
    // but the transport can be closed.
    mcpClientPromise = null;
    mcpClient = null;
  }
}
