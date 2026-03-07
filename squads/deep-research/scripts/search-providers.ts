/**
 * Multi-Provider Search
 *
 * Priority order:
 * 1. EXA_API_KEY (best for semantic search)
 * 2. BRAVE_API_KEY (good balance)
 * 3. SERPAPI_KEY (Google results)
 * 4. Fallback: Return queries for WebSearch
 *
 * Usage:
 *   const provider = getSearchProvider();
 *   const results = await provider.search(query);
 */

export interface SearchResult {
  url: string;
  title: string;
  snippet: string;
  content?: string;
  score?: number;
  provider: 'exa' | 'brave' | 'serpapi' | 'websearch';
}

export interface SearchProvider {
  name: string;
  available: boolean;
  search: (query: string, numResults?: number) => Promise<SearchResult[]>;
}

// ============ EXA PROVIDER ============
const exaProvider: SearchProvider = {
  name: 'exa',
  available: !!process.env.EXA_API_KEY,

  async search(query: string, numResults = 10): Promise<SearchResult[]> {
    const response = await fetch('https://api.exa.ai/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.EXA_API_KEY!
      },
      body: JSON.stringify({
        query,
        numResults,
        type: 'auto',
        useAutoprompt: true,
        contents: {
          text: { maxCharacters: 3000 },
          highlights: { numSentences: 5 }
        }
      })
    });

    if (!response.ok) throw new Error(`Exa error: ${response.status}`);
    const data = await response.json();

    return data.results.map((r: any) => ({
      url: r.url,
      title: r.title,
      snippet: r.highlights?.join(' ') || '',
      content: r.text,
      score: r.score,
      provider: 'exa' as const
    }));
  }
};

// ============ BRAVE PROVIDER ============
const braveProvider: SearchProvider = {
  name: 'brave',
  available: !!process.env.BRAVE_API_KEY,

  async search(query: string, numResults = 10): Promise<SearchResult[]> {
    const params = new URLSearchParams({
      q: query,
      count: String(numResults)
    });

    const response = await fetch(`https://api.search.brave.com/res/v1/web/search?${params}`, {
      headers: {
        'Accept': 'application/json',
        'X-Subscription-Token': process.env.BRAVE_API_KEY!
      }
    });

    if (!response.ok) throw new Error(`Brave error: ${response.status}`);
    const data = await response.json();

    return (data.web?.results || []).map((r: any) => ({
      url: r.url,
      title: r.title,
      snippet: r.description || '',
      provider: 'brave' as const
    }));
  }
};

// ============ SERPAPI PROVIDER ============
const serpapiProvider: SearchProvider = {
  name: 'serpapi',
  available: !!process.env.SERPAPI_KEY,

  async search(query: string, numResults = 10): Promise<SearchResult[]> {
    const params = new URLSearchParams({
      q: query,
      api_key: process.env.SERPAPI_KEY!,
      engine: 'google',
      num: String(numResults)
    });

    const response = await fetch(`https://serpapi.com/search.json?${params}`);
    if (!response.ok) throw new Error(`SerpAPI error: ${response.status}`);
    const data = await response.json();

    return (data.organic_results || []).map((r: any) => ({
      url: r.link,
      title: r.title,
      snippet: r.snippet || '',
      provider: 'serpapi' as const
    }));
  }
};

// ============ FALLBACK PROVIDER ============
const fallbackProvider: SearchProvider = {
  name: 'websearch',
  available: true, // Always available

  async search(query: string): Promise<SearchResult[]> {
    // Returns empty - signals to use WebSearch tool
    console.log(`[Fallback] No API key available. Use WebSearch tool for: "${query}"`);
    return [];
  }
};

// ============ PROVIDER SELECTION ============
const providers: SearchProvider[] = [
  exaProvider,
  braveProvider,
  serpapiProvider,
  fallbackProvider
];

export function getSearchProvider(): SearchProvider {
  const available = providers.find(p => p.available);
  console.log(`[SearchProvider] Using: ${available?.name}`);
  return available || fallbackProvider;
}

export function getAvailableProviders(): string[] {
  return providers.filter(p => p.available).map(p => p.name);
}

export function getProviderStatus(): Record<string, boolean> {
  return {
    exa: !!process.env.EXA_API_KEY,
    brave: !!process.env.BRAVE_API_KEY,
    serpapi: !!process.env.SERPAPI_KEY,
    websearch: true
  };
}

// ============ UNIFIED SEARCH ============
export async function search(
  query: string,
  options?: {
    numResults?: number;
    preferredProvider?: 'exa' | 'brave' | 'serpapi';
  }
): Promise<SearchResult[]> {
  const { numResults = 10, preferredProvider } = options || {};

  // Use preferred if available
  if (preferredProvider) {
    const preferred = providers.find(p => p.name === preferredProvider && p.available);
    if (preferred) {
      return preferred.search(query, numResults);
    }
  }

  // Use best available
  const provider = getSearchProvider();
  return provider.search(query, numResults);
}

// ============ PARALLEL SEARCH ============
export async function parallelSearch(
  queries: string[],
  options?: {
    numResultsPerQuery?: number;
    dedupe?: boolean;
  }
): Promise<SearchResult[]> {
  const { numResultsPerQuery = 5, dedupe = true } = options || {};

  const provider = getSearchProvider();

  if (provider.name === 'websearch') {
    console.log('[ParallelSearch] No API available. Queries for WebSearch:');
    queries.forEach((q, i) => console.log(`  ${i + 1}. ${q}`));
    return [];
  }

  const promises = queries.map(q =>
    provider.search(q, numResultsPerQuery).catch(err => {
      console.error(`[ParallelSearch] Error for "${q}": ${err.message}`);
      return [] as SearchResult[];
    })
  );

  const resultsArrays = await Promise.all(promises);
  let allResults = resultsArrays.flat();

  // Dedupe by URL
  if (dedupe) {
    const seen = new Set<string>();
    allResults = allResults.filter(r => {
      if (seen.has(r.url)) return false;
      seen.add(r.url);
      return true;
    });
  }

  return allResults;
}

// ============ CLI ============
const args = process.argv.slice(2);

if (args.length > 0) {
  if (args[0] === '--status') {
    console.log('Provider Status:');
    console.log(JSON.stringify(getProviderStatus(), null, 2));
  } else {
    const query = args.join(' ');
    search(query)
      .then(results => {
        console.log(`Found ${results.length} results:`);
        results.forEach((r, i) => {
          console.log(`\n${i + 1}. ${r.title}`);
          console.log(`   ${r.url}`);
          console.log(`   ${r.snippet.substring(0, 200)}...`);
        });
      })
      .catch(err => {
        console.error('Error:', err);
        process.exit(1);
      });
  }
}
