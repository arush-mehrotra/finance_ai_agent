import { useState, useEffect } from 'react';
import './App.css';
import api from './services/api';
import ReactMarkdown from 'react-markdown';

function App() {
  const [ticker, setTicker] = useState('');
  const [currentStock, setCurrentStock] = useState(null);
  const [stockInfo, setStockInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);

  // News state
  const [newsData, setNewsData] = useState([]);
  const [newsSentiment, setNewsSentiment] = useState(null);
  const [newsLoading, setNewsLoading] = useState(false);

  // Check backend connection on mount
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    const connected = await api.healthCheck();
    setIsConnected(connected);
  };

  // Fetch news when stock changes
  useEffect(() => {
    if (currentStock) {
      fetchNews();
    }
  }, [currentStock]);

  const fetchNews = async () => {
    if (!currentStock) return;

    setNewsLoading(true);
    try {
      // Fetch news sentiment which includes recent news articles
      const sentimentResult = await api.getNewsSentiment(currentStock);

      if (sentimentResult.success) {
        setNewsSentiment(sentimentResult.data);
        console.log(sentimentResult.data);
        // Extract recent news from sentiment data
        setNewsData(sentimentResult.data.recent_news || []);
      }
    } catch (err) {
      console.error('Error fetching news:', err);
      setNewsData([]);
      setNewsSentiment(null);
    } finally {
      setNewsLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!ticker.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await api.getStockInfo(ticker.toUpperCase());
      if (result.success) {
        setStockInfo(result.data);
        setCurrentStock(ticker.toUpperCase());
        // Add welcome message
        setMessages([{
          type: 'assistant',
          content: `I've loaded information for ${result.data.name}. What would you like to know?`,
          timestamp: new Date()
        }]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !currentStock) return;

    const userMessage = {
      type: 'user',
      content: chatInput,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setChatInput('');
    setLoading(true);

    try {
      const result = await api.askQuestion(currentStock, chatInput);
      if (result.success) {
        const aiMessage = {
          type: 'assistant',
          content: result.answer,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, aiMessage]);
      }
    } catch (err) {
      const errorMessage = {
        type: 'error',
        content: `Error: ${err.message}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!currentStock) return;

    setLoading(true);
    const userMessage = {
      type: 'user',
      content: 'Analyze this stock for me',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      const result = await api.analyzeInvestment(currentStock);
      if (result.success) {
        const analysis = result.ai_analysis.analysis;
        const recommendation = result.recommendation;

        const aiMessage = {
          type: 'assistant',
          content: analysis,
          recommendation: recommendation,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, aiMessage]);
      }
    } catch (err) {
      const errorMessage = {
        type: 'error',
        content: `Error: ${err.message}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    if (!num) return 'N/A';
    if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
    return `$${num.toFixed(2)}`;
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp * 1000);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));

    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    if (diffInHours < 48) return 'Yesterday';
    return date.toLocaleDateString();
  };

  return (
    <div className="min-h-screen bg-dark text-white">
      {/* Header */}
      <header className="bg-card border-b border-gray-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
                <span className="text-2xl">📈</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold">Finance AI Agent</h1>
                <p className="text-sm text-gray-400">AI-Powered Investment Insights</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-success animate-pulse' : 'bg-error'}`}></div>
              <span className="text-sm text-gray-400">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel: Dashboard */}
          <div className="space-y-6">
            {/* Stock Search */}
            <div className="bg-card rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold mb-4">Search Stock</h2>
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value.toUpperCase())}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  placeholder="Enter ticker symbol (e.g., AAPL, TSLA)"
                  className="flex-1 bg-dark border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary"
                />
                <button
                  onClick={handleSearch}
                  disabled={loading}
                  className="bg-primary hover:bg-blue-600 text-white px-6 py-3 rounded-lg transition-colors disabled:opacity-50"
                >
                  {loading ? 'Loading...' : 'Search'}
                </button>
              </div>
              {error && (
                <div className="mt-3 p-3 bg-error bg-opacity-20 border border-error rounded-lg text-sm">
                  {error}
                </div>
              )}
            </div>

            {/* Stock Info Card */}
            {stockInfo ? (
              <div className="bg-card rounded-xl p-6 shadow-xl">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-2xl font-bold">{stockInfo.name}</h3>
                    <p className="text-gray-400">{stockInfo.ticker}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-3xl font-bold">${stockInfo.current_price?.toFixed(2) || 'N/A'}</p>
                  </div>
                </div>

                {/* Quick Metrics */}
                <div className="grid grid-cols-2 gap-4 mt-6">
                  <div className="bg-dark rounded-lg p-4">
                    <p className="text-gray-400 text-sm">Market Cap</p>
                    <p className="text-lg font-bold mt-1">{formatNumber(stockInfo.market_cap)}</p>
                  </div>
                  <div className="bg-dark rounded-lg p-4">
                    <p className="text-gray-400 text-sm">P/E Ratio</p>
                    <p className="text-lg font-bold mt-1">{stockInfo.pe_ratio?.toFixed(2) || 'N/A'}</p>
                  </div>
                  <div className="bg-dark rounded-lg p-4">
                    <p className="text-gray-400 text-sm">Sector</p>
                    <p className="text-lg font-bold mt-1">{stockInfo.sector || 'N/A'}</p>
                  </div>
                  <div className="bg-dark rounded-lg p-4">
                    <p className="text-gray-400 text-sm">Industry</p>
                    <p className="text-lg font-bold mt-1">{stockInfo.industry || 'N/A'}</p>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="grid grid-cols-1 gap-3 mt-6">
                  <button
                    onClick={handleAnalyze}
                    disabled={loading}
                    className="bg-primary hover:bg-blue-600 text-white px-4 py-3 rounded-lg transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
                  >
                    <span>🧠</span>
                    <span>Get AI Analysis</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-card rounded-xl p-6 shadow-xl">
                <h3 className="text-xl font-bold mb-4">Stock Information</h3>
                <p className="text-gray-400 text-center py-8">Search for a stock to view information</p>
              </div>
            )}

            {/* News Panel */}
            {currentStock && (
              <div className="bg-card rounded-xl p-6 shadow-xl">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold">Latest News</h3>
                  {newsLoading && (
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-accent rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                    </div>
                  )}
                </div>

                {/* Sentiment Summary */}
                {newsSentiment && newsSentiment.sentiment && (
                  <div className="bg-dark rounded-lg p-4 mb-4 text-center">
                    <p className="text-sm text-gray-400 mb-2">Overall Sentiment</p>
                    <span className={`px-4 py-2 rounded-full text-lg font-bold ${
                      newsSentiment.sentiment === 'positive' ? 'bg-success bg-opacity-20 text-success' :
                      newsSentiment.sentiment === 'negative' ? 'bg-error bg-opacity-20 text-error' :
                      'bg-gray-600 bg-opacity-20 text-gray-300'
                    }`}>
                      {newsSentiment.sentiment.toUpperCase()}
                    </span>
                  </div>
                )}

                {/* News Articles List */}
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {newsData.length === 0 && !newsLoading ? (
                    <p className="text-gray-400 text-center py-8">No news articles found</p>
                  ) : (
                    newsData.map((article, index) => (
                      <div key={index} className="bg-dark rounded-lg p-3 hover:bg-gray-800 transition-colors">
                        <div className="flex gap-3">
                          {/* Article Thumbnail */}
                          {article.image && (
                            <div className="flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden bg-gray-700">
                              <img
                                src={article.image}
                                alt={article.title}
                                className="w-full h-full object-cover"
                                onError={(e) => {
                                  e.target.style.display = 'none';
                                }}
                                loading="lazy"
                              />
                            </div>
                          )}

                          {/* Article Content */}
                          <div className="flex-1 min-w-0">
                            <a
                              href={article.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-white hover:text-primary transition-colors"
                            >
                              <h4 className="font-semibold text-sm leading-tight line-clamp-2 mb-1">
                                {article.title}
                              </h4>
                            </a>

                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-xs text-gray-400">
                                {article.source}
                              </span>
                              <span className="text-xs text-gray-500">•</span>
                              <span className="text-xs text-gray-400">
                                {formatTimestamp(article.published_at)}
                              </span>
                              {article.sentiment && (
                                <>
                                  <span className="text-xs text-gray-500">•</span>
                                  <span className={`text-xs font-medium ${
                                    article.sentiment === 'positive' ? 'text-success' :
                                    article.sentiment === 'negative' ? 'text-error' :
                                    'text-gray-400'
                                  }`}>
                                    {article.sentiment}
                                  </span>
                                </>
                              )}
                            </div>

                            {article.description && (
                              <p className="text-xs text-gray-400 line-clamp-2">
                                {article.description}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Right Panel: AI Chat */}
          <div className="bg-card rounded-xl shadow-xl flex flex-col" style={{height: 'calc(100vh - 180px)'}}>
            <div className="p-6 border-b border-gray-700">
              <h2 className="text-xl font-bold">AI Assistant</h2>
              <p className="text-sm text-gray-400 mt-1">
                {currentStock ? `Analyzing ${currentStock}` : 'Search for a stock to start'}
              </p>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.length === 0 ? (
                <div className="text-center text-gray-400 py-8">
                  <p className="text-4xl mb-3">✨</p>
                  <p>Search for a stock to start analyzing!</p>
                </div>
              ) : (
                messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        msg.type === 'user'
                          ? 'bg-primary text-white'
                          : msg.type === 'error'
                          ? 'bg-error bg-opacity-20 border border-error'
                          : 'bg-dark text-white'
                      }`}
                    >
                      {msg.type === 'assistant' || msg.type === 'error' ? (
                        <div className="markdown-content">
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                      ) : (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      )}
                      {msg.recommendation && (
                        <div className="mt-3 p-3 bg-dark rounded-lg border border-gray-700">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-bold">Recommendation:</span>
                            <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                              msg.recommendation.recommendation === 'BUY' ? 'bg-success text-white' :
                              msg.recommendation.recommendation === 'SELL' ? 'bg-error text-white' :
                              'bg-gray-600 text-white'
                            }`}>
                              {msg.recommendation.recommendation}
                            </span>
                          </div>
                          <p className="text-sm text-gray-400">
                            Confidence: {msg.recommendation.confidence}
                          </p>
                        </div>
                      )}
                      <p className={`text-xs mt-2 ${
                        msg.type === 'user' ? 'text-blue-200' : 'text-gray-400'
                      }`}>
                        {msg.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))
              )}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-dark rounded-lg p-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-accent rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      <div className="w-2 h-2 bg-accent rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Chat Input */}
            <div className="p-6 border-t border-gray-700">
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder={currentStock ? "Ask a question about the stock..." : "Search for a stock first..."}
                  disabled={!currentStock || loading}
                  className="flex-1 bg-dark border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent disabled:opacity-50"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!currentStock || loading || !chatInput.trim()}
                  className="bg-accent hover:bg-purple-600 text-white px-6 py-3 rounded-lg transition-colors disabled:opacity-50"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
