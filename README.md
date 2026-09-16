[README.md](https://github.com/user-attachments/files/31331481/README.md)
# 📈 Autonomous Multi-Agent Equity & Market Intelligence Platform

An enterprise-grade, multi-agent AI system designed to autonomously aggregate market data, perform fundamental and technical analysis, and synthesize institutional-grade investment memos. 

This project simulates the workflow of an Asset Management Company (AMC) and equity research firm, featuring a Human-in-the-Loop (HITL) architecture, stateful graph orchestration, and decoupled API/UI layers.

## 🚀 Key Features

*   **Multi-Agent Orchestration:** Powered by **LangGraph**, utilizing specialized AI agents (Fundamental Analyst, Technical Analyst, and Portfolio Manager) that operate on a shared workflow state.
*   **Deterministic Data Ingestion:** Uses `yfinance` to reliably fetch real-time market data, valuation multiples, and price action, preventing LLM arithmetic hallucinations.
*   **Human-in-the-Loop (HITL) Checkpoint:** Stateful execution pauses before final memo generation, requiring Chief Investment Officer (CIO) approval via the UI before the Portfolio Manager finalizes the report.
*   **Decoupled Architecture:** A **FastAPI** backend manages the LangGraph execution and state persistence, while a **Streamlit** frontend provides a clean, interactive dashboard.
*   **High-Speed Inference:** Utilizes lightning-fast LLM reasoning via the **OpenAI API**.

## 🛠️ Tech Stack

*   **AI & Orchestration:** LangGraph, LangChain, OPenAI API
*   **Backend:** FastAPI, Uvicorn, Python 3.10+
*   **Frontend:** Streamlit, Requests
*   **Data & Finance:** `yfinance`, Pandas
*   **State Management:** LangGraph `MemorySaver`

## 📂 Project Structure

```text
equity_intelligence_platform/
├── api/
│   ├── routes.py              # FastAPI endpoints (/start, /approve)
│   └── schemas.py             # Pydantic request models
├── core/
│   ├── config.py              # Environment variables & OpenAI LLM init
│   └── state.py               # LangGraph AgentState TypedDict
├── mcp_servers/
│   └── finance_api.py         # YFinance data extraction tools
├── agents/
│   ├── fundamental.py         # Fundamental Analyst agent logic
│   ├── technical.py           # Technical Analyst agent logic
│   └── portfolio_manager.py   # Synthesis and final memo generation
├── graph/
│   └── workflow.py            # LangGraph node routing and HITL setup
├── app.py                     # Streamlit Frontend UI
├── main.py                    # Terminal execution script (optional)
├── requirements.txt           # Project dependencies
└── README.md
```



## Reviewed deployment setup

See [DEPLOYMENT_REVIEW.md](DEPLOYMENT_REVIEW.md) for the review findings, required secrets, hosting setup, verification limits, and remaining work. The Render blueprint is [render.yaml](render.yaml).
