/**
 * Chat input component
 * Multi-line textarea with send button
 * Supports Shift+Enter for new lines
 * Always enabled - can type even while AI is responding
 */

import { useState, FormEvent, KeyboardEvent, useRef, useEffect } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  onClear?: () => void;
  showClear?: boolean;
  clearConfirm?: boolean;
}

export default function ChatInput({ onSend, disabled, onClear, showClear, clearConfirm }: ChatInputProps) {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput('');
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Enter = send, Shift+Enter = new line
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="p-4 bg-white border-t" onSubmit={handleSubmit}>
      <div className="flex gap-2 items-end">
        {showClear && onClear && (
          <button
            type="button"
            onClick={onClear}
            className={`px-3 py-3 rounded-lg transition-colors font-medium text-sm whitespace-nowrap ${
              clearConfirm
                ? 'bg-red-500 text-white hover:bg-red-600'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
            title="Clear chat"
          >
            {clearConfirm ? '⚠️' : '🗑️'}
          </button>
        )}
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message... (Shift+Enter for new line)"
          rows={1}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none max-h-32 overflow-y-auto"
        />
        <button 
          type="submit" 
          disabled={!input.trim()}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium whitespace-nowrap"
        >
          Send
        </button>
      </div>
      {disabled && (
        <div className="text-xs text-gray-500 mt-1 text-center">
          AI is responding... (You can still type and queue your next message)
        </div>
      )}
    </form>
  );
}

