/**
 * API service for backend communication
 * Centralized API calls with error handling
 */

import { Message, ChatResponse, InitChatResponse } from '../types';

const API_BASE = '/api';

/**
 * Initialize a new chat session
 */
export async function initChat(sessionId: string): Promise<InitChatResponse> {
  const response = await fetch(`${API_BASE}/chat/init`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error(`Failed to initialize chat: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Send a chat message and get AI response
 */
export async function sendChatMessage(
  messages: Message[],
  sessionId: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      messages: messages.map(m => ({
        role: m.role,
        content: m.content,
      })),
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`);
  }

  return response.json();
}

