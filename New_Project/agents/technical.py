# agents/technical.py
from langchain_core.prompts import ChatPromptTemplate
from core.config import get_llm
import json

def technical_analyst(state: dict) -> dict:
    """Analyzes price action, moving averages, momentum, and volume profiles."""
    print("--- Running Technical Analyst ---")
    
    ticker = state.get("ticker", "Unknown")
    technicals = state.get("market_data", {})
    
    llm = get_llm(temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a highly experienced Technical Analyst and swing trader.
        Use only supplied data and identify missing indicators. Review the provided technical market data and generate a strict technical outlook.
        
        Focus your analysis on:
        1. Trend Analysis: Compare Current Price against the 20-day and 50-day Simple Moving Averages (SMA).
        2. Momentum & Mean Reversion: Analyze the 14-day RSI (oversold < 30, overbought > 70).
        3. Support & Resistance: Factor in the 52-week highs and lows.
        4. Volume Profile: Note any significant volume spikes that confirm the current trend.
        
        Provide a concise, 2-3 paragraph analysis. Conclude with specific hypothetical support and resistance levels to watch, and state whether the chart is Bullish, Bearish, or Neutral."""),
        ("user", "Analyze the following technical data for {ticker}:\n\n{technicals}")
    ])
    
    chain = prompt | llm
    
    data_str = json.dumps(technicals, indent=2)
    response = chain.invoke({"ticker": ticker, "technicals": data_str})
    
    return {"technical_analysis": response.content, "next_agent": "portfolio_manager"}
