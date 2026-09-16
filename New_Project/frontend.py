import os
import uuid
import requests
import streamlit as st
from deployment_access import require_access

st.set_page_config(page_title="Enterprise Equity Intelligence", page_icon="📈", layout="wide")
require_access()
API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
st.title("📈 Enterprise Equity Intelligence")
st.caption("AI-generated research. Market data may be delayed; verify figures before making decisions.")
if not os.getenv("OPENAI_API_KEY"):
    st.error("The analyst is awaiting its AI service configuration. Contact the owner.")
    st.stop()


def api_call(path, payload):
    try:
        response = requests.post(f"{API_URL}{path}", json=payload, timeout=(10, 240))
        if not response.ok:
            try:
                detail = response.json().get("detail", "The request could not be completed.")
            except ValueError:
                detail = "The service could not complete this request. Please try again."
            st.error(detail if isinstance(detail, str) else "Please check the ticker symbol.")
            return None
        return response.json()
    except (requests.RequestException, ValueError):
        st.error("The research service is temporarily unavailable. Please try again.")
        return None


ticker = st.text_input("Enter ticker (e.g. AAPL, TSLA, RELIANCE.NS)", value="TSLA", max_chars=24)
if st.button("Run Analyst Team", type="primary"):
    if not ticker.strip():
        st.warning("Enter a ticker symbol.")
    else:
        # Never reuse checkpoints from a previous ticker or retain a stale memo.
        for key in ("preview", "memo", "pending"):
            st.session_state.pop(key, None)
        st.session_state.thread_id = str(uuid.uuid4())
        with st.spinner("Fetching data and running analysis..."):
            result = api_call("/api/research/start", {"ticker": ticker.strip().upper(), "thread_id": st.session_state.thread_id})
        if result:
            st.session_state.preview = result
            st.session_state.pending = True

if "preview" in st.session_state:
    left, right = st.columns(2)
    with left:
        st.subheader("Fundamental analysis")
        st.markdown(st.session_state.preview.get("fundamental_preview") or "No analysis returned.")
    with right:
        st.subheader("Technical analysis")
        st.markdown(st.session_state.preview.get("technical_preview") or "No analysis returned.")

if st.session_state.get("pending"):
    approve, reject = st.columns(2)
    action = None
    with approve:
        if st.button("Approve & Generate Memo"):
            action = "approve"
    with reject:
        if st.button("Reject Research"):
            action = "reject"
    if action:
        with st.spinner("Processing your decision..."):
            result = api_call("/api/research/approve", {"thread_id": st.session_state.thread_id, "action": action})
        if result:
            st.session_state.pending = False
            st.session_state.memo = result.get("final_memo", result.get("message", ""))
            st.rerun()
if st.session_state.get("memo"):
    st.subheader("Research result")
    st.markdown(st.session_state.memo)
