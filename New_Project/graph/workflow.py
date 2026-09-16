# graph/workflow.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from core.state import AgentState
from mcp_server.finance_api import get_fundamental_data, get_technical_data
from agents.fundamental import fundamental_analyst
from agents.technical import technical_analyst
from agents.portfolio_manager import portfolio_manager

def data_ingestion_node(state: dict) -> dict:
    """The entry node that triggers the MCP servers to fetch raw data."""
    print("--- Running Data Ingestion ---")
    ticker = state["ticker"]
    
    fundamentals = get_fundamental_data(ticker)
    if fundamentals.get("error"):
        raise ValueError(fundamentals["error"])
    technicals = get_technical_data(ticker)
    if technicals.get("error"):
        raise ValueError(technicals["error"])
    
    return {
        "financial_statements": fundamentals,
        "market_data": technicals,
        "next_agent": "fundamental_analyst"
    }

# graph/workflow.py (Update the build_graph function)

def build_graph():
    builder = StateGraph(AgentState)
    
    builder.add_node("data_ingestion", data_ingestion_node)
    builder.add_node("fundamental_analyst", fundamental_analyst)
    builder.add_node("technical_analyst", technical_analyst)
    builder.add_node("portfolio_manager", portfolio_manager)
    
    builder.add_edge(START, "data_ingestion")
    builder.add_edge("data_ingestion", "fundamental_analyst")
    builder.add_edge("fundamental_analyst", "technical_analyst")
    builder.add_edge("technical_analyst", "portfolio_manager")
    builder.add_edge("portfolio_manager", END)
    
    memory = MemorySaver()
    
    # NEW: Interrupt the graph before the final memo is generated
    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["portfolio_manager"]
    )
    
    return graph
