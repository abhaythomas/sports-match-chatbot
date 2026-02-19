import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("Sports Match Chatbot (MVP)")

# Show backend status clearly
try:
    health = requests.get(f"{API}/health", timeout=2).json()
    st.success(f"Backend connected ✅ ({health.get('time_utc','')})")
except Exception as e:
    st.error(f"Backend not reachable at {API}. Is uvicorn running? Error: {e}")
    st.stop()

league = st.selectbox("League", ["Bundesliga"])

col1, col2 = st.columns(2)

with col1:
    if st.button("Show live matches"):
        try:
            matches = requests.get(f"{API}/matches/live", params={"league": league}, timeout=5).json()
            st.write(matches)
        except Exception as e:
            st.error(f"Failed to fetch live matches: {e}")

with col2:
    if st.button("Show today's matches"):
        try:
            matches = requests.get(f"{API}/matches/today", params={"league": league}, timeout=5).json()
            st.write(matches)
        except Exception as e:
            st.error(f"Failed to fetch today's matches: {e}")

st.divider()
match_id = st.text_input("Match ID", value="2")

c1, c2 = st.columns(2)
with c1:
    if st.button("Preview"):
        try:
            out = requests.get(f"{API}/match/{match_id}/preview", timeout=5).json()
            st.subheader("Preview")
            st.code(out.get("preview", str(out)))
        except Exception as e:
            st.error(f"Failed to generate preview: {e}")

with c2:
    if st.button("Summary"):
        try:
            out = requests.get(f"{API}/match/{match_id}/summary", timeout=5).json()
            st.subheader("Summary")
            st.code(out.get("summary", str(out)))
        except Exception as e:
            st.error(f"Failed to generate summary: {e}")
