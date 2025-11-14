/**
 * Typing indicator component
 * Shows animated dots when AI is thinking
 */

export default function TypingIndicator() {
  return (
    <div className="bg-white p-4 rounded-2xl max-w-[80%] flex items-center gap-2 shadow-sm border border-gray-200">
      <div className="text-gray-600 text-sm font-medium">Alex is typing</div>
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
    </div>
  );
}

