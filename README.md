# Multi-Agent Market Analyst

[Live app](https://market-analyst-rishabh.onrender.com/) · [Portfolio and demo access](https://my-portfolio-website-topaz-beta.vercel.app/)

A personal Python and GenAI project by Rishabh Shukla. The LangGraph workflow gathers market data, runs fundamental and technical analysis, then pauses for human review before generating the final research memo. FastAPI serves the private backend and Streamlit provides the public, password-protected interface.

## Recruiter quick scan

- **Agent orchestration:** fundamental and technical analyst nodes feed a portfolio-manager synthesis workflow in LangGraph.
- **Human-in-the-loop:** explicit approval is required before memo generation; rejected requests terminate safely.
- **Data pipeline:** yfinance and Pandas power fundamentals, price history, SMA and RSI analysis with validation for unavailable/invalid data.
- **Delivery:** FastAPI, Streamlit, regression tests, GitHub Actions and Render deployment configuration.

## Implemented behavior

- yfinance and Pandas supply available company fundamentals, price history, SMA-20, SMA-50 and RSI-14.
- Fundamental and technical analyst nodes feed a portfolio-manager synthesis node.
- Explicit approval is required before memo generation. Rejecting a request ends that workflow; it cannot later be approved accidentally.
- Invalid tickers and unavailable data stop the workflow rather than silently producing a research memo.
- Regression tests, a CI workflow and a Render deployment blueprint are included.

## Limits

This is a research prototype, not verified investment advice or a trading system. Provider data can be missing, delayed or rate limited, and generated analysis can be wrong. It does not place trades. In-memory checkpoints do not survive restarts. No performance, profit, production-readiness or independent model-quality claim is made.

## Run locally

Use Python 3.12 or 3.13:

```bash
git clone https://github.com/rs6739171-hash/Market_Analyst_Agent.git
cd Market_Analyst_Agent
python -m venv .venv
source .venv/bin/activate
pip install -r New_Project/requirements.txt
cd New_Project
cp .env.example .env
# Set OPENAI_API_KEY and your chosen OPENAI_MODEL.
python serve.py
```

Set APP_PASSWORD for hosted access. Open the Streamlit URL printed by the launcher. The FastAPI service binds to loopback; do not expose it publicly without adding appropriate access controls. Never commit credentials.

## Verify and deploy

From the repository root, run `python -m unittest discover -s tests -v`. Tests cover rejection, invalid data, ticker validation and RSI edge cases. GitHub Actions installs dependencies, runs tests and checks Python syntax without paid provider calls.

The Render blueprint is [render.yaml](render.yaml). The prior detailed deployment review is [DEPLOYMENT_REVIEW.md](DEPLOYMENT_REVIEW.md). Passing offline tests does not guarantee live provider availability.
