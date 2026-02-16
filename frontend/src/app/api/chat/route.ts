import { NextResponse } from 'next/server';
import axios from 'axios';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { messages, model, temperature, api_key, api_base } = body;

    const apiKey = api_key || process.env.LLM_API_KEY;
    const apiBase = api_base || process.env.LLM_API_BASE || 'https://api.openai.com/v1';
    const targetModel = model || process.env.LLM_MODEL || 'gpt-4o';

    if (!apiKey) {
      return NextResponse.json(
        { error: 'LLM API key is not configured. Please add it in the settings tab or configure it on the server.' },
        { status: 400 }
      );
    }

    // Normalize baseURL
    let baseURL = apiBase;
    if (baseURL.endsWith('/')) {
      baseURL = baseURL.slice(0, -1);
    }

    const response = await axios.post(`${baseURL}/chat/completions`, {
      model: targetModel,
      messages: messages,
      temperature: temperature || 0.7,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      }
    });

    return NextResponse.json({
      content: response.data.choices[0].message.content,
      model: response.data.model
    });

  } catch (error: any) {
    console.error('API Route Error:', error.response?.data || error.message);
    return NextResponse.json(
      { error: error.response?.data?.error?.message || error.message },
      { status: error.response?.status || 500 }
    );
  }
}
