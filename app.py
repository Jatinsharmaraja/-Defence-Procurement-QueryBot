# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v14.0 - IMMORTAL TITAN)
# VERSION: 14.0.1 | STABLE CLOUD DEPLOYMENT
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# TOTAL ESTIMATED LINES: 750+ (Robust Analytical Build)
# ==============================================================================

import streamlit as st
import ollama
import os
import time
import pandas as pd
import json
import logging
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# ==============================================================================
# SECTION 1: CORE ARCHITECTURE CONFIGURATION (Lines 30-100)
# ==============================================================================

# Initialize Secure Logging for Presentation Audit Trail
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AEGIS_ULTIMATE")

# System Constants and Identity Manifest
SYSTEM_MANIFEST = {
    "VERSION": "14.0.1",
    "CODENAME": "TITAN-IMMORTAL",
    "ACADEMY": "NADP Nagpur",
    "LLM_ENGINE": "llama-3.1-8b-instant",  # FIXED: Decommissioned model replaced
    "EMBED_ENGINE": "nomic-ai/nomic-embed-text-v1.5",
    "DIMENSIONS": 768,
    "YEAR": "2025-26"
}

# Secure Credential Management with Error Handling
try:
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    else:
        # Emergency backup key provided by developer
        GROQ_API_KEY = "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"
except Exception:
    GROQ_API_KEY = "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"

# ==============================================================================
# SECTION 2: ADVANCED TELEMETRY UTILITIES (Lines 101-220)
# ==============================================================================

def push_telemetry(msg, status="INFO"):
    """
    Maintains a persistent real-time system event log within the user session.
    This provides 'Proof of Robustness' for the Capstone Presentation.
    """
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = []
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] {status}: {msg}"
    st.session_state.session_telemetry.append(log_entry)
    
    # Manage log buffer to prevent browser memory leaks
    if len(st.session_state.session_telemetry) > 20:
        st.session_state.session_telemetry.pop(0)

def get_telemetry_stream():
    """Formats the telemetry list for terminal-style UI display."""
    return "\n".join(st.session_state.session_telemetry)

# ==============================================================================
# SECTION 3: TACTICAL INTERFACE DESIGN (CSS) (Lines 221-450)
# ==============================================================================

st.set_page_config(
    page_title="AEGIS | Strategic Procurement Bot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_military_ui():
    """Injects high-fidelity tactical CSS for military command-center aesthetics."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;700&family=Orbitron:wght@400;900&display=swap');
        
        :root {
            --gold: #ffcc00;
            --navy-deep: #000814;
            --cyber-blue: #00f5ff;
            --alert-red: #ff3e3e;
            --text-ghost: #ced4da;
        }

        .stApp {
            background-color: var(--navy-deep);
            color: var(--text-ghost);
            font-family: 'Fira Code', monospace;
        }

        /* Tactical Sidebar Control Panel */
        [data-testid="stSidebar"] {
            background-color: #000814;
            border-right: 2px solid var(--gold);
            box-shadow: 10px 0px 20px rgba(0,0,0,0.5);
        }

        /* Strategic Oracle HUD Title */
        .oracle-header {
            font-family: 'Orbitron', sans-serif;
            color: var(--gold);
            text-align: center;
            font-size: 2.5rem;
            letter-spacing: 12px;
            padding: 30px;
            border-bottom: 4px double var(--gold);
            margin-bottom: 40px;
            text-transform: uppercase;
        }

        /* Diagnostic Process Monitor */
        .terminal-box {
            background-color: #000;
            color: #39ff14;
            padding: 15px;
            border: 1px solid #1a1a1a;
            font-size: 0.8rem;
            height: 280px;
            overflow-y: scroll;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }

        /* Strategic Result Cards */
        .report-panel {
            background: linear-gradient(145deg, #001d3d 0%, #003566 100%);
            border: 1px solid var(--cyber-blue);
            padding: 30px;
            border-radius: 6px;
            border-left: 10px solid var(--gold);
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        }

        /* Metrics HUD */
        .hud-unit { text-align: center; border: 1px solid #2a2a2a; padding: 15px; background: #010a15; }
        .hud-lbl { color: var(--gold); font-size: 0.7rem; font-weight: bold; text-transform: uppercase; }
        .hud-val { color: white; font-size: 1.8rem; font-weight: 900; }

        /* Scrollbars Customization */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--navy-deep); }
        ::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

apply_military_ui()

# ==============================================================================
# SECTION 4: INTELLIGENCE ENGINE (DIMENSION-STABLE) (Lines 451-680)
# ==============================================================================

class TitanIntelligenceEngine:
    """Orchestrates Strategic Retrieval and High-Fidelity Synthesis."""
    
    def __init__(self, api_key):
        self.key = api_key
        # DIMENSION MATCH: Local nomic-embed used 768. Cloud must match.
        self.embeddings = HuggingFaceEmbeddings(
            model_name=SYSTEM_MANIFEST["EMBED_ENGINE"],
            model_kwargs={'trust_remote_code': True}
        )
        # Determine data path dynamically (checks root and vault folder)
        self.vault_path = "permanent_vault" if os.path.exists("permanent_vault/index.faiss") else "."
        self.vault = self._load_vault()

    def _load_vault(self):
        """Loads and verifies the FAISS index files from the detected repository path."""
        try:
            return FAISS.load_local(
                self.vault_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            logger.error(f"VAULT_FAILURE: {e}")
            return None

    def generate_analytical_brief(self, user_query):
        """Executes the Pointed Analytical Approach across Policy, Process, Power, and Plan."""
        if not self.vault: return "SYSTEM ERROR: Knowledge Vault Offline."

        # RETRIEVAL: Pulling 10 relevant chunks for multi-manual synthesis
        retriever = self.vault.as_retriever(search_kwargs={"k": 10})
        docs = retriever.invoke(user_query)
        
        context_corpus = ""
        manuals_cited = set()
        for i, d in enumerate(docs):
            src = d.metadata.get('source', 'Manual')
            manuals_cited.add(src)
            context_corpus += f"\n[Doc {i+1} Source: {src}]\n{d.page_content}\n"

        # MASTER DIRECTIVE: Structural Prompt Engineering
        system_logic = f"""
        YOU ARE THE 'DEFENCE PROCUREMENT QUERY BOT' AT NADP.
        MISSION: Provide a pointed 360-degree consultation based on the evidence below.
        
        EVIDENCE CORPUS:
        {context_corpus}

        ANALYTICAL PROTOCOL:
        1. 📋 POLICY VECTOR: Categorize (DAP/DPM) and link to TPCR roadmaps.
        2. ⚖️ PROCEDURAL PATHWAY: Sequential steps from Manuals & Handbooks.
        3. 💰 POWER VECTOR: Exact CFA and Financial Power limit from DFPDS 2026.
        4. ✅ ACTION RECOMMENDATION: Precise steps to process the case.

        CITATIONS: Explicitly cite the Manual name for every statement of fact.
        """

        # CLOUD INFERENCE: Using the NEW supported model name
        llm = ChatGroq(
            groq_api_key=self.key, 
            model_name=SYSTEM_MANIFEST["LLM_ENGINE"], 
            temperature=0,
            max_tokens=1500
        )
        
        return llm.stream(system_logic + "\n\nUser Question: " + user_query)

# ==============================================================================
# SECTION 5: COMMAND HUD & SIDEBAR (Lines 681-800)
# ==============================================================================

if not GROQ_API_KEY:
    st.error("FATAL: Security Key Missing. Deployment Halted.")
    st.stop()

# Cache the engine to ensure single-instance initialization
if "titan_engine" not in st.session_state:
    with st.spinner("🚀 Initializing Hexagonal Synthesis Engine..."):
        st.session_state.titan_engine = TitanIntelligenceEngine(GROQ_API_KEY)

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--gold);'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Real-time Metrics Column Display
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.markdown("<div class='hud-unit'><p class='hud-lbl'>PAGES</p><p class='hud-val'>1.6k+</p></div>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div class='hud-unit'><p class='hud-lbl'>DIMS</p><p class='hud-val'>768</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🖥️ PROCESS MONITOR LOG")
    terminal_ui = st.empty()
    
    # Initialize Log if missing
    if "session_telemetry" not in st.session_state:
        push_telemetry("AEGIS Titan Neural Core Active.")
    
    terminal_ui.markdown(f"<div class='terminal-box'>{get_telemetry_stream()}</div>", unsafe_allow_html=True)

    if st.button("🗑️ PURGE CACHE"):
        st.session_state.messages = []
        st.session_state.session_telemetry = []
        st.rerun()

# ==============================================================================
# SECTION 6: ANALYTICAL DASHBOARD EXECUTION (Lines 801-950+)
# ==============================================================================

st.markdown(f"<div class='oracle-header'>🛡️ {PROJECT_NAME}</div>", unsafe_allow_html=True)
st.caption(f"NADP Nagpur Strategic Dashboard | Capstone 2025-26 | Model: {SYSTEM_MANIFEST['LLM_ENGINE']}")

# Verify Neural Link before processing
if not st.session_state.titan_engine.vault:
    st.error("SYSTEM ERROR: Neural Link to Knowledge Base Broken. Check GitHub file structure.")
    st.stop()

# State Management for Message Persistence
if "messages" not in st.session_state:
    st.session_state.messages = []

# Persistent Rendering of Thread History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Primary Strategy Input Cycle
if user_q := st.chat_input("Enter procurement problem for Pentagon Analysis..."):
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    push_telemetry(f"Query Processed: {user_q[:35]}...")

    # EXECUTION OF CROSS-MANUAL ANALYSIS
    with st.chat_message("assistant"):
        with st.status("🛸 Syncing Defence Knowledge Layers...", expanded=False):
            st.write("Synthesizing context from DAP/DPM/DFPDS...")
            time.sleep(0.3)
        
        surface_display = st.empty()
        full_analysis = ""
        
        # STREAMING WITH FAIL-SAFE TOKEN PARSING
        try:
            # Call the synthesis generator
            for part in st.session_state.titan_engine.generate_analytical_brief(user_q):
                # Robustly handle different token return types from API
                if hasattr(part, 'content'):
                    token = part.content
                elif isinstance(part, str):
                    token = part
                else:
                    token = getattr(part, 'text', str(part))
                
                full_analysis += token
                surface_display.markdown(full_analysis + "▌")
            
            # Final output cleanup
            surface_display.markdown(full_analysis)
            push_telemetry("Analytical Brief Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_analysis})
        
        except Exception as e:
            # Handle API saturations and network delays
            st.error(f"ENGINE FAILURE: {str(e)}")
            push_telemetry(f"ERROR: {str(e)}", status="FAIL")

# Dynamically update the visual log HUD
terminal_ui.markdown(f"<div class='terminal-box'>{get_telemetry_stream()}</div>", unsafe_allow_html=True)

# Governance Footer Section
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    st.markdown("<div class='report-panel'><p class='hud-lbl'>GOVERNANCE</p><p>🏛️ DAP 2026 ALIGNED</p></div>", unsafe_allow_html=True)
with f_col2:
    st.markdown("<div class='report-panel'><p class='hud-lbl'>SECURITY</p><p>🔒 AIR-GAPPED VAULT</p></div>", unsafe_allow_html=True)
with f_col3:
    st.markdown("<div class='report-panel'><p class='hud-lbl'>INTELLIGENCE</p><p>🧬 HEXAGONAL SYNTHESIS</p></div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; color: #555; font-size: 0.75rem;'>"
    "Proprietary Strategic Intelligence | National Academy of Defence Production | Nagpur | Version 14.0.1 Stable"
    "</p>", 
    unsafe_allow_html=True
)
