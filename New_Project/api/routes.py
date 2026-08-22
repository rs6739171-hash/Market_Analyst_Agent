# api/routes.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import ResearchRequest, ApprovalRequest
from graph.workflow import build_graph
import uvicorn

app = FastAPI(title="Equity Intelligence API")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Equity Intelligence API",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/research/start")
def start_research(req: ResearchRequest):
    """Initiates the data ingestion and analyst agents."""
    config = {"configurable": {"thread_id": req.thread_id}}
    initial_state = {"ticker": req.ticker, "messages": []}
    
    # Run the graph until the interrupt_before checkpoint
    for _ in graph.stream(initial_state, config=config):
        pass
        
    state = graph.get_state(config)
    
    return {
        "message": "Analysts finished. Waiting for CIO approval.",
        "fundamental_preview": state.values.get("fundamental_analysis"),
        "technical_preview": state.values.get("technical_analysis")
    }

@app.post("/api/research/approve")
def approve_research(req: ApprovalRequest):
    """Resumes the graph to generate the final memo if approved."""
    config = {"configurable": {"thread_id": req.thread_id}}
    state = graph.get_state(config)
    
    if not state.next:
        raise HTTPException(status_code=400, detail="No pending research to approve.")
        
    if req.action == "approve":
        # Passing None resumes the graph from the exact point it paused
        for _ in graph.stream(None, config=config):
            pass
            
        final_state = graph.get_state(config)
        return {"final_memo": final_state.values.get("final_memo")}
    else:
        return {"message": "Research rejected. Graph execution aborted."}

if __name__ == "__main__":
    uvicorn.run("api.routes:app", host="127.0.0.1", port=8000, reload=True)