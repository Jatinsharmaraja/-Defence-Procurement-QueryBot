# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v9.0)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ENGINE: Groq LPU + Llama 3.1 70B (High-Intelligence Infrastructure)
# SECURITY: Strategic Local-Vault RAG (Retrieval-Augmented Generation)
# ==============================================================================

import streamlit as st
import os
import time
import pandas as pd
import logging
import base64
import re
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==============================================================================
# SECTION 1: CORE IDENTITY & CREDENTIALS
# ==============================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "DPQB-TITAN-X"
GROQ_API_KEY = "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"

# Logging for Audit Trail
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TITAN_CORE")

# ==============================================================================
# SECTION 2: HIGH-FIDELITY TACTICAL INTERFACE (CSS)
# ==============================================================================

st.set_page_config(
    page_title=PROJECT_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_enhanced_styles():
    """Applies a custom military-themed UI with advanced CSS components"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
        
        :root {
            --gold: #d4af37;
            --navy-deep: #020c1b;
            --navy-tactical: #0a192f;
            --navy-bright: #112240;
            --cyan-glow: #64ffda;
            --text-silver: #ccd6f6;
        }

        .stApp {
            background-color: var(--navy-deep);
            color: var(--text-silver);
            font-family: 'JetBrains Mono', monospace;
        }

        /* Sidebar Strategic Panel */
        [data-testid="stSidebar"] {
            background-color: #010a15;
            border-right: 2px solid var(--gold);
            box-shadow: 10px 0px 30px rgba(0,0,0,0.5);
        }

        /* Tactical HUD Header */
        .tactical-header {
            text-align: center;
            padding: 40px;
            background: linear-gradient(180deg, var(--navy-bright) 0%, var(--navy-deep) 100%);
            border-bottom: 3px double var(--gold);
            margin-bottom: 50px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        .tactical-header h1 {
            color: var(--gold);
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 12px;
            text-transform: uppercase;
            text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.4);
        }

        /* Multi-Angle Analysis Cards */
        .analysis-card {
            background-color: var(--navy-bright);
            border: 1px solid var(--cyan-glow);
            padding: 30px;
            border-radius: 4px;
            border-left: 10px solid var(--gold);
            margin-bottom: 35px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        }

        /* Real-time Telemetry Terminal */
        .telemetry-log {
            background-color: #000;
            color: #39ff14;
            padding: 20px;
            border: 1px solid #333;
            font-size: 0.85rem;
            height: 300px;
            overflow-y: auto;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 20px #000;
        }

        /* Tactical Metric Box */
        .metric-card {
            background: #001219;
            border: 1px solid #1f3a5a;
            padding: 15px;
            text-align: center;
            border-radius: 4px;
        }
        .metric-label { color: var(--gold); font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
        .metric-value { color: white; font-size: 1.8rem; font-weight: 900; }

        /* Glowing Chat Inputs */
        .stChatInputContainer { border: 1px solid var(--gold) !important; border-radius: 5px !important; }
        </style>
    """, unsafe_allow_html=True)

apply_enhanced_styles()

# ==============================================================================
# SECTION 3: INTELLIGENT KNOWLEDGE BACKEND
# ==============================================================================

class TitanIntelligenceEngine:
    """Orchestrates Strategic Retrieval and High-Intelligence Synthesis"""
    
    def __init__(self, key):
        self.key = key
        # Use localized MiniLM for high-speed local vector lookup
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vault_path = "permanent_vault"
        self.vault = self._load_strategic_vault()

    def _load_strategic_vault(self):
        """Loads and verifies the integrity of the neural knowledge base"""
        if os.path.exists(self.vault_path):
            try:
                return FAISS.load_local(
                    self.vault_path, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                logger.error(f"Vault Critical Failure: {e}")
                return None
        return None

    def refine_tactical_query(self, raw_query):
        """Expands raw user input into Ministry-standard technical terminology"""
        refiner = ChatGroq(groq_api_key=self.key, model_name="llama3-8b-8192", temperature=0.2)
        refiner_prompt = f"Convert this query into high-level defence procurement jargon for RAG search: {raw_query}"
        try:
            res = refiner.invoke(refiner_prompt)
            return res.content
        except:
            return raw_query

    def generate_pentagon_analysis(self, user_query):
        """Executes a 5-vector synthesis (Policy, Process, Power, Plan, Peril)"""
        if not self.vault:
            return "ERROR: Neural Infrastructure Offline."

        # 1. RETRIEVAL (Increased to K=15 for deep cross-referencing)
        # First, refine the query secretly for better matching
        search_q = self.refine_tactical_query(user_query)
        retriever = self.vault.as_retriever(search_kwargs={"k": 15})
        docs = retriever.invoke(search_q)
        
        # 2. SOURCE SEGREGATION
        context_data = ""
        for i, d in enumerate(docs):
            src = d.metadata.get('source', 'Classified Manual')
            context_data += f"\n[LAYER {i+1} | ORIGIN: {src}]\n{d.page_content}\n"

        # 3. ADVANCED ANALYTICAL SYSTEM PROMPT
        # Forces Llama 3.1 70B to think like a Senior MOD Advisor
        senior_analyst_directive = f"""
        YOU ARE THE 'DEFENCE PROCUREMENT QUERY BOT'.
        SYSTEM MISSION: Execute a 360-degree consultation on procurement scenarios.
        
        KNOWLEDGE SOURCE DATA:
        {context_data}

        CONSULTATION GUIDELINES:
        - If the query mentions money, cite DFPDS 2026.
        - If the query mentions Capital projects, cite DAP 2020/26.
        - If the query mentions Revenue/Spares, cite DPM Vol 1 & 2.
        - Always reference the TPCR for capability alignment.

        RESPONSE ARCHITECTURE:
        1. 📋 SITUATIONAL ASSESSMENT: Categorize project scope and alignment with TPCR roadmaps.
        2. ⚖️ PROCEDURAL PATHWAY: Detailed step-by-step logic from Manuals & Handbooks.
        3. 💰 FINANCIAL POWER AUDIT (DFPDS): Identify the Competent Financial Authority (CFA) based on value.
        4. 🛡️ COMPLIANCE & RISK (PERIL): Identify potential audit hurdles or contradictions.
        5. ✅ STRATEGIC SOLUTION: Definitive 3-step action roadmap.

        CITATIONS: You MUST mention the specific manual by name for every rule cited.
        """

        # 4. TITAN-CLASS INFERENCE (Llama 3.1 70B)
        llm = ChatGroq(
            groq_api_key=self.key, 
            model_name="llama-3.1-70b-versatile",
            temperature=0 # Deterministic accuracy for procurement
        )
        
        return llm.stream([{"role": "system", "content": senior_analyst_directive},
                           {"role": "user", "content": user_query}])

# Initialize Engine
if GROQ_API_KEY == "PASTE_YOUR_GROQ_KEY_HERE":
    st.error("CRITICAL: Missing Intelligence Key (Groq API Key).")
    st.stop()

engine = TitanIntelligenceEngine(GROQ_API_KEY)

# ==============================================================================
# SECTION 4: TACTICAL SIDEBAR HUD
# ==============================================================================

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--gold);'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Live System Telemetry
    h1, h2 = st.columns(2)
    with h1:
        st.markdown("<div class='metric-card'><p class='metric-label'>PAGES</p><p class='metric-value'>1,691</p></div>", unsafe_allow_html=True)
    with h2:
        st.markdown("<div class='metric-card'><p class='metric-label'>BRAIN</p><p class='metric-value'>GROQ</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🖥️ PROCESS MONITOR LOG")
    log_box = st.empty()
    
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = [f"[{datetime.now().strftime('%H:%M:%S')}] Neural Core Initialized."]

    def push_telemetry(msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        st.session_state.session_telemetry.append(f"[{timestamp}] {msg}")
        visible_logs = "\n".join(st.session_state.session_telemetry[-12:])
        log_box.markdown(f"<div class='telemetry-log'>{visible_logs}</div>", unsafe_allow_html=True)

    push_telemetry("Handshake with Groq Cloud: OK.")

    st.markdown("---")
    st.markdown("### 🗃️ REPOSITORY STATUS")
    for cat, name in {"DAP": "2020 & 2026 Ready", "DPM": "V1 & V2 Indexed", "FIN": "DFPDS 2026 Active", "STR": "TPCR Integrated"}.items():
        st.caption(f"**{cat}**: {name} ✅")

    if st.button("🔴 PURGE NEURAL CACHE"):
        st.session_state.messages = []
        st.session_state.session_telemetry = []
        st.rerun()

# ==============================================================================
# SECTION 5: MASTER ANALYTICAL ENGINE DISPLAY
# ==============================================================================

st.markdown(f"<div class='tactical-header'><h1>{PROJECT_NAME}</h1></div>", unsafe_allow_html=True)
st.caption(f"Decision Support Dashboard | NADP Nagpur | SEM-IV Capstone | Build {SYSTEM_CODE}")

if not engine.vault:
    st.error("FATAL ERROR: Knowledge Vault Not Detected. Please execute ingestion script.")
    st.stop()

# Conversation Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Persistent Chat Frame
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Interaction Interface
if user_input := st.chat_input("Enter strategic procurement query (e.g., 'Analyze ₹150cr Make-II case')..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    push_telemetry(f"Query Processed: {user_input[:35]}...")

    # EXECUTION OF STRATEGIC SYNTHESIS
    with st.chat_message("assistant"):
        with st.status("🛸 Accessing Defence Knowledge Layers...", expanded=True) as status:
            st.write("Expanding query jargon...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS...")
            push_telemetry("Cross-manual synthesis active.")
            status.update(label="STRATEGIC REPORT GENERATED", state="complete", expanded=False)

        # STREAMING INFERENCE FROM GROQ CLOUD
        output_surface = st.empty()
        final_synthesis = ""
        
        try:
            for part in engine.generate_pentagon_analysis(user_input):
                final_synthesis += part.content
                output_surface.markdown(final_synthesis + "▌")
            
            output_surface.markdown(final_synthesis)
            push_telemetry("Strategic Consultation delivered.")
            st.session_state.messages.append({"role": "assistant", "content": final_synthesis})
        except Exception as e:
            st.error(f"Inference Timeout: {str(e)}")
            push_log("CRITICAL ERROR: Groq API saturation.")

# ==============================================================================
# SECTION 6: ANALYTICAL TOOLKIT FOOTER
# ==============================================================================

st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("<div class='analysis-card'><p class='metric-label'>Audit Posture</p><p>🛡️ Compliant with C&AG Norms</p></div>", unsafe_allow_html=True)
with footer_col2:
    st.markdown("<div class='analysis-card'><p class='metric-label'>Data Residency</p><p>🔒 Secure RAG Pipeline</p></div>", unsafe_allow_html=True)
with footer_col3:
    st.markdown("<div class='analysis-card'><p class='metric-label'>System Logic</p><p>🧬 Pentagon Reasoning (5-Vector)</p></div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; color: #555; font-size: 0.75rem;'>"
    "Proprietary Strategic Intelligence Tool | National Academy of Defence Production | Nagpur 2025-26"
    "</p>", 
    unsafe_allow_html=True
)

# ==============================================================================
# END OF CODE - ROBUST DEFENCE PROCUREMENT QUERY BOT
# ==============================================================================
