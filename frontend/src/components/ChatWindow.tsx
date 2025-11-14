/**
 * Main chat window component
 * Orchestrates all chat UI elements
 */

import { useEffect, useRef, useState } from 'react';
import { useChat } from '../hooks/useChat';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import QuickReplies from './QuickReplies';
import TypingIndicator from './TypingIndicator';
import CalendlyButton from './CalendlyButton';
import ErrorMessage from './ErrorMessage';
import { clearMessages } from '../utils/clearChat';

export default function ChatWindow() {
  const { messages, loading, error, quickReplies, calendlyUrl, sendMessage } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [showClearConfirm, setShowClearConfirm] = useState(false);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleQuickReply = (value: string) => {
    sendMessage(value);
  };

  const handleClearChat = () => {
    if (showClearConfirm) {
      clearMessages();
      window.location.reload();
    } else {
      setShowClearConfirm(true);
      setTimeout(() => setShowClearConfirm(false), 3000);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="p-4 bg-blue-600 text-white shadow-md">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold">EliseAI SDR Assistant</h1>
            <p className="text-sm text-blue-100">Powered by AI • Always here to help</p>
          </div>
          <a
            href="https://calendly.com/eliseai-demo/30min"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-white text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-50 transition-colors font-medium text-sm"
          >
            📅 Book a Demo
          </a>
        </div>
      </header>
      
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {/* Error message */}
          {error && <ErrorMessage message={error} />}

          {/* Messages */}
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}

          {/* Loading indicator */}
          {loading && <TypingIndicator />}

          {/* Calendly button if demo was booked */}
          {calendlyUrl && <CalendlyButton url={calendlyUrl} />}

          {/* Quick replies */}
          {quickReplies && !loading && (
            <QuickReplies 
              replies={quickReplies} 
              onSelect={handleQuickReply}
              disabled={loading}
            />
          )}

          {/* Scroll anchor */}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input area - always enabled, can type while AI responds */}
      <ChatInput 
        onSend={sendMessage} 
        disabled={false}
        onClear={handleClearChat}
        showClear={messages.length > 0}
        clearConfirm={showClearConfirm}
      />
    </div>
  );
}

