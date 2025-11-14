/**
 * Session management utilities
 * Handles session ID generation and persistence
 */

const SESSION_KEY = 'eliseai_session_id';

/**
 * Generate a unique session ID
 */
function generateSessionId(): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 15);
  return `session_${timestamp}_${random}`;
}

/**
 * Get existing session ID or create a new one
 * Session persists across browser sessions via localStorage
 */
export function getOrCreateSessionId(): string {
  let sessionId = localStorage.getItem(SESSION_KEY);
  
  if (!sessionId) {
    sessionId = generateSessionId();
    localStorage.setItem(SESSION_KEY, sessionId);
  }
  
  return sessionId;
}

/**
 * Clear current session (for testing or reset)
 */
export function clearSession(): void {
  localStorage.removeItem(SESSION_KEY);
}

