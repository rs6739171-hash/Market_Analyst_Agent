from langchain_core.prompts import ChatPromptTemplate
# pyrefly: ignore [missing-import]
from core.config import get_llm
import json

def fundamental_analyst(state:dict)->dict:
    """Analyzes financial health, valuation ratios, and instituional trends"""
    print("---Running Fundamental Analyst---")

    ticker = state.get("ticker","Unknown")
    fundamentals = state.get("financial_statements") or state.get("fundamental_statements") or {}

    # Initialize the GROQ model
    llm = get_llm(temperature=0.1)

    # Define the expert system prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Tier-1 Equity Research Fundamental Analyst. 
        Use only the supplied data. Explicitly identify missing or stale data; never invent metrics, prices, or historical comparisons. Your job is to analyze the provided financial data and generate a comprehensive fundamental thesis.
        
        Focus your analysis on:
        1. Valuation Multiples (P/E, Forward P/E, P/B) vs. historical/sector averages.
        2. Profitability and Margin expansion (Gross, Operating, ROE, ROA).
        3. Balance Sheet Health (Debt-to-Equity, Current Ratio, Free Cash Flow).
        4. Institutional Activity cues (e.g., if FII/DII data or strong volume suggests accumulation/distribution).
        
        Provide a structured, 3-4 paragraph thesis detailing the company's financial health and intrinsic value potential. Be highly quantitative."""),
        ("user", "Analyze the following data for {ticker}:\n\n{fundamentals}")
    ])

    chain = prompt| llm

    #Convert dictionary to Json string for a llm to read easily
    data_str = json.dumps(fundamentals,indent=2)
    response = chain.invoke({"ticker":ticker,"fundamentals":data_str})

    # Return the dictionary to update the Lnaggraph State
    return {"fundamental_analysis": response.content, "next_agent": "technical_analyst"}
