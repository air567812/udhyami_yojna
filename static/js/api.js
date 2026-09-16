/**
 * API Client Module for Udhyami Yojna
 * Communicates with FastAPI backend endpoints (/api/*)
 */

const API_BASE = '/api';

/**
 * Sends speech transcript to backend for Gemini/heuristic extraction.
 * @param {string} transcript - The raw speech text
 * @param {string} language - Locale code, e.g. "hi-IN"
 * @returns {Promise<Object>} ExtractionResponse containing profile and metadata
 */
export async function extractTranscript(transcript, language = 'hi-IN') {
  const response = await fetch(`${API_BASE}/extract`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      transcript: transcript.trim(),
      language: language
    })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server error: ${response.status}`);
  }

  return await response.json();
}

/**
 * Submits reviewed user profile for rule-based scoring and Gemini advice.
 * @param {Object} profile - UserProfile object
 * @returns {Promise<Object>} SchemeMatchResponse with ranked schemes
 */
export async function matchSchemes(profile) {
  const response = await fetch(`${API_BASE}/match-schemes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(profile)
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Matching error: ${response.status}`);
  }

  return await response.json();
}

/**
 * Fetches scheme catalog with optional filters.
 * @param {Object} filters - { sector, state, category, type, search }
 * @returns {Promise<Array>} List of Scheme objects
 */
export async function fetchSchemes(filters = {}) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value && value !== 'All') {
      params.append(key, value);
    }
  }

  const url = `${API_BASE}/schemes${params.toString() ? '?' + params.toString() : ''}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to load schemes: ${response.status}`);
  }

  return await response.json();
}

/**
 * Fetches specific scheme details by ID.
 * @param {string} schemeId
 * @returns {Promise<Object>}
 */
export async function fetchSchemeById(schemeId) {
  const response = await fetch(`${API_BASE}/schemes/${encodeURIComponent(schemeId)}`);
  if (!response.ok) {
    throw new Error(`Scheme ${schemeId} not found.`);
  }
  return await response.json();
}

/**
 * Fetches all state entrepreneurial ecosystems.
 * @returns {Promise<Array>}
 */
export async function fetchStates() {
  const response = await fetch(`${API_BASE}/states`);
  if (!response.ok) {
    throw new Error(`Failed to load state ecosystems: ${response.status}`);
  }
  return await response.json();
}

/**
 * Fetches details and state-specific schemes for a given state code.
 * @param {string} stateCode - e.g. "MH", "UP"
 * @returns {Promise<Object>}
 */
export async function fetchStateDetails(stateCode) {
  const response = await fetch(`${API_BASE}/states/${encodeURIComponent(stateCode)}`);
  if (!response.ok) {
    throw new Error(`State ${stateCode} details unavailable: ${response.status}`);
  }
  return await response.json();
}

/**
 * Checks backend health status.
 * @returns {Promise<Object>}
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    if (response.ok) {
      return await response.json();
    }
    return { status: 'degraded' };
  } catch (e) {
    return { status: 'offline', error: e.message };
  }
}
