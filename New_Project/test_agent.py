# test_agents.py
from agents.fundamental import fundamental_analyst
from agents.technical import technical_analyst
from mcp_server.finance_api import get_fundamental_data, get_technical_data

def test_single_agent_execution():
    ticker = "RELIANCE.NS" # Or any ticker you prefer (e.g., "AAPL")
    
    # 1. Manually fetch the data (simulating the MCP step)
    fundamentals = get_fundamental_data(ticker)
    technicals = get_technical_data(ticker)
    
    # 2. Construct a mock LangGraph State
    mock_state = {
        "ticker": ticker,
        "financial_statements": fundamentals,
        "market_data": technicals,
        "messages": []
    }
    
    # 3. Test Fundamental Agent
    new_state_fund = fundamental_analyst(mock_state)
    print("\n=== FUNDAMENTAL ANALYSIS ===")
    print(new_state_fund["fundamental_analysis"])
    
    # 4. Test Technical Agent
    new_state_tech = technical_analyst(mock_state)
    print("\n=== TECHNICAL ANALYSIS ===")
    print(new_state_tech["technical_analysis"])

if __name__ == "__main__":
    test_single_agent_execution()