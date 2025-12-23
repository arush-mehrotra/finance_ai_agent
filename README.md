# Finance AI Agent

An AI-powered investment analysis application that provides real-time stock data, news sentiment analysis, and intelligent investment recommendations.

## Features

- **Stock Analysis**: Real-time stock information including price, market cap, P/E ratio, sector, and industry
- **News Integration**: Latest news articles with sentiment analysis (positive/negative/neutral)
- **AI Chat Assistant**: Interactive AI agent for asking questions about stocks and getting detailed investment analysis
- **Investment Recommendations**: AI-generated BUY/SELL/HOLD recommendations with confidence scores
- **Dark/Light Mode**: Fully responsive theme switching with localStorage persistence

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **OpenAI API**: Powers the AI agent for investment analysis
- **Finnhub API**: Real-time stock data and news
- **yfinance**: Historical stock data and financial metrics

### Frontend
- **React**: UI component library
- **Tailwind CSS**: Utility-first CSS framework with dark mode support
- **ReactMarkdown**: Renders AI responses with markdown formatting

## Project Structure

```
finance_ai_agent/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment configuration
│   ├── models.py               # Data models
│   ├── routes/                 # API route handlers
│   │   ├── stock.py            # Stock data endpoints
│   │   ├── news.py             # News and sentiment endpoints
│   │   └── analysis.py         # AI analysis endpoints
│   ├── services/               # Business logic
│   │   ├── stock_data.py       # Stock data fetching
│   │   ├── news_service.py     # News and sentiment analysis
│   │   ├── ai_agent.py         # OpenAI integration
│   │   └── portfolio_analyzer.py # Investment analysis logic
│   └── tests/                  # Unit tests
├── frontend/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Custom styles
│   │   └── services/
│   │       └── api.js          # Backend API client
│   ├── public/                 # Static assets
│   └── tailwind.config.js      # Tailwind configuration
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- OpenAI API key
- Finnhub API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_key
FINNHUB_API_KEY=your_finnhub_key
```

4. Start the server:
```bash
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## API Endpoints

### Stock Data
- `GET /api/stock/{ticker}` - Get stock information
- `GET /api/stock/{ticker}/history` - Get historical price data
- `GET /api/stock/{ticker}/metrics` - Get financial metrics

### News
- `GET /api/news/{ticker}` - Get company news articles
- `GET /api/news/{ticker}/sentiment` - Get news sentiment analysis
- `GET /api/news/market` - Get general market news

### AI Analysis
- `POST /api/analyze` - Get comprehensive investment analysis
- `POST /api/ask` - Ask questions about a specific stock
- `POST /api/compare` - Compare multiple stocks

## Usage

1. **Search for a stock**: Enter a ticker symbol (e.g., AAPL, TSLA, GOOGL)
2. **View stock information**: See real-time price, market cap, and key metrics
3. **Check news sentiment**: Review recent news articles with sentiment analysis
4. **Get AI analysis**: Click "Get AI Analysis" for detailed investment recommendations
5. **Ask questions**: Use the chat interface to ask specific questions about the stock
6. **Toggle theme**: Click the sun/moon icon to switch between light and dark mode