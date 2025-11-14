/**
 * Quick reply buttons component
 * Shows product selection buttons or other quick actions
 */

import { QuickReply } from '../types';

interface QuickRepliesProps {
  replies: QuickReply[];
  onSelect: (value: string) => void;
  disabled?: boolean;
}

export default function QuickReplies({ replies, onSelect, disabled }: QuickRepliesProps) {
  return (
    <div className="flex flex-wrap gap-2 mb-4">
      {replies.map((reply, index) => (
        <button
          key={index}
          onClick={() => onSelect(reply.value)}
          disabled={disabled}
          className="px-4 py-2 bg-white border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
        >
          {reply.label}
        </button>
      ))}
    </div>
  );
}

