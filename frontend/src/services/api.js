// API service for connecting to the backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class FinanceAPI {
  // Stock Data APIs
  async getStockInfo(ticker) {
    const response = await fetch(`${API_BASE_URL}/api/stock/${ticker}`);
    if (!response.ok) throw new Error('Failed to fetch stock info');
    return response.json();
  }

  async getStockHistory(ticker, period = '1mo', interval = '1d') {
    const response = await fetch(
      `${API_BASE_URL}/api/stock/${ticker}/history?period=${period}&interval=${interval}`
    );
    if (!response.ok) throw new Error('Failed to fetch stock history');
    return response.json();
  }

  async getStockMetrics(ticker) {
    const response = await fetch(`${API_BASE_URL}/api/stock/${ticker}/metrics`);
    if (!response.ok) throw new Error('Failed to fetch stock metrics');
    return response.json();
  }

  // News APIs
  async getCompanyNews(ticker, limit = 10) {
    const response = await fetch(
      `${API_BASE_URL}/api/news/${ticker}?limit=${limit}`
    );
    if (!response.ok) throw new Error('Failed to fetch news');
    return response.json();
  }

  async getNewsSentiment(ticker) {
    const response = await fetch(`${API_BASE_URL}/api/news/${ticker}/sentiment`);
    if (!response.ok) throw new Error('Failed to fetch news sentiment');
    return response.json();
  }

  // AI Analysis APIs
  async analyzeInvestment(ticker, question = null, includeRecommendation = true) {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ticker,
        question,
        include_recommendation: includeRecommendation,
      }),
    });
    if (!response.ok) throw new Error('Failed to analyze investment');
    return response.json();
  }

  async askQuestion(ticker, question) {
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ticker,
        question,
      }),
    });
    if (!response.ok) throw new Error('Failed to ask question');
    return response.json();
  }

  async compareStocks(tickers) {
    const response = await fetch(`${API_BASE_URL}/api/compare`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tickers,
      }),
    });
    if (!response.ok) throw new Error('Failed to compare stocks');
    return response.json();
  }

  // Health check
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return response.ok;
    } catch (error) {
      return false;
    }
  }
}

export default new FinanceAPI();
