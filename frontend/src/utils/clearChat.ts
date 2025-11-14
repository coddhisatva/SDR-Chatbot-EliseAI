/**
 * Clear chat utilities
 * Functions to reset conversation and session
 */

const MESSAGES_KEY = 'eliseai_messages';
const SESSION_KEY = 'eliseai_session_id';

/**
 * Clear all chat messages from localStorage
 */
export function clearMessages(): void {
  localStorage.removeItem(MESSAGES_KEY);
}

/**
 * Clear entire session (messages + session ID)
 * Forces a fresh start with new session
 */
export function clearSession(): void {
  localStorage.removeItem(MESSAGES_KEY);
  localStorage.removeItem(SESSION_KEY);
}

/**
 * Check if there are any saved messages
 */
export function hasMessages(): boolean {
  const saved = localStorage.getItem(MESSAGES_KEY);
  if (!saved) return false;
  
  try {
    const messages = JSON.parse(saved);
    return Array.isArray(messages) && messages.length > 0;
  } catch {
    return false;
  }
}

