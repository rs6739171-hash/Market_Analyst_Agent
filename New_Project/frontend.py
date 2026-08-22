import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Enterprise Equity Intelligence", page_icon="📈", layout="wide")

st.title("📈 Enterprise Equity Intelligence")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

ticker = st.text_input("Enter Ticker (e.g., AAPL, TSLA):", value="TSLA")

if st.button("Run Analyst Team"):
    if not ticker.strip():
        st.warning("Please enter a valid ticker symbol.")
    else:
        with st.spinner("Fetching data and running analysis..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/research/start", 
                    json={"ticker": ticker.upper().strip(), "thread_id": st.session_state.thread_id},
                    timeout=60
                )
                if response.status_code == 200:
                    res = response.json()
                    if "error" in str(res):
                        st.error("Invalid Ticker. Please enter a valid exchange symbol (e.g., TSLA or PERSISTENT.NS).")
                    else:
                        st.session_state.fund_preview = res.get("fundamental_preview") or "No fundamental analysis available."
                        st.session_state.tech_preview = res.get("technical_preview") or "No technical analysis available."
                else:
                    st.error(f"Backend API error ({response.status_code}): {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend API server is not running! Please start the FastAPI server first using:\n`uvicorn api.routes:app --reload --port 8000`")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

if "fund_preview" in st.session_state:
    st.subheader("HITL Checkpoint: CIO Review Required")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Fundamental Analysis**")
        st.info(st.session_state.fund_preview)
    with col2:
        st.write("**Technical Analysis**")
        st.info(st.session_state.tech_preview)
        
    if st.button("Approve & Generate Memo"):
        with st.spinner("Portfolio Manager drafting final memo..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/research/approve",
                    json={"thread_id": st.session_state.thread_id, "action": "approve"},
                    timeout=60
                )
                if response.status_code == 200:
                    res = response.json()
                    st.success("Memo Generated!")
                    st.markdown(res.get("final_memo", "No memo generated."))
                else:
                    st.error(f"Backend API error ({response.status_code}): {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend API server is not running! Please start the FastAPI server using:\n`uvicorn api.routes:app --reload --port 8000`")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")