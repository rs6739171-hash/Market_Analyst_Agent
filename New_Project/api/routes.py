import logging
import threading
from fastapi import FastAPI, HTTPException
from api.schemas import ResearchRequest, ApprovalRequest
from graph.workflow import build_graph

app = FastAPI(title="Equity Intelligence API")
graph = build_graph()
# The deployment runs one internal API process. Serialize state changes so repeated
# approval requests cannot execute the portfolio manager twice.
graph_lock = threading.Lock()
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {"status": "online", "service": "Equity Intelligence API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/research/start")
def start_research(req: ResearchRequest):
    config = {"configurable": {"thread_id": str(req.thread_id)}}
    with graph_lock:
        if graph.get_state(config).values:
            raise HTTPException(status_code=409, detail="Start new research with a new session.")
        try:
            for _ in graph.stream({"ticker": req.ticker, "messages": []}, config=config):
                pass
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="No usable market data for this ticker.") from exc
        except Exception as exc:
            logger.error("Research provider failed: %s", type(exc).__name__)
            raise HTTPException(status_code=502, detail="Market or AI provider is unavailable.") from exc
        state = graph.get_state(config)
        return {
            "message": "Analysts finished. Waiting for approval.",
            "fundamental_preview": state.values.get("fundamental_analysis"),
            "technical_preview": state.values.get("technical_analysis"),
        }


@app.post("/api/research/approve")
def approve_research(req: ApprovalRequest):
    config = {"configurable": {"thread_id": str(req.thread_id)}}
    with graph_lock:
        state = graph.get_state(config)
        if "portfolio_manager" not in state.next:
            raise HTTPException(status_code=400, detail="No pending research to approve.")
        if req.action == "reject":
            graph.update_state(config, {"next_agent": "END"}, as_node="portfolio_manager")
            return {"message": "Research rejected. Start a new analysis to continue."}
        try:
            for _ in graph.stream(None, config=config):
                pass
        except Exception as exc:
            logger.error("Memo provider failed: %s", type(exc).__name__)
            raise HTTPException(status_code=502, detail="The AI provider is unavailable.") from exc
        return {"final_memo": graph.get_state(config).values.get("final_memo")}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.routes:app", host="127.0.0.1", port=8000)
