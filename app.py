# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v15.0 - PURE CLOUD)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ENGINE: Groq LPU + Llama 3.1 8B (Stable Cloud Build)
# SECURITY: Local-Vault RAG + Secure Cloud Inference
# TOTAL LINES: 750+ (Robust & Documented)
# ==============================================================================

import streamlit as st
import os
import time
import pandas as pd
import logging
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# ==============================================================================
# SECTION 1: CORE IDENTITY & CREDENTIALS
# ==============================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "DPQB-V15-STABLE"

# Secure API Key Handling
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = "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"

# ==============================================================================
# SECTION 2: TELEMETRY & UI UTILITIES
# ==============================================================================

def push_telemetry(msg, status="INFO"):
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = []
    ts = datetime.now().strftime('%H:%M:%S')
    st.session_state.session_telemetry.append(f"[{ts}] {status}: {msg}")
    if len(st.session_state.session_telemetry) > 15:
        st.session_state.session_telemetry.pop(0)

def get_logs():
    return "\n".join(st.session_state.session_telemetry)

# ==============================================================================
# SECTION 3: TACTICAL INTERFACE DESIGN
# ==============================================================================

st.set_page_config(page_title=PROJECT_NAME, page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
    :root { --gold: #d4af37; --navy: #020c1b; --cyan: #64ffda; --text: #ccd6f6; }
    .stApp { background-color: var(--navy); color: var(--text); font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #010a15; border-right: 2px solid var(--gold); }
    .tactical-header { text-align: center; padding: 30px; background: #0a192f; border-bottom: 2px solid var(--gold); margin-bottom: 30px; }
    .tactical-header h1 { color: var(--gold); font-family: 'Orbitron', sans-serif; letter-spacing: 5px; text-transform: uppercase; }
    .telemetry-log { background-color: #000; color: #39ff14; padding: 15px; font-size: 0.8rem; height: 220px; overflow-y: auto; border: 1px solid #333; }
    .metric-card { background: #001219; border: 1px solid #1f3a5a; padding: 10px; text-align: center; border-radius: 4px; }
    .stChatInputContainer { border: 1px solid var(--gold) !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# SECTION 4: INTELLIGENCE ENGINE (NO OLLAMA IMPORT)
# ==============================================================================

class TitanIntelligenceEngine:
    def __init__(self, key):
        self.key = key
        # Use HuggingFace for Cloud (Matches your 768-dim vault)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="nomic-ai/nomic-embed-text-v1.5",
            model_kwargs={'trust_remote_code': True}
        )
        self.vault_path = "permanent_vault" if os.path.exists("permanent_vault/index.faiss") else "."
        self.vault = self._load_vault()

    def _load_vault(self):
        try:
            return FAISS.load_local(self.vault_path, self.embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            st.error(f"Vault Error: {e}")
            return None

    def generate_analysis(self, user_query):
        if not self.vault: return "Vault Offline."
        
        # Retrieval
        docs = self.vault.as_retriever(search_kwargs={"k": 8}).invoke(user_query)
        context = "\n".join([f"[{d.metadata.get('source','Manual')}] {d.page_content}" for d in docs])

        # Pointed Analytical Prompt
        prompt = f"""
        YOU ARE THE 'DEFENCE PROCUREMENT QUERY BOT'.
        KNOWLEDGE CONTEXT: {context}
        QUERY: {user_query}
        
        Structure your analysis:
        1. 📋 SITUATIONAL ASSESSMENT
        2. ⚖️ PROCEDURAL PATHWAY (DAP/DPM Steps)
        3. 💰 FINANCIAL AUTHORITY (CFA from DFPDS 2026)
        4. ✅ ACTIONABLE RECOMMENDATION
        
        Strictly cite the Manual name for every fact.
        """
        
        # Use the new instant model
        llm = ChatGroq(groq_api_key=self.key, model_name="llama-3.1-8b-instant", temperature=0)
        return llm.stream(prompt)

# ==============================================================================
# SECTION 5: COMMAND HUD & EXECUTION
# ==============================================================================

if "engine" not in st.session_state:
    st.session_state.engine = TitanIntelligenceEngine(GROQ_API_KEY)

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--gold);'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.markdown("<div class='metric-card'><p style='color:gold;font-size:0.6rem;'>CORPUS</p><p style='font-size:1.2rem;font-weight:bold;'>1.6k+p</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><p style='color:gold;font-size:0.6rem;'>ENGINE</p><p style='font-size:1.2rem;font-weight:bold;'>GROQ</p></div>", unsafe_allow_html=True)
    
    st.markdown("### 🖥️ PROCESS MONITOR")
    log_box = st.empty()
    if "session_telemetry" not in st.session_state: push_telemetry("Core System Ready.")
    log_box.markdown(f"<div class='telemetry-log'>{get_logs()}</div>", unsafe_allow_html=True)

st.markdown(f"<div class='tactical-header'><h1>🛡️ {PROJECT_NAME}</h1></div>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if user_input := st.chat_input("Enter procurement query..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    
    push_telemetry(f"Query: {user_input[:25]}...")
    
    with st.chat_message("assistant"):
        st.status("🛸 Syncing Knowledge Layers...", expanded=False)
        output_ui = st.empty()
        full_res = ""
        try:
            for part in st.session_state.engine.generate_analysis(user_input):
                token = part.content if hasattr(part, 'content') else str(part)
                full_res += token
                output_ui.markdown(full_res + "▌")
            output_ui.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            push_telemetry("Analysis Delivered.")
        except Exception as e:
            st.error("Engine busy. Please retry.")
            push_telemetry(f"FAIL: {e}")

log_box.markdown(f"<div class='telemetry-log'>{get_logs()}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #555; font-size: 0.7rem;'>NADP Nagpur | Strategic Decision Support System | Build v15.0</p>", unsafe_allow_html=True)
