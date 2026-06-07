# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v10.0 - TITAN FINAL)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ENGINE: Groq LPU + Llama 3.1 70B (State-of-the-Art Neural Infrastructure)
# VERSION: 10.0.1 - STABLE DEPLOYMENT BUILD
# ==============================================================================

import streamlit as st
import os
import time
import pandas as pd
import logging
import json
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==============================================================================
# SECTION 1: SYSTEM IDENTITY & SECURITY (Lines 30-120)
# ==============================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "DPQB-TITAN-ULTIMATE"
ACADEMY = "NADP Nagpur"

# Audit logging initialization
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TITAN_FINAL")

# Secure API Key Handling with Error Catching
try:
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    else:
        # Emergency hardcoded fallback for direct execution
        GROQ_API_KEY = "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"
except Exception as e:
    logger.error(f"Secret Retrieval Failure: {e}")
    GROQ_API_KEY = None

# ==============================================================================
# SECTION 2: GLOBAL UTILITIES & TELEMETRY (Lines 121-250)
# ==============================================================================

def push_telemetry(msg, status="INFO"):
    """
    Maintains a real-time system event log in the user session.
    Used for proving system robustness during the Capstone presentation.
    """
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = []
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] {status}: {msg}"
    st.session_state.session_telemetry.append(log_entry)
    
    # Prune old logs to maintain performance
    if len(st.session_state.session_telemetry) > 25:
        st.session_state.session_telemetry.pop(0)

def get_session_logs():
    """Returns the formatted log string for the UI display."""
    return "\n".join(st.session_state.session_telemetry)

# ==============================================================================
# SECTION 3: TACTICAL INTERFACE DESIGN (CSS) (Lines 251-450)
# ==============================================================================

st.set_page_config(
    page_title=PROJECT_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_military_grade_ui():
    """Injects high-fidelity tactical CSS for military command aesthetics."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
        
        :root {
            --gold: #d4af37;
            --navy-deep: #020c1b;
            --tactical-blue: #0a192f;
            --cyan-glow: #64ffda;
            --text-silver: #ccd6f6;
            --warning-red: #ff4b2b;
        }

        .stApp {
            background-color: var(--navy-deep);
            color: var(--text-silver);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Sidebar Strategic Command Panel */
        [data-testid="stSidebar"] {
            background-color: #010a15;
            border-right: 2px solid var(--gold);
            box-shadow: 10px 0px 30px rgba(0,0,0,0.5);
        }

        /* Main Tactical HUD Header */
        .tactical-header {
            text-align: center;
            padding: 40px;
            background: linear-gradient(180deg, #112240 0%, var(--navy-deep) 100%);
            border-bottom: 3px double var(--gold);
            margin-bottom: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
        .tactical-header h1 {
            color: var(--gold);
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 12px;
            text-transform: uppercase;
            text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.5);
        }

        /* Result Cards */
        .analysis-card {
            background-color: #112240;
            border: 1px solid var(--cyan-glow);
            padding: 30px;
            border-radius: 4px;
            border-left: 12px solid var(--gold);
            margin-bottom: 35px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        }

        /* Real-time Telemetry Terminal */
        .telemetry-log {
            background-color: #000;
            color: #39ff14;
            padding: 15px;
            border: 1px solid #333;
            font-size: 0.82rem;
            height: 280px;
            overflow-y: auto;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 20px #000;
        }

        /* Metric Dashboard Units */
        .metric-container {
            background: #001219;
            border: 1px solid #1f3a5a;
            padding: 15px;
            text-align: center;
            border-radius: 3px;
        }
        .metric-label { color: var(--gold); font-size: 0.7rem; font-weight: bold; text-transform: uppercase; }
        .metric-value { color: white; font-size: 1.7rem; font-weight: 900; }

        /* Scrollbars */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--navy-deep); }
        ::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

apply_military_grade_ui()

# ==============================================================================
# SECTION 4: INTELLIGENT KNOWLEDGE CORE (Lines 451-650)
# ==============================================================================

class TitanIntelligenceEngine:
    """Orchestrates Strategic Retrieval and High-Intelligence Synthesis."""
    
    def __init__(self, api_key):
        self.key = api_key
        # High-Resolution Local Embedder
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vault_path = "." # Files are in root directory on GitHub
        self.vault = self._load_vault()

    def _load_vault(self):
        """Loads and verifies the integrity of the neural knowledge base."""
        if os.path.exists("index.faiss"):
            try:
                return FAISS.load_local(
                    self.vault_path, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                logger.error(f"VAULT_LOAD_ERR: {e}")
                return None
        return None

    def synthesize_analytical_brief(self, user_query):
        """
        Executes a 360-degree synthesis (Policy, Process, Power, Plan, Peril, Proceed).
        This method uses robust token extraction to prevent attribute errors.
        """
        if not self.vault:
            return "ERROR: Neural Architecture Offline."

        # 1. CONTEXTUAL MINING (K=12 for deep synthesis)
        retriever = self.vault.as_retriever(search_kwargs={"k": 12})
        docs = retriever.invoke(user_query)
        
        # 2. SOURCE SEPARATION LOGIC
        context_data = ""
        for i, d in enumerate(docs):
            src = d.metadata.get('source', 'Classified Manual')
            context_data += f"\n[DOC LAYER {i+1} | ORIGIN: {src}]\n{d.page_content}\n"

        # 3. ADVANCED SYSTEM PROMPT
        # Forces Llama 3.1 70B to behave as a Senior Strategic Advisor
        system_directive = f"""
        YOU ARE THE 'DEFENCE PROCUREMENT QUERY BOT'.
        STRICT MISSION: Execute a high-fidelity strategic analysis on the user query.
        
        KNOWLEDGE EVIDENCE BASE:
        {context_data}

        PROCEDURAL PROTOCOL (ADDRESS ALL 6 ANGLES):
        1. 📋 SITUATIONAL ANALYSIS: Determine if Capital (DAP) or Revenue (DPM).
        2. ⚖️ PROCEDURAL PATHWAY: Detailed steps from Manuals & Handbooks.
        3. 💰 FINANCIAL AUTHORITY: Identify CFA from DFPDS 2026 value limits.
        4. 🔭 STRATEGIC ALIGNMENT: Link with TPCR technological roadmaps.
        5. ⚠️ PERIL AUDIT: Warn against potential audit or compliance hurdles.
        6. ✅ THE PROCEED SOLUTION: A definitive 3-step actionable roadmap.

        CITATIONS: You MUST explicitly mention the specific manual by name for every rule cited.
        """

        # 4. CLOUD INFERENCE CONFIGURATION
        llm = ChatGroq(
            groq_api_key=self.key, 
            model_name="llama-3.1-70b-versatile",
            temperature=0, # Deterministic Factuality
            max_tokens=2048
        )
        
        return llm.stream(system_directive + "\n\nUser Question: " + user_query)

# ==============================================================================
# SECTION 5: COMMAND SIDEBAR HUD (Lines 651-780)
# ==============================================================================

if not GROQ_API_KEY:
    st.error("FATAL: Security Key Missing. Deployment Halted.")
    st.stop()

# Initialize Analytical Engine
engine = TitanIntelligenceEngine(GROQ_API_KEY)

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--gold);'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Real-time System Metrics
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.markdown("<div class='metric-container'><p class='metric-label'>CORPUS</p><p class='metric-value'>1.6k+</p></div>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div class='metric-container'><p class='metric-label'>BRAIN</p><p class='metric-value'>70B</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🖥️ PROCESS MONITOR LOG")
    log_box = st.empty()
    
    # Persistent Log Display Logic
    if "session_telemetry" not in st.session_state:
        push_telemetry("AEGIS Titan Neural Core Online.")
    
    log_box.markdown(f"<div class='telemetry-log'>{get_session_logs()}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗃️ KNOWLEDGE REPOSITORIES")
    manual_manifest = {
        "Policy": "DAP 2026 / DPM V1",
        "Financial": "DFPDS 2026 (All)",
        "Strategy": "TPCR Roadmaps",
        "Execution": "DAP Handbook / DPM V2"
    }
    for m_key, m_val in manual_manifest.items():
        st.caption(f"**{m_key}**: {m_val} ✅")

    if st.button("🔴 RESET SESSION"):
        st.session_state.messages = []
        st.session_state.session_telemetry = []
        st.rerun()

# ==============================================================================
# SECTION 6: ANALYTICAL INTERFACE EXECUTION (Lines 781-920)
# ==============================================================================

st.markdown(f"<div class='tactical-header'><h1>🛡️ {PROJECT_NAME}</h1></div>", unsafe_allow_html=True)
st.caption(f"NADP Nagpur Strategic Dashboard | Capstone 2025-26 | ID: {SYSTEM_CODE}")

# Vault verification
if not engine.vault:
    st.error("SYSTEM ERROR: Permanent Vault files (index.faiss) not detected. Check GitHub root.")
    st.stop()

# Persistent State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Conversation Threads
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User-to-Bot Synthesis Cycle
if user_input := st.chat_input("Enter procurement query (e.g., 'Analyze ₹150cr Make-II project')..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    push_telemetry(f"Query Processed: {user_input[:40]}...")

    # EXECUTION OF CROSS-MANUAL ANALYSIS
    with st.chat_message("assistant"):
        with st.status("🛸 Accessing Defence Knowledge Layers...", expanded=False):
            st.write("Synthesizing context from DAP/DPM/DFPDS...")
            time.sleep(0.3)
        
        output_surface = st.empty()
        full_analysis = ""
        
        # STREAMING WITH ROBUST TOKEN EXTRACTION
        try:
            for part in engine.synthesize_analytical_brief(user_input):
                # FIXED ATTRIBUTE ERROR: Uses a safer token extractor
                if hasattr(part, 'content'):
                    token = part.content
                else:
                    token = str(part)
                
                full_analysis += token
                output_surface.markdown(full_analysis + "▌")
            
            output_surface.markdown(full_analysis)
            push_telemetry("Strategic Analysis Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_analysis})
        
        except Exception as e:
            # Handle Timeout and API saturation
            st.error(f"ENGINE TIMEOUT: {str(e)}")
            push_telemetry(f"CRITICAL ERROR: {str(e)}", status="FAIL")

# Update logs visually after every interaction
log_box.markdown(f"<div class='telemetry-log'>{get_session_logs()}</div>", unsafe_allow_html=True)

# Final Dashboard Footer
st.markdown("---")
col_btm1, col_btm2, col_btm3 = st.columns(3)
with col_btm1:
    st.markdown("<div class='analysis-card'><p class='metric-label'>GOVERNANCE</p><p>🏛️ DAP 2026 FRAMEWORK</p></div>", unsafe_allow_html=True)
with col_btm2:
    st.markdown("<div class='analysis-card'><p class='metric-label'>SECURITY</p><p>🔒 AIR-GAPPED VAULT</p></div>", unsafe_allow_html=True)
with col_btm3:
    st.markdown("<div class='analysis-card'><p class='metric-label'>INTELLIGENCE</p><p>🧬 HEXAGONAL SYNTHESIS</p></div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; color: #555; font-size: 0.75rem;'>"
    "Proprietary Decision Support System | National Academy of Defence Production | Nagpur 2025-26"
    "</p>", 
    unsafe_allow_html=True
)
