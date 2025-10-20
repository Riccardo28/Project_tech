import React, { useState, useEffect } from 'react';
import { Sparkles, Zap, Building2, TrendingUp, Search, Radar } from 'lucide-react';
import { API_ENDPOINTS } from '../config/api';

function TechNewsHub() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [aiArticles, setAiArticles] = useState([]);
  const [hackerNewsArticles, setHackerNewsArticles] = useState([]);
  const [experienceDevArticles, setExperienceDevArticles] = useState([]);
  const [automationArticles, setAutomationArticles] = useState([]);
  const [solutionArchitectArticles, setSolutionArchitectArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedArticle, setSelectedArticle] = useState(null);

  // Fetch AI articles from FastAPI RSS endpoint AI
  useEffect(() => {
    const fetchAi = async () => {
      setLoading(true);
      setError(null);
      try {
        // Fetch all three RSS feeds in parallel
        const responses = await Promise.all([
          fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/ArtificialInteligence.rss&limit=20`),
          fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/LLMDevs.rss&limit=20`),
          fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/LocalLLaMA.rss&limit=20`)
        ]);

        // Check if all responses are OK
        responses.forEach(res => {
          if (res.status !== 200) {
            throw new Error('Failed to fetch one or more AI RSS feeds');
          }
        });

        // Parse all JSON responses
        const dataArrays = await Promise.all(responses.map(res => res.json()));

        // Merge all articles from the three feeds
        const allArticles = dataArrays.flatMap(data => data.articles);

        // Format the articles to match the existing news item structure
        const formattedArticles = allArticles.map((article, index) => ({
          id: `ai_${index}`,
          title: article.title,
          category: 'llm',
          date: formatTimestamp(article.published),
          source: 'AI Communities',
          excerpt: stripHtml(article.summary || article.description || '').substring(0, 200) + '...',
          fullContent: stripHtml(article.content || article.description || article.summary || ''),
          url: article.link
        }));

        setAiArticles(formattedArticles);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching AI articles:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAi();
  }, []);

  // Fetch Hacker News articles from FastAPI
  useEffect(() => {
    const fetchHackerNews = async () => {
      setLoading(true);
      setError(null);
      try {
        const url = `${API_ENDPOINTS.hackerNews}?limit=20&story_type=topstories`;
        console.log('Fetching Hacker News from:', url);

        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          }
        });

        console.log('Hacker News response status:', response.status);

        if (!response.ok) {
          throw new Error(`Failed to fetch Hacker News articles: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        console.log('Hacker News data received:', data.total, 'articles');

        // Format the articles to match the existing news item structure
        const formattedArticles = data.articles.map(article => ({
          id: article.id,
          title: article.title,
          category: 'hacker_news',
          date: formatTimestamp(article.time),
          source: 'Hacker News',
          excerpt: `Score: ${article.score} | Comments: ${article.descendants || 0}`,
          url: article.url,
          by: article.by
        }));

        setHackerNewsArticles(formattedArticles);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching Hacker News:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHackerNews();
  }, []);

  // Fetch Experienced Devs articles from FastAPI RSS endpoint experienced devs
  useEffect(() => {
    const fetchExperienceDev = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/ExperiencedDevs.rss&limit=20`);
        if (response.status !== 200) {
          throw new Error('Failed to fetch Experienced Devs articles');
        }
        const data = await response.json();

        // Format the articles to match the existing news item structure
        const formattedArticles = data.articles.map((article, index) => ({
          id: `experience_dev_${index}`,
          title: article.title,
          category: 'experienced_devs',
          date: formatTimestamp(article.published),
          source: 'Experienced Devs',
          excerpt: stripHtml(article.summary || article.description || '').substring(0, 200) + '...',
          fullContent: stripHtml(article.content || article.description || article.summary || ''),
          url: article.link
        }));

        setExperienceDevArticles(formattedArticles);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching Experienced Devs:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchExperienceDev();
  }, []);

  // Helper function to format Unix timestamp or ISO 8601 string
  const formatTimestamp = (timestamp) => {
    // Handle both Unix timestamps (numbers) and ISO strings
    const date = typeof timestamp === 'number'
      ? new Date(timestamp * 1000)  // Unix timestamp is in seconds
      : new Date(timestamp);         // ISO string

    const now = Date.now();
    const diff = (now - date.getTime()) / 1000; // diff in seconds

    if (diff < 3600) {
      const minutes = Math.floor(diff / 60);
      return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
    } else if (diff < 86400) {
      const hours = Math.floor(diff / 3600);
      return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
    } else {
      const days = Math.floor(diff / 86400);
      return `${days} day${days !== 1 ? 's' : ''} ago`;
    }
  };

  // Helper function to strip HTML tags and clean up text
  const stripHtml = (html) => {
    if (!html) return '';

    // Remove HTML comments and tags
    const text = html
      .replace(/<!--[\s\S]*?-->/g, '') // Remove HTML comments
      .replace(/<[^>]+>/g, '')         // Remove HTML tags
      .replace(/&nbsp;/g, ' ')         // Replace &nbsp; with space
      .replace(/&amp;/g, '&')          // Replace &amp; with &
      .replace(/&lt;/g, '<')           // Replace &lt; with <
      .replace(/&gt;/g, '>')           // Replace &gt; with >
      .replace(/&quot;/g, '"')         // Replace &quot; with "
      .trim();

    return text;
  };

  // Helper function to format article content with better readability
  const formatArticleContent = (content) => {
    if (!content) return '';

    return content
      // Add spacing after periods followed by capital letters (likely new sentences)
      .replace(/\.([A-Z])/g, '.\n\n$1')
      // Preserve double line breaks
      .replace(/\n\n+/g, '\n\n')
      // Add spacing before common list indicators
      .replace(/([^\n])(\n- |\n\* |\n\d+\. )/g, '$1\n$2');
  };

  // Fetch Automation articles from FastAPI RSS endpoint Automation
  useEffect(() => {
    const fetchAutomation = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/automation.rss&limit=20`);
        if (response.status !== 200) {
          throw new Error('Failed to fetch Automation articles');
        }
        const data = await response.json();

        // Format the articles to match the existing news item structure
        const formattedArticles = data.articles.map((article, index) => ({
          id: `automation${index}`,
          title: article.title,
          category: 'automation',
          date: formatTimestamp(article.published),
          source: 'Automation',
          excerpt: stripHtml(article.summary || article.description || '').substring(0, 200) + '...',
          fullContent: stripHtml(article.content || article.description || article.summary || ''),
          url: article.link
        }));

        setAutomationArticles(formattedArticles);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching Automation:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAutomation();
  }, []);

  

  // Fetch Solution architecture articles from FastAPI RSS endpoint Solution Architect
  useEffect(() => {
    const fetchSolutionArchitect = async () => {
      setLoading(true);
      setError(null);
      try {
        // Fetch architecture-related RSS feeds in parallel
        const responses = await Promise.all([
          fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/softwarearchitecture.rss&limit=20`),
          fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/aws.rss&limit=20`),
          fetch(`${API_ENDPOINTS.rss}?url=https://www.reddit.com/r/devops.rss&limit=20`)
        ]);

        // Check if all responses are OK
        responses.forEach(res => {
          if (res.status !== 200) {
            throw new Error('Failed to fetch one or more solution architecture RSS feeds');
          }
        });

        // Parse all JSON responses
        const dataArrays = await Promise.all(responses.map(res => res.json()));

        // Merge all articles from the three feeds
        const allArticles = dataArrays.flatMap(data => data.articles);

        // Format the articles to match the existing news item structure
        const formattedArticles = allArticles.map((article, index) => ({
          id: `solution_architecture_${index}`,
          title: article.title,
          category: 'architecture',
          date: formatTimestamp(article.published),
          source: 'Architecture Communities',
          excerpt: stripHtml(article.summary || article.description || '').substring(0, 200) + '...',
          fullContent: stripHtml(article.content || article.description || article.summary || ''),
          url: article.link
        }));

        setSolutionArchitectArticles(formattedArticles);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching solution architecture articles:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSolutionArchitect();
  }, []);

  const newsItems = [];

  const categories = [
    { id: 'all', label: 'All News', icon: TrendingUp, color: 'bg-purple-500' },
    { id: 'llm', label: 'LLM Models', icon: Sparkles, color: 'bg-blue-500' },
    { id: 'automation', label: 'Automation Tools', icon: Zap, color: 'bg-green-500' },
    { id: 'architecture', label: 'Architecture', icon: Building2, color: 'bg-orange-500' },
    { id: 'hacker_news', label: 'Hacker News', icon: TrendingUp, color: 'bg-pink-500' },
    { id: 'experienced_devs', label: 'Experienced Devs', icon: Radar, color: 'bg-cyan-500' },
  ];

  // Combine static news with Hacker News and Experienced Devs articles
  const allNews = [...newsItems, ...aiArticles, ...hackerNewsArticles, ...experienceDevArticles, ...automationArticles, ...solutionArchitectArticles];

  const filteredNews = allNews.filter(item => {
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.excerpt.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-5xl font-bold text-white mb-3 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Tech News Hub
          </h1>
          <p className="text-slate-400 text-lg">
            Your source for LLMs, automation tools, and architecture trends
          </p>
        </header>

        {/* Loading and Error States */}
        {loading && (
          <div className="mb-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg text-blue-400 text-center">
            Loading Hacker News articles...
          </div>
        )}

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-center">
            Error loading Hacker News: {error}
          </div>
        )}

        {/* Search Bar */}
        <div className="mb-8 relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
          <input
            type="text"
            placeholder="Search news..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
          />
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap gap-3 mb-8">
          {categories.map(cat => {
            const Icon = cat.icon;
            return (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-full font-medium transition-all ${
                  selectedCategory === cat.id
                    ? `${cat.color} text-white shadow-lg scale-105`
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                <Icon size={18} />
                {cat.label}
              </button>
            );
          })}
        </div>

        {/* News Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredNews.map(item => {
            const category = categories.find(c => c.id === item.category);
            if (!category) return null; // Skip if category not found
            const Icon = category.icon;

            return (
              <article
                key={item.id}
                onClick={() => setSelectedArticle(item)}
                className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6 hover:border-blue-500/50 hover:shadow-xl hover:shadow-blue-500/10 transition-all cursor-pointer group"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className={`${category.color} p-2 rounded-lg`}>
                    <Icon size={20} className="text-white" />
                  </div>
                  <span className="text-sm text-slate-400">{item.date}</span>
                </div>
                
                <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-blue-400 transition-colors">
                  {item.title}
                </h3>
                
                <p className="text-slate-400 text-sm mb-4 line-clamp-3">
                  {item.excerpt}
                </p>
                
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-500">
                    {item.source}
                  </span>
                  <span className="text-xs text-blue-400 group-hover:underline">
                    Read more →
                  </span>
                </div>
              </article>
            );
          })}
        </div>

        {filteredNews.length === 0 && (
          <div className="text-center py-20">
            <p className="text-slate-400 text-lg">No news found matching your criteria</p>
          </div>
        )}

        {/* Article Modal */}
        {selectedArticle && (
          <div
            className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
            onClick={() => setSelectedArticle(null)}
          >
            <div
              className="bg-slate-800 rounded-xl max-w-3xl w-full max-h-[80vh] overflow-y-auto p-6 border border-slate-700"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-white pr-8">{selectedArticle.title}</h2>
                <button
                  onClick={() => setSelectedArticle(null)}
                  className="text-slate-400 hover:text-white text-2xl leading-none"
                >
                  ×
                </button>
              </div>

              <div className="flex items-center gap-4 text-sm text-slate-400 mb-6 pb-4 border-b border-slate-700">
                <span>{selectedArticle.source}</span>
                <span>•</span>
                <span>{selectedArticle.date}</span>
              </div>

              <div className="text-slate-300 mb-6 prose prose-invert max-w-none">
                <div className="whitespace-pre-line leading-relaxed">
                  {formatArticleContent(selectedArticle.fullContent || selectedArticle.excerpt)}
                </div>
              </div>

              {selectedArticle.url && (
                <a
                  href={selectedArticle.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
                >
                  View Original →
                </a>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default TechNewsHub;