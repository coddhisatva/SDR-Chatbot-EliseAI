/**
 * Individual chat message component
 * Renders user or assistant messages with appropriate styling
 */

import { Message } from '../types';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  const messageClass = isUser
    ? 'ml-auto bg-blue-600 text-white p-4 rounded-2xl max-w-[80%] shadow-sm'
    : 'bg-white p-4 rounded-2xl max-w-[80%] shadow-sm border border-gray-200';

  return (
    <div className={messageClass}>
      <div className="whitespace-pre-wrap break-words">{message.content}</div>
      {message.timestamp && (
        <div className={`text-xs mt-2 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
          {new Date(message.timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      )}
    </div>
  );
}

