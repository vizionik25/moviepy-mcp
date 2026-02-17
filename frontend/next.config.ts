import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/mcp',
        destination: `${process.env.BACKEND_URL || 'http://localhost:8080'}/mcp`,
      },
      {
        source: '/sse',
        destination: `${process.env.BACKEND_URL || 'http://localhost:8000'}/sse`,
      },
      {
        source: '/messages',
        destination: `${process.env.BACKEND_URL || 'http://localhost:8000'}/messages`,
      },
    ];
  },
};

export default nextConfig;
