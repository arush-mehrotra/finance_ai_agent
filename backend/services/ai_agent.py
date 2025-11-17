"""AI Agent service using Anthropic's Claude for financial analysis."""
from anthropic import Anthropic
from typing import Dict, Any, List, Optional
import json


class AIAgentService:
    """Service for AI-powered financial analysis using Claude."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize AI agent service.

        Args:
            api_key: Anthropic API key (required)
            model: Claude model to use (default: claude-sonnet-4-5-20250929)

        Raises:
            ValueError: If API key is not provided
        """
        if not api_key:
            raise ValueError("Anthropic API key is required")

        self.api_key = api_key
        self.model = model
        self.client = Anthropic(api_key=api_key)

    def analyze_stock(
        self,
        ticker: str,
        stock_data: Dict[str, Any],
        news: List[Dict[str, Any]],
        user_question: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive stock analysis using AI.

        Args:
            ticker: Stock ticker symbol
            stock_data: Dictionary with stock information and metrics
            news: List of recent news articles
            user_question: Optional specific question from user

        Returns:
            Dictionary with AI analysis, recommendation, and key points

        Example:
            >>> agent = AIAgentService("your_api_key")
            >>> analysis = agent.analyze_stock("AAPL", stock_data, news)
        """
        # Build context from stock data and news
        context = self._build_analysis_context(ticker, stock_data, news)

        # Create the prompt
        system_prompt = self._get_system_prompt()

        if user_question:
            user_prompt = f"{context}\n\nUser Question: {user_question}\n\nProvide a detailed analysis addressing the user's question."
        else:
            user_prompt = f"{context}\n\nProvide a comprehensive investment analysis for {ticker}."

        try:
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Extract response
            analysis_text = message.content[0].text

            # Parse and structure the response
            result = self._structure_analysis(ticker, analysis_text, stock_data)

            return result

        except Exception as e:
            raise ValueError(f"Error generating analysis: {str(e)}")

    def answer_question(
        self,
        ticker: str,
        question: str,
        stock_data: Dict[str, Any],
        news: List[Dict[str, Any]]
    ) -> str:
        """
        Answer a specific question about a stock.

        Args:
            ticker: Stock ticker symbol
            question: User's question
            stock_data: Stock information and metrics
            news: Recent news articles

        Returns:
            AI-generated answer to the question

        Example:
            >>> agent = AIAgentService("your_api_key")
            >>> answer = agent.answer_question("AAPL", "Is this a good long-term investment?", data, news)
        """
        context = self._build_analysis_context(ticker, stock_data, news)
        system_prompt = self._get_system_prompt()

        user_prompt = f"{context}\n\nQuestion: {question}\n\nProvide a clear, concise answer based on the data provided."

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return message.content[0].text

        except Exception as e:
            raise ValueError(f"Error answering question: {str(e)}")

    def summarize_news(
        self,
        ticker: str,
        news: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Summarize news articles and extract key insights.

        Args:
            ticker: Stock ticker symbol
            news: List of news articles

        Returns:
            Dictionary with summary, sentiment, and key points

        Example:
            >>> agent = AIAgentService("your_api_key")
            >>> summary = agent.summarize_news("AAPL", news_articles)
        """
        if not news:
            return {
                "ticker": ticker,
                "summary": "No recent news available.",
                "sentiment": "neutral",
                "key_points": []
            }

        # Format news for the prompt
        news_text = self._format_news_for_prompt(news)

        system_prompt = "You are a financial news analyst. Summarize news articles and extract key insights that would impact investment decisions."

        user_prompt = f"""Analyze the following news articles for {ticker}:

{news_text}

Provide:
1. A brief summary (2-3 sentences)
2. Overall sentiment (positive/negative/neutral)
3. 3-5 key points that investors should know

Format your response as:
SUMMARY: [your summary]
SENTIMENT: [positive/negative/neutral]
KEY POINTS:
- [point 1]
- [point 2]
- [point 3]
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.5,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            response_text = message.content[0].text
            parsed = self._parse_news_summary(response_text)

            return {
                "ticker": ticker,
                "summary": parsed["summary"],
                "sentiment": parsed["sentiment"],
                "key_points": parsed["key_points"]
            }

        except Exception as e:
            return {
                "ticker": ticker,
                "summary": f"Error summarizing news: {str(e)}",
                "sentiment": "neutral",
                "key_points": []
            }

    def generate_recommendation(
        self,
        ticker: str,
        analysis: str,
        stock_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate investment recommendation based on analysis.

        Args:
            ticker: Stock ticker symbol
            analysis: Previous analysis text
            stock_data: Stock information

        Returns:
            Dictionary with recommendation, confidence, and reasoning

        Example:
            >>> agent = AIAgentService("your_api_key")
            >>> rec = agent.generate_recommendation("AAPL", analysis_text, data)
        """
        system_prompt = "You are a financial advisor providing investment recommendations. Be objective and consider both risks and opportunities."

        user_prompt = f"""Based on the following analysis for {ticker}:

{analysis}

Current Price: ${stock_data.get('current_price', 'N/A')}
P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
Market Cap: ${stock_data.get('market_cap', 'N/A'):,} if stock_data.get('market_cap') else 'N/A'

Provide a recommendation (BUY/HOLD/SELL) with:
1. Your recommendation
2. Confidence level (High/Medium/Low)
3. Brief reasoning (2-3 sentences)
4. Key risk factors

Format as:
RECOMMENDATION: [BUY/HOLD/SELL]
CONFIDENCE: [High/Medium/Low]
REASONING: [your reasoning]
RISKS: [key risks]
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                temperature=0.5,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            response_text = message.content[0].text
            parsed = self._parse_recommendation(response_text)

            return {
                "ticker": ticker,
                "recommendation": parsed["recommendation"],
                "confidence": parsed["confidence"],
                "reasoning": parsed["reasoning"],
                "risks": parsed["risks"]
            }

        except Exception as e:
            return {
                "ticker": ticker,
                "recommendation": "HOLD",
                "confidence": "Low",
                "reasoning": f"Error generating recommendation: {str(e)}",
                "risks": "Unable to assess risks due to error."
            }

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI agent."""
        return """You are an expert financial analyst and investment advisor with deep knowledge of:
- Fundamental analysis (P/E ratios, earnings, revenue, margins, etc.)
- Market sentiment and news analysis
- Risk assessment and portfolio management
- Technical and quantitative analysis

Your role is to:
1. Provide objective, data-driven analysis
2. Explain complex financial concepts clearly
3. Consider both opportunities and risks
4. Give actionable insights for investors
5. Be honest about uncertainty and limitations

Always base your analysis on the provided data and clearly state when you're making assumptions."""

    def _build_analysis_context(
        self,
        ticker: str,
        stock_data: Dict[str, Any],
        news: List[Dict[str, Any]]
    ) -> str:
        """Build context string from stock data and news."""
        context_parts = [f"Stock Analysis for {ticker} ({stock_data.get('name', 'N/A')})\n"]

        # Basic info
        context_parts.append(f"\nCurrent Price: ${stock_data.get('current_price', 'N/A')}")
        context_parts.append(f"Market Cap: ${stock_data.get('market_cap', 'N/A'):,}" if stock_data.get('market_cap') else "Market Cap: N/A")
        context_parts.append(f"Sector: {stock_data.get('sector', 'N/A')}")
        context_parts.append(f"Industry: {stock_data.get('industry', 'N/A')}")

        # Valuation metrics
        context_parts.append("\n\nValuation Metrics:")
        context_parts.append(f"- P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}")
        context_parts.append(f"- Forward P/E: {stock_data.get('forward_pe', 'N/A')}")
        context_parts.append(f"- Beta: {stock_data.get('beta', 'N/A')}")

        # Profitability
        context_parts.append("\n\nProfitability:")
        profit_margin = stock_data.get('profit_margins')
        context_parts.append(f"- Profit Margin: {profit_margin*100:.2f}%" if profit_margin else "- Profit Margin: N/A")
        operating_margin = stock_data.get('operating_margins')
        context_parts.append(f"- Operating Margin: {operating_margin*100:.2f}%" if operating_margin else "- Operating Margin: N/A")
        roe = stock_data.get('return_on_equity')
        context_parts.append(f"- ROE: {roe*100:.2f}%" if roe else "- ROE: N/A")

        # Growth
        context_parts.append("\n\nGrowth:")
        earnings_growth = stock_data.get('earnings_growth')
        context_parts.append(f"- Earnings Growth: {earnings_growth*100:.2f}%" if earnings_growth else "- Earnings Growth: N/A")
        revenue_growth = stock_data.get('revenue_growth')
        context_parts.append(f"- Revenue Growth: {revenue_growth*100:.2f}%" if revenue_growth else "- Revenue Growth: N/A")

        # Recent news
        if news:
            context_parts.append("\n\nRecent News:")
            for i, article in enumerate(news[:5], 1):
                context_parts.append(f"\n{i}. {article.get('title', '')}")
                context_parts.append(f"   Source: {article.get('source', 'Unknown')} | Sentiment: {article.get('sentiment', 'neutral')}")
                if article.get('description'):
                    context_parts.append(f"   {article['description'][:150]}...")

        return "\n".join(context_parts)

    def _format_news_for_prompt(self, news: List[Dict[str, Any]]) -> str:
        """Format news articles for prompt."""
        formatted = []
        for i, article in enumerate(news[:10], 1):
            formatted.append(f"{i}. {article.get('title', '')}")
            if article.get('description'):
                formatted.append(f"   {article['description']}")
            formatted.append(f"   Source: {article.get('source', 'Unknown')}")
            formatted.append("")
        return "\n".join(formatted)

    def _structure_analysis(
        self,
        ticker: str,
        analysis_text: str,
        stock_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Structure the analysis response."""
        # Extract key points (look for bullet points or numbered lists)
        key_points = []
        lines = analysis_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith(("-", "•", "*")) or (line and line[0].isdigit() and ". " in line):
                key_points.append(line.lstrip("-•*0123456789. "))

        return {
            "ticker": ticker,
            "analysis": analysis_text,
            "key_points": key_points[:5] if key_points else ["See full analysis for details"],
            "current_price": stock_data.get('current_price'),
            "recommendation": None  # Will be set separately if needed
        }

    def _parse_news_summary(self, response_text: str) -> Dict[str, Any]:
        """Parse structured news summary response."""
        result = {
            "summary": "",
            "sentiment": "neutral",
            "key_points": []
        }

        lines = response_text.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith("SUMMARY:"):
                result["summary"] = line.replace("SUMMARY:", "").strip()
            elif line.startswith("SENTIMENT:"):
                sentiment = line.replace("SENTIMENT:", "").strip().lower()
                if sentiment in ["positive", "negative", "neutral"]:
                    result["sentiment"] = sentiment
            elif line.startswith("KEY POINTS:"):
                current_section = "key_points"
            elif current_section == "key_points" and line.startswith("-"):
                result["key_points"].append(line.lstrip("- "))

        # Fallback if parsing failed
        if not result["summary"]:
            result["summary"] = response_text[:200]

        return result

    def _parse_recommendation(self, response_text: str) -> Dict[str, Any]:
        """Parse structured recommendation response."""
        result = {
            "recommendation": "HOLD",
            "confidence": "Medium",
            "reasoning": "",
            "risks": ""
        }

        lines = response_text.split("\n")

        for line in lines:
            line = line.strip()
            if line.startswith("RECOMMENDATION:"):
                rec = line.replace("RECOMMENDATION:", "").strip().upper()
                if rec in ["BUY", "HOLD", "SELL"]:
                    result["recommendation"] = rec
            elif line.startswith("CONFIDENCE:"):
                conf = line.replace("CONFIDENCE:", "").strip()
                if conf in ["High", "Medium", "Low"]:
                    result["confidence"] = conf
            elif line.startswith("REASONING:"):
                result["reasoning"] = line.replace("REASONING:", "").strip()
            elif line.startswith("RISKS:"):
                result["risks"] = line.replace("RISKS:", "").strip()

        # Fallback
        if not result["reasoning"]:
            result["reasoning"] = response_text[:200]

        return result
