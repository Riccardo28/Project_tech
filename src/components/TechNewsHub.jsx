import React, { useState } from 'react';
import { Sparkles, Zap, Building2, TrendingUp, Search } from 'lucide-react';

function TechNewsHub() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const newsItems = [
    {
      id: 1,
      title: "GPT-5 Rumors: OpenAI Hints at Major Breakthrough",
      category: "llm",
      date: "2 hours ago",
      source: "TechCrunch",
      excerpt: "Industry insiders suggest the next generation of language models could arrive sooner than expected with significant improvements in reasoning capabilities."
    },
    {
      id: 2,
      title: "Zapier Unveils Advanced Canvas for No-Code Automation",
      category: "automation",
      date: "5 hours ago",
      source: "VentureBeat",
      excerpt: "The popular automation platform introduces a visual builder that allows users to create complex workflows without writing a single line of code."
    },
    {
      id: 3,
      title: "Microservices vs Monoliths: The Pendulum Swings Back",
      category: "architecture",
      date: "1 day ago",
      source: "InfoQ",
      excerpt: "Leading tech companies are reconsidering their architecture choices as maintenance costs and complexity of microservices become apparent."
    },
    {
      id: 4,
      title: "Anthropic Releases Claude 4: Enhanced Multi-Modal Capabilities",
      category: "llm",
      date: "3 hours ago",
      source: "The Verge",
      excerpt: "The latest iteration promises better understanding of images, charts, and documents with improved context handling up to 200K tokens."
    },
    {
      id: 5,
      title: "Make.com Acquires Automation Startup for $150M",
      category: "automation",
      date: "8 hours ago",
      source: "Business Insider",
      excerpt: "The acquisition signals continued consolidation in the automation tools market as demand for workflow optimization grows."
    },
    {
      id: 6,
      title: "Event-Driven Architecture Gains Momentum in Enterprise",
      category: "architecture",
      date: "12 hours ago",
      source: "DZone",
      excerpt: "More organizations are adopting event-driven patterns to build responsive, scalable systems that can handle real-time data streams."
    },
    {
      id: 7,
      title: "Google Gemini 2.0 Shows Impressive Coding Abilities",
      category: "llm",
      date: "6 hours ago",
      source: "Ars Technica",
      excerpt: "Benchmarks reveal that the latest Gemini model outperforms competitors in programming tasks and technical documentation generation."
    },
    {
      id: 8,
      title: "AI-Powered Automation Tools See 300% Growth",
      category: "automation",
      date: "1 day ago",
      source: "Forbes",
      excerpt: "Market research shows explosive growth in AI-enhanced automation platforms as businesses seek to optimize operations and reduce costs."
    },
    {
      id: 9,
      title: "Serverless Architectures Hit Mainstream Adoption",
      category: "architecture",
      date: "18 hours ago",
      source: "AWS Blog",
      excerpt: "Major enterprises report significant cost savings and improved scalability after migrating critical workloads to serverless platforms."
    }
  ];

  const categories = [
    { id: 'all', label: 'All News', icon: TrendingUp, color: 'bg-purple-500' },
    { id: 'llm', label: 'LLM Models', icon: Sparkles, color: 'bg-blue-500' },
    { id: 'automation', label: 'Automation Tools', icon: Zap, color: 'bg-green-500' },
    { id: 'architecture', label: 'Architecture', icon: Building2, color: 'bg-orange-500' }
  ];

  const filteredNews = newsItems.filter(item => {
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
            const Icon = category.icon;
            
            return (
              <article
                key={item.id}
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
      </div>
    </div>
  );
}

export default TechNewsHub;
