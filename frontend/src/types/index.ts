/**
 * TypeScript type definitions for the chat application
 */

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: Date;
}

export interface QuickReply {
  label: string;
  value: string;
}

export interface Source {
  title: string;
  author: string;
  date: string;
}

export interface ChatResponse {
  response: string;
  quick_replies?: QuickReply[];
  sources?: Source[];
  tool_used?: string;
  calendly_url?: string;
}

export interface InitChatResponse {
  response: string;
  quick_replies?: QuickReply[];
  is_new_session: boolean;
}

