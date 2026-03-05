/**
 * Protagons ClawHub Skill — ES module entry point.
 *
 * Provides tools for browsing, deploying, and generating Protagon
 * character identities from within an OpenClaw workspace.
 *
 * @module protagons
 */

const API_BASE = 'https://api.usaw.ai/api/v1';
const REQUEST_TIMEOUT_MS = 30_000;

/**
 * Fetch JSON from the Protagons API with timeout.
 *
 * @param {string} path - API path (e.g. '/library').
 * @param {Object} [options] - Fetch options.
 * @returns {Promise<Object>} Parsed JSON response.
 */
async function apiFetch(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const resp = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!resp.ok) {
      const body = await resp.json().catch(() => ({}));
      throw new Error(body.message || `API ${resp.status}: ${path}`);
    }

    return resp.json();
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * List available Protagons from the public library.
 *
 * @param {Object} params - Query parameters.
 * @param {number} [params.page=1] - Page number.
 * @param {number} [params.limit=20] - Items per page.
 * @param {string} [params.category] - Category filter.
 * @param {string} [params.search] - Search query.
 * @returns {Promise<Object>} Paginated list of Protagons.
 */
export async function protagons_list(params = {}) {
  const qs = new URLSearchParams();
  if (params.page) qs.set('page', params.page);
  if (params.limit) qs.set('limit', params.limit);
  if (params.category) qs.set('category', params.category);
  if (params.search) qs.set('search', params.search);

  const queryString = qs.toString();
  return apiFetch(`/library${queryString ? `?${queryString}` : ''}`);
}

/**
 * Fetch a single Protagon by slug.
 *
 * @param {Object} params - Tool parameters.
 * @param {string} params.slug - Protagon slug.
 * @returns {Promise<Object>} Full .protagon.json object.
 */
export async function protagons_get(params) {
  if (!params.slug) throw new Error('slug is required');
  return apiFetch(`/library/${encodeURIComponent(params.slug)}`);
}

/**
 * Deploy a Protagon to the workspace as a SOUL.md file.
 *
 * @param {Object} params - Tool parameters.
 * @param {string} params.slug - Protagon slug to deploy.
 * @param {Object} context - OpenClaw context with workspace info.
 * @returns {Promise<Object>} Deploy result.
 */
export async function protagons_deploy(params, context) {
  if (!params.slug) throw new Error('slug is required');

  const protagon = await apiFetch(`/library/${encodeURIComponent(params.slug)}`);

  const name = protagon.name || 'Protagon';
  const prompt = protagon.synthesized_prompt?.content || '';
  const personality = protagon.personality || {};
  const bestFor = protagon.best_for || {};
  const tagline = protagon.tagline || '';

  // Build SOUL.md
  const lines = [`# ${name}`, ''];
  if (tagline) lines.push(`> ${tagline}`, '');
  lines.push('## Voice & Personality', '', prompt, '');

  if (Object.keys(personality).length > 0) {
    lines.push('## Personality Axes', '');
    const labels = {
      formal_casual: ['Formal', 'Casual'],
      analytical_emotional: ['Analytical', 'Emotional'],
      authoritative_collaborative: ['Authoritative', 'Collaborative'],
      serious_playful: ['Serious', 'Playful'],
      concise_elaborate: ['Concise', 'Elaborate'],
    };
    for (const [axis, value] of Object.entries(personality)) {
      if (labels[axis]) {
        const [left, right] = labels[axis];
        lines.push(`- **${left} / ${right}**: ${Number(value).toFixed(2)}`);
      }
    }
    lines.push('');
  }

  if (bestFor.summary || bestFor.use_cases?.length) {
    lines.push('## Best For', '');
    if (bestFor.summary) lines.push(bestFor.summary, '');
    for (const uc of bestFor.use_cases || []) {
      lines.push(`- ${uc}`);
    }
    lines.push('');
  }

  lines.push('---');
  lines.push(`*Deployed from Protagons: ${name} | ${new Date().toISOString().split('T')[0]}*`);

  const soulMd = lines.join('\n');

  return {
    soul_md: soulMd,
    protagon_slug: params.slug,
    protagon_name: name,
    content_tier: protagon.deployment?.content_tier || 'standard',
    deployed_at: new Date().toISOString(),
  };
}

/**
 * Check the current deployment status.
 *
 * @param {Object} _params - Unused.
 * @param {Object} context - OpenClaw context.
 * @returns {Object} Status information.
 */
export function protagons_status(_params, context) {
  return {
    skill: 'protagons',
    version: '1.0.0',
    api_base: API_BASE,
    available: true,
  };
}

/**
 * Generate a new Protagon from a description.
 *
 * @param {Object} params - Tool parameters.
 * @param {string} params.name - Character name.
 * @param {string} params.description - Character description.
 * @param {string} params.google_api_key - Google/Gemini API key.
 * @param {string} [params.protagons_api_key] - Protagons API key (pg-...).
 * @returns {Promise<Object>} Generation job info.
 */
export async function protagons_generate(params) {
  if (!params.name) throw new Error('name is required');
  if (!params.description) throw new Error('description is required');
  if (!params.google_api_key) throw new Error('google_api_key is required');

  const headers = { 'Content-Type': 'application/json' };
  if (params.protagons_api_key) {
    headers['Authorization'] = `Bearer ${params.protagons_api_key}`;
  }

  return apiFetch('/generate', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      name: params.name,
      description: params.description,
      google_api_key: params.google_api_key,
    }),
  });
}
