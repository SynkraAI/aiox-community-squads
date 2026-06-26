/**
 * Deep Search Script
 *
 * Arquitetura econômica de tokens:
 * 1. Faz N buscas paralelas (Exa ou WebSearch)
 * 2. Lê páginas relevantes
 * 3. Filtra/resume antes de passar pro Claude
 *
 * Uso via CLI:
 *   npx ts-node deep-search.ts "query" --max-results=20 --read-pages=5
 *
 * Uso via import:
 *   import { deepSearch } from './deep-search'
 *   const results = await deepSearch({ query, maxResults: 20 })
 */

interface SearchResult {
  url: string;
  title: string;
  snippet: string;
  content?: string; // Full page content if read
  score?: number;
  source: 'exa' | 'websearch';
}

interface DeepSearchOptions {
  query: string;
  subQueries?: string[];
  maxResults?: number;
  readPages?: number;
  useExa?: boolean;
  exaApiKey?: string;
}

interface DeepSearchResult {
  query: string;
  results: SearchResult[];
  summary: string;
  sources: string[];
  tokenEstimate: number;
}

// Exa API types
interface ExaSearchParams {
  query: string;
  numResults?: number;
  type?: 'keyword' | 'neural' | 'auto';
  useAutoprompt?: boolean;
  contents?: {
    text?: boolean | { maxCharacters?: number };
    highlights?: boolean | { numSentences?: number };
  };
}

/**
 * Search via Exa API (when available)
 */
async function searchExa(
  query: string,
  apiKey: string,
  numResults: number = 10
): Promise<SearchResult[]> {
  const params: ExaSearchParams = {
    query,
    numResults,
    type: 'auto',
    useAutoprompt: true,
    contents: {
      text: { maxCharacters: 2000 },
      highlights: { numSentences: 3 }
    }
  };

  const response = await fetch('https://api.exa.ai/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey
    },
    body: JSON.stringify(params)
  });

  if (!response.ok) {
    throw new Error(`Exa API error: ${response.status}`);
  }

  const data = await response.json();

  return data.results.map((r: any) => ({
    url: r.url,
    title: r.title,
    snippet: r.highlights?.join(' ') || r.text?.substring(0, 500) || '',
    content: r.text,
    score: r.score,
    source: 'exa' as const
  }));
}

/**
 * Decompose query into sub-queries for parallel search
 */
function decomposeQuery(query: string): string[] {
  // Simple decomposition - can be enhanced with LLM
  const baseQuery = query;
  const subQueries = [
    baseQuery,
    `${baseQuery} tutorial example`,
    `${baseQuery} best practices 2025 2026`,
    `${baseQuery} comparison alternatives`,
    `${baseQuery} implementation guide`
  ];
  return subQueries;
}

/**
 * Filter and dedupe results
 */
function filterResults(results: SearchResult[]): SearchResult[] {
  const seen = new Set<string>();
  return results
    .filter(r => {
      if (seen.has(r.url)) return false;
      seen.add(r.url);
      return true;
    })
    .sort((a, b) => (b.score || 0) - (a.score || 0));
}

/**
 * Estimate tokens in results
 */
function estimateTokens(results: SearchResult[]): number {
  let chars = 0;
  for (const r of results) {
    chars += (r.title?.length || 0);
    chars += (r.snippet?.length || 0);
    chars += (r.content?.length || 0);
  }
  return Math.ceil(chars / 4); // ~4 chars per token
}

/**
 * Create summary of results (pre-filter for Claude)
 */
function summarizeResults(results: SearchResult[]): string {
  const lines: string[] = [];

  lines.push(`# Search Results Summary`);
  lines.push(`Found ${results.length} unique sources\n`);

  for (let i = 0; i < Math.min(results.length, 10); i++) {
    const r = results[i];
    lines.push(`## ${i + 1}. ${r.title}`);
    lines.push(`URL: ${r.url}`);
    lines.push(`Score: ${r.score?.toFixed(2) || 'N/A'}`);
    lines.push(`\n${r.snippet}\n`);

    if (r.content && r.content.length > r.snippet.length) {
      lines.push(`### Key Content`);
      lines.push(r.content.substring(0, 1500));
      lines.push('\n---\n');
    }
  }

  return lines.join('\n');
}

/**
 * Main deep search function
 */
export async function deepSearch(options: DeepSearchOptions): Promise<DeepSearchResult> {
  const {
    query,
    subQueries = decomposeQuery(query),
    maxResults = 20,
    readPages = 5,
    useExa = true,
    exaApiKey = process.env.EXA_API_KEY
  } = options;

  let allResults: SearchResult[] = [];

  if (useExa && exaApiKey) {
    // Use Exa API - parallel search all sub-queries
    console.log(`[DeepSearch] Using Exa API for ${subQueries.length} queries`);

    const promises = subQueries.map(q =>
      searchExa(q, exaApiKey, Math.ceil(maxResults / subQueries.length))
        .catch(err => {
          console.error(`[DeepSearch] Exa error for "${q}": ${err.message}`);
          return [] as SearchResult[];
        })
    );

    const resultsArrays = await Promise.all(promises);
    allResults = resultsArrays.flat();
  } else {
    // Fallback message - actual WebSearch would be done by Claude
    console.log(`[DeepSearch] Exa not available, returning decomposed queries for WebSearch`);
    return {
      query,
      results: [],
      summary: `No Exa API. Use these queries with WebSearch:\n${subQueries.map((q, i) => `${i + 1}. ${q}`).join('\n')}`,
      sources: [],
      tokenEstimate: 0
    };
  }

  // Filter and dedupe
  const filtered = filterResults(allResults).slice(0, maxResults);

  // Create summary
  const summary = summarizeResults(filtered);

  // Extract sources
  const sources = filtered.map(r => r.url);

  return {
    query,
    results: filtered,
    summary,
    sources,
    tokenEstimate: estimateTokens(filtered)
  };
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const query = args.find(a => !a.startsWith('--')) || '';

  if (!query) {
    console.log('Usage: npx ts-node deep-search.ts "your query" [--max-results=20] [--read-pages=5]');
    process.exit(1);
  }

  const maxResults = parseInt(args.find(a => a.startsWith('--max-results='))?.split('=')[1] || '20');
  const readPages = parseInt(args.find(a => a.startsWith('--read-pages='))?.split('=')[1] || '5');

  deepSearch({ query, maxResults, readPages })
    .then(result => {
      console.log(result.summary);
      console.log(`\n---\nToken estimate: ${result.tokenEstimate}`);
    })
    .catch(err => {
      console.error('Error:', err);
      process.exit(1);
    });
}
