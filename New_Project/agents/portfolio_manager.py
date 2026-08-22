# agents/portfolio_manager.py
from langchain_core.prompts import ChatPromptTemplate
from core.config import get_llm

def portfolio_manager(state: dict) -> dict:
    """Synthesizes analyst reports and generates the final investment memo."""
    print("--- Running Portfolio Manager ---")
    
    ticker = state.get("ticker", "Unknown")
    fundamental_analysis = state.get("fundamental_analysis", "No fundamental data provided.")
    technical_analysis = state.get("technical_analysis", "No technical data provided.")
    
    llm = get_llm(temperature=0.2) # Slightly higher temperature for better narrative flow
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Lead Portfolio Manager at a top-tier Asset Management Company.
        Your job is to read the reports from your Fundamental and Technical analysts and draft a final Investment Memo.
        
        Your memo must include:
        1. Executive Summary: A one-paragraph definitive stance (Buy, Hold, or Sell).
        2. Fundamental Synthesis: The core value drivers and risks.
        3. Technical Alignment: How the price action aligns (or misaligns) with the fundamentals.
        4. Actionable Execution Plan: Target entry prices, stop-loss levels, and time horizon.
        
        Write in a highly professional, institutional tone."""),
        ("user", """Generate the final investment memo for {ticker} based on the following analyst reports:
        
        FUNDAMENTAL ANALYSIS:
        {fundamental}
        
        TECHNICAL ANALYSIS:
        {technical}""")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "ticker": ticker,
        "fundamental": fundamental_analysis,
        "technical": technical_analysis
    })
    
    return {"final_memo": response.content, "next_agent": "END"}