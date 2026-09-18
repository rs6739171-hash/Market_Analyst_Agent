import yfinance as yf
import pandas as pd
from typing import Dict, Any

def get_fundamental_data(ticker: str) -> Dict[str, Any]:
    """Fetches key valuation metrics, balance sheet items, and profitability ratios."""
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # NEW: Check if the ticker actually exists by looking for basic info
    if "shortName" not in info:
        return {"error": f"Ticker '{ticker}' not found. Please use a valid Yahoo Finance ticker symbol."}
    
    return {
        "ticker": ticker,
        "company_name": info.get("shortName", "N/A"),
        # ... (rest of your dictionary)
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "pb_ratio": info.get("priceToBook"),
        "debt_to_equity": info.get("debtToEquity"),
        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAssets"),
        "revenue_growth": info.get("revenueGrowth"),
        "gross_margins": info.get("grossMargins"),
        "operating_margins": info.get("operatingMargins"),
        "free_cash_flow": info.get("freeCashflow"),
        "current_ratio": info.get("currentRatio")       
    }

def get_technical_data(ticker:str,period:str="6mo")->Dict[str,Any]:
    "Fetches historical OHLCV data and calculates technical momentum indicators."
    stock=yf.Ticker(ticker)
    hist= stock.history(period = period)

    if hist.empty:
        return{"error": f"No historical data found for {ticker}"}
    # Calculate simple moving average
    hist["SMA_20"] = hist["Close"].rolling(window=20).mean()
    hist["SMA_50"] = hist["Close"].rolling(window=50).mean()
    
    # Calculate 14 day RSI
    delta = hist["Close"].diff()
    gain = (delta.where(delta>0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta<0,0)).rolling(window=14).mean()
    rs = gain/loss
    hist["RSI_14"] = 100-(100/(1+rs))
    # Flat series is neutral; an all-gain series is overbought, all-loss is oversold.
    hist.loc[(gain == 0) & (loss == 0), "RSI_14"] = 50.0
    latest = hist.iloc[-1]
    prev_close = hist["Close"].iloc[-2] if len(hist)>1 else latest["Close"]

    return {
        "ticker": ticker,
        "current_price": round(float(latest["Close"]), 2),
        "previous_close": round(float(prev_close), 2),
        "sma_20": round(float(latest["SMA_20"]), 2) if pd.notna(latest["SMA_20"]) else None,
        "sma_50": round(float(latest["SMA_50"]), 2) if pd.notna(latest["SMA_50"]) else None,
        "rsi_14": round(float(latest["RSI_14"]), 2) if pd.notna(latest["RSI_14"]) else None,
        "volume": int(latest["Volume"]),
        "52_week_high": info_high if (info_high := stock.info.get("fiftyTwoWeekHigh")) else round(float(hist["High"].max()), 2),
        "52_week_low": info_low if (info_low := stock.info.get("fiftyTwoWeekLow")) else round(float(hist["Low"].min()), 2),
    }
