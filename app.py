# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v9.5 PRO)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ENGINE: Groq LPU + Llama 3.1 70B (Ultra-Intelligence Architecture)
# SECURITY: Strategic Local-Vault RAG + Cloud Inference
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
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==============================================================================
# SECTION 1: CORE IDENTITY & CREDENTIALS
# ==============================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "DPQB-TITAN-X-PRO"
# Secure key retrieval from Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # Fallback for local testing
    GROQ_API_KEY = "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"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TITAN_CORE")

# ==============================================================================
# SECTION 2: GLOBAL UTILITIES (FIXED SCOPE)
# ==============================================================================

def push_telemetry(msg):
    """Pushes real-time events to the session telemetry log"""
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = []
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.session_telemetry.append(f"[{timestamp}] {msg}")

# ==============================================================================
# SECTION 3: TACTICAL INTERFACE DESIGN (CSS)
# ==============================================================================

st.set_page_config(page_title=PROJECT_NAME, page_icon="🛡️", layout="wide")

def apply_enhanced_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
        :root { --gold: #d4af37; --navy-deep: #020c1b; --cyan: #64ffda; --text: #ccd6f6; }
        .stApp { background-color: var(--navy-deep); color: var(--text); font-family: 'JetBrains Mono', monospace; }
        [data-testid="stSidebar"] { background-color: #010a15; border-right: 2px solid var(--gold); }
        .tactical-header { text-align: center; padding: 40px; background: #0a192f; border-bottom: 3px double var(--gold); margin-bottom: 50px; }
        .tactical-header h1 { color: var(--gold); font-family: 'Orbitron', sans-serif; letter-spacing: 8px; text-transform: uppercase; }
        .analysis-card { background-color: #112240; border: 1px solid var(--cyan); padding: 25px; border-radius: 4px; border-left: 8px solid var(--gold); margin-bottom: 30px; }
        .telemetry-log { background-color: #000; color: #39ff14; padding: 15px; font-size: 0.8rem; height: 250px; overflow-y: auto; border: 1px solid #333; font-family: 'Courier New', monospace; }
        .metric-card { background: #001219; border: 1px solid #1f3a5a; padding: 15px; text-align: center; border-radius: 4px; }
        .stChatInputContainer { border: 1px solid var(--gold) !important; }
        </style>
    """, unsafe_allow_html=True)

apply_enhanced_styles()

# ==============================================================================
# SECTION 4: KNOWLEDGE ARCHITECTURE
# ==============================================================================

class TitanIntelligenceEngine:
    def __init__(self, key):
        self.key = key
        # Model for reading the Vault
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vault_path = "." # Set to dot since vault files are in root on GitHub
        self.vault = self._load_vault()

    def _load_vault(self):
        if os.path.exists("index.faiss"):
            try:
                return FAISS.load_local(self.vault_path, self.embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                st.error(f"Vault Error: {e}")
                return None
        return None

    def synthesize_consultation(self, user_query):
        if not self.vault: return "Vault Offline."
        
        # 1. Broad Retrieval
        docs = self.vault.as_retriever(search_kwargs={"k": 12}).invoke(user_query)
        context = "\n".join([f"[{d.metadata.get('source','Manual')}] {d.page_content}" for d in docs])

        # 2. Master System Directive
        prompt = f"""
        YOU ARE THE 'DEFENCE PROCUREMENT QUERY BOT'. 
        GOAL: Provide a Pointed, Authoritative 360-degree Analysis.

        KNOWLEDGE BASE:
        {context}

        QUERY: {user_query}

        STRUCTURE:
        1. 📋 EXECUTIVE SUMMARY: Category fit (Capital/Revenue) & TPCR alignment.
        2. ⚖️ PROCEDURAL PATHWAY: Detailed rules from DAP/DPM & Handbook steps.
        3. 💰 FINANCIAL POWER (DFPDS): Identify CFA & specific financial limit.
        4. 🛡️ AUDIT & RISK COMPLIANCE: Warning on potential hurdles.
        5. ✅ ACTIONABLE SOLUTION: 3-step roadmap.

        CITE MANUAL NAMES FOR EVERY FACT.
        """
        
        llm = ChatGroq(groq_api_key=self.key, model_name="llama-3.1-70b-versatile", temperature=0)
        return llm.stream(prompt)

# ==============================================================================
# SECTION 5: UI EXECUTION
# ==============================================================================

engine = TitanIntelligenceEngine(GROQ_API_KEY)

# Sidebar HUD
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.markdown("<div class='metric-card'><p style='color:grey;font-size:0.7rem;'>PAGES</p><p style='font-size:1.2rem;font-weight:bold;'>1,691</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><p style='color:grey;font-size:0.7rem;'>BRAIN</p><p style='font-size:1.2rem;font-weight:bold;'>70B</p></div>", unsafe_allow_html=True)
    
    st.markdown("### 🖥️ PROCESS LOG")
    log_placeholder = st.empty()
    
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = [f"[{datetime.now().strftime('%H:%M:%S')}] Neural Core Ready."]

    # Refresh visual log
    log_placeholder.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry[-12:])}</div>", unsafe_allow_html=True)

    if st.button("Purge Cache"):
        st.session_state.messages = []
        st.session_state.session_telemetry = []
        st.rerun()

st.markdown(f"<div class='tactical-header'><h1>🛡️ {PROJECT_NAME}</h1></div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if user_input := st.chat_input("Enter procurement query..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    
    push_telemetry(f"Query: {user_input[:30]}...")

    with st.chat_message("assistant"):
        with st.status("🛸 Accessing Defence Knowledge Layers...", expanded=False):
            st.write("Mining context from DAP/DPM/DFPDS...")
            time.sleep(0.4)
        
        output_ui = st.empty()
        full_res = ""
        try:
            for part in engine.synthesize_consultation(user_input):
                full_res += part.content
                output_ui.markdown(full_res + "▌")
            output_ui.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            push_telemetry("Analysis Delivered.")
        except Exception as e:
            st.error(f"Inference Timeout. Please retry.")
            push_telemetry(f"ERROR: {str(e)}")

# Log refresh at end of run
log_placeholder.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry[-12:])}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #555; font-size: 0.7rem;'>Proprietary Tool | NADP Nagpur | Capstone 2025-26 | DPQB Build v9.5</p>", unsafe_allow_html=True)
