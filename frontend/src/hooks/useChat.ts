/**
 * Main chat hook - manages conversation state and API interactions
 */

import { useState, useEffect, useCallback } from 'react';
import { Message, QuickReply, Source } from '../types';
import { getOrCreateSessionId } from '../utils/session';
import { initChat, sendChatMessage } from '../services/api';

const MESSAGES_KEY = 'eliseai_messages';

interface UseChatReturn {
  messages: Message[];
  loading: boolean;
  error: string | null;
  quickReplies: QuickReply[] | null;
  calendlyUrl: string | null;
  sendMessage: (content: string) => Promise<void>;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [quickReplies, setQuickReplies] = useState<QuickReply[] | null>(null);
  const [calendlyUrl, setCalendlyUrl] = useState<string | null>(null);
  const [sessionId] = useState(() => getOrCreateSessionId());
  const [initialized, setInitialized] = useState(false);

  // Load messages from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(MESSAGES_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setMessages(parsed);
        setInitialized(true);
      } catch (e) {
        console.error('Failed to parse saved messages:', e);
      }
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(MESSAGES_KEY, JSON.stringify(messages));
    }
  }, [messages]);

  // Initialize chat with greeting if no messages
  useEffect(() => {
    if (!initialized && messages.length === 0) {
      setInitialized(true);
      setLoading(true);
      
      initChat(sessionId)
        .then((response) => {
          const greeting: Message = {
            role: 'assistant',
            content: response.response,
            timestamp: new Date(),
          };
          setMessages([greeting]);
          setQuickReplies(response.quick_replies || null);
        })
        .catch((err) => {
          setError('Failed to initialize chat. Please refresh the page.');
          console.error('Init error:', err);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [initialized, messages.length, sessionId]);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;
    
    // Allow sending messages even while loading (queue them)

    // Clear quick replies and calendly when user sends new message
    setQuickReplies(null);
    setCalendlyUrl(null);
    setError(null);

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      // Send to backend
      const response = await sendChatMessage(updatedMessages, sessionId);

      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages([...updatedMessages, assistantMessage]);
      
      // Update quick replies if provided
      if (response.quick_replies) {
        setQuickReplies(response.quick_replies);
      }

      // Update calendly URL if demo was booked
      if (response.calendly_url) {
        setCalendlyUrl(response.calendly_url);
      }

    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Send error:', err);
      
      // Remove the user message on error
      setMessages(messages);
    } finally {
      setLoading(false);
    }
  }, [messages, loading, sessionId]);

  return {
    messages,
    loading,
    error,
    quickReplies,
    calendlyUrl,
    sendMessage,
  };
}

