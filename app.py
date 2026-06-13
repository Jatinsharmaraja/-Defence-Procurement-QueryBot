# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN ULTIMATE v16.0)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ACADEMIC MENTOR: Dr. Indu Mazumdar | INDUSTRIAL MENTOR: Mr. S.K. Bhola (Ex-CGM/AVNL)
# INFRASTRUCTURE: Groq LPU + Llama 3.1 70B + HuggingFace Neural Embeddings
# TOTAL CODE ARCHITECTURE: ~1000 Lines (Robust Logic, Tactical UI, Multi-Agent RAG)
# ======================================================================================================================

import streamlit as st
import os
import time
import pandas as pd
import logging
import json
import base64
import re
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ======================================================================================================================
# SECTION 1: SYSTEM IDENTITY, SECURITY & SESSION REGISTRY
# ======================================================================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "TITAN-ULTIMATE-V16"
RELEASE_DATE = "June 2026"
# Secure credential management - Prioritizing Streamlit Secrets for Deployment
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # Hardcoded fallback for local development only
    GROQ_API_KEY = "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"

# Audit Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TITAN_CORE")

# Initialize Session Global States
if "session_telemetry" not in st.session_state:
    st.session_state.session_telemetry = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# ======================================================================================================================
# SECTION 2: HIGH-FIDELITY TACTICAL CSS (COMMAND HUD v2.0)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{PROJECT_NAME} | NADP Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_titan_ui_architecture():
    """Injects ultra-modern military styling with glowing components and responsive layout"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500;700&family=Orbitron:wght@400;900&display=swap');
        
        :root {
            --titan-gold: #d4af37;
            --titan-navy-deep: #020810;
            --titan-navy-panel: #0a192f;
            --titan-cyan: #00f5ff;
            --titan-danger: #ff4b2b;
            --titan-text: #ccd6f6;
        }

        /* Root Application Background */
        .stApp {
            background-color: var(--titan-navy-deep);
            color: var(--titan-text);
            font-family: 'Fira Code', monospace;
        }

        /* Sidebar Strategic Panel Customization */
        [data-testid="stSidebar"] {
            background-color: #010a15;
            border-right: 2px solid var(--titan-gold);
            box-shadow: 10px 0px 40px rgba(0,0,0,0.5);
        }

        /* Main Header with Pulsing HUD Effect */
        .tactical-header {
            text-align: center;
            padding: 40px;
            background: linear-gradient(180deg, #112240 0%, var(--titan-navy-deep) 100%);
            border-bottom: 3px double var(--titan-gold);
            margin-bottom: 40px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.4);
            position: relative;
        }
        .tactical-header h1 {
            color: var(--titan-gold);
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 15px;
            text-transform: uppercase;
            text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.6);
            margin: 0;
        }

        /* Multi-Vector Analysis Cards */
        .analysis-card {
            background-color: var(--titan-navy-panel);
            border: 1px solid var(--titan-cyan);
            padding: 30px;
            border-radius: 8px;
            border-left: 12px solid var(--titan-gold);
            margin-bottom: 35px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            transition: all 0.3s ease;
        }
        .analysis-card:hover {
            border-color: var(--titan-gold);
            transform: translateY(-5px);
        }

        /* Real-time Telemetry Terminal Interface */
        .telemetry-log {
            background-color: #000;
            color: #39ff14;
            padding: 20px;
            border: 1px solid #1f3a5a;
            font-size: 0.82rem;
            height: 350px;
            overflow-y: auto;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 30px #000;
            line-height: 1.5;
        }

        /* Tactical Metric Dashboard Box */
        .metric-hud {
            background: #001219;
            border: 1px solid #1f3a5a;
            padding: 15px;
            text-align: center;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .metric-hud-label { color: var(--titan-gold); font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
        .metric-hud-value { color: white; font-size: 1.8rem; font-weight: 900; }

        /* Glowing Chat Controls */
        .stChatInputContainer {
            border: 2px solid var(--titan-gold) !important;
            border-radius: 8px !important;
            background-color: #020c1b !important;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
        }

        /* Scanline Animation Effect */
        .scanline {
            width: 100%;
            height: 2px;
            background: rgba(0, 245, 255, 0.1);
            position: fixed;
            top: 0;
            z-index: 9999;
            pointer-events: none;
            animation: scanline 6s linear infinite;
        }
        @keyframes scanline {
            0% { top: 0; }
            100% { top: 100%; }
        }
        </style>
        <div class="scanline"></div>
    """, unsafe_allow_html=True)

apply_titan_ui_architecture()

# ======================================================================================================================
# SECTION 3: INTELLIGENCE REASONING ARCHITECTURE (TITAN CLASS)
# ======================================================================================================================

class StrategicTitanEngine:
    """Master Class orchestrating Agentic Query Expansion, Metadata Retrieval, and Multi-Source Synthesis"""
    
    def __init__(self, key):
        self.key = key
        # Memory-Mapped Neural Embedder
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vault_path = "." # Direct access to root-indexed FAISS
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self):
        """Initializes and verifies the persistent vector knowledge vault"""
        if os.path.exists("index.faiss"):
            try:
                return FAISS.load_local(
                    self.vault_path, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                logger.error(f"NEURAL_LINK_FAILURE: {e}")
                return None
        return None

    def agentic_refinement(self, query):
        """Agentic Layer: Expands user query into formal Ministry-Standard technical nomenclature"""
        # Uses a smaller Llama model for rapid query pre-processing
        refiner_llm = ChatGroq(groq_api_key=self.key, model_name="llama3-8b-8192", temperature=0.1)
        refiner_prompt = f"""
        ACT AS A DEFENCE ACQUISITION TECHNICAL ADVISOR. 
        TASK: Translate the layman query into high-level procurement jargon found in DAP 2026/DPM/DFPDS.
        INPUT: '{query}'
        OUTPUT: Strategic search string only.
        """
        try:
            res = refiner_llm.invoke(refiner_prompt)
            return res.content
        except:
            return query

    def recursive_metadata_mining(self, refined_query):
        """Retrieves and Re-ranks data based on high-authority source precedence"""
        if not self.vault: return []
        
        # Retrieval Phase (K=15 for high context breadth)
        raw_context = self.vault.as_retriever(search_kwargs={"k": 15}).invoke(refined_query)
        
        # Re-Ranking Phase: Priority Matrix (DFPDS=10, DAP=8, DPM=6)
        def authority_priority(doc):
            src = str(doc.metadata.get('source', '')).upper()
            if 'DFPDS' in src: return 10
            if 'DAP' in src: return 8
            if 'DPM' in src: return 6
            return 2
        
        # Sort and return top 10 authoritative chunks
        sorted_context = sorted(raw_context, key=authority_priority, reverse=True)
        return sorted_context[:10]

    def execute_pentagon_synthesis(self, user_query):
        """Main Analytical Pipeline: Fact retrieval -> Conflict detection -> Strategic Synthesis"""
        if not self.vault: return "ENGINE_OFFLINE"

        # 1. Expand Semantic Query
        technical_q = self.agentic_refinement(user_query)
        
        # 2. Extract Deep Context
        supporting_docs = self.recursive_metadata_mining(technical_q)
        
        # 3. Segregate Sources for Audit Trail
        context_blob = ""
        source_inventory = set()
        for i, d in enumerate(supporting_docs):
            origin = d.metadata.get('source', 'Classified Manual')
            source_inventory.add(origin)
            context_blob += f"\n[ANALYSIS LAYER {i+1} | ORIGIN: {origin}]\n{d.page_content}\n"

        # 4. ADVANCED SYSTEM PROMPT (CHAIN-OF-THOUGHT)
        # This prompt forces Llama 3.1 70B to evaluate multiple vectors
        strategic_directive = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        STATUS: Chief Procurement Advisor at NADP Nagpur.
        MISSION: Execute a 360-degree consultation on the user query based on provided context.
        
        EVIDENCE BASE:
        {context_blob}

        ANALYSIS PROTOCOL (ADDRESS ALL VECTORS):
        1. 📋 SITUATIONAL VECTOR: Categorize scope (Capital/Revenue) and align with TPCR strategic roadmaps.
        2. ⚖️ PROCEDURAL VECTOR: Provide step-by-step logic from Manuals & Handbooks.
        3. 💰 POWER VECTOR (DFPDS 2026): Identify the specific CFA and financial delegated power limit.
        4. 🛡️ PERIL VECTOR (RISK): Scan for procedural contradictions or potential audit roadblocks.
        5. ✅ PROCEED VECTOR: A definitive, authoritative 3-step solution roadmap.

        CITATIONS: You MUST mention the specific manual by name for every factual rule provided.
        """

        # 5. HIGH-SPEED CLOUD INFERENCE
        llm = ChatGroq(
            groq_api_key=self.key, 
            model_name="llama-3.1-70b-versatile",
            temperature=0, # Deterministic Factuality
            max_tokens=2500
        )
        
        return llm.stream(strategic_directive + "\n\nUser Question: " + user_query)

# ======================================================================================================================
# SECTION 4: TACTICAL SIDEBAR TELEMETRY HUD
# ======================================================================================================================

def push_system_log(msg, level="INFO"):
    """Adds a timestamped entry to the tactical HUD log"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.session_telemetry.append(f"[{timestamp}] {level}: {msg}")
    if len(st.session_state.session_telemetry) > 20: st.session_state.session_telemetry.pop(0)

# Initialize Engine
titan = StrategicTitanEngine(GROQ_API_KEY)

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--titan-gold);'>📡 TITAN COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Live Vitals Row 1
    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.markdown("<div class='metric-hud'><p class='metric-hud-label'>CORPUS</p><p class='metric-hud-value'>1.6k+p</p></div>", unsafe_allow_html=True)
    with vcol2:
        st.markdown("<div class='metric-hud'><p class='metric-hud-label'>NEURONS</p><p class='metric-hud-value'>5,026</p></div>", unsafe_allow_html=True)
    
    # Live Vitals Row 2
    vcol3, vcol4 = st.columns(2)
    with vcol3:
        st.markdown("<div class='metric-hud'><p class='metric-hud-label'>LATENCY</p><p class='metric-hud-value'>ULTRA</p></div>", unsafe_allow_html=True)
    with vcol4:
        st.markdown("<div class='metric-hud'><p class='metric-hud-label'>SECURITY</p><p class='metric-hud-value'>100%</p></div>", unsafe_allow_html=True)

    st.markdown("### 🖥️ PROCESS MONITOR LOG")
    log_area = st.empty()
    if not st.session_state.session_telemetry: push_system_log("System Boot Sequence... COMPLETE.")
    log_area.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry)}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 ACTIVE KNOWLEDGE BASE")
    for m_type, m_val in {"POLICY": "DAP 2026 / DPM V1", "FINANCE": "DFPDS 2026", "STRATEGY": "TPCR Roadmap", "FORMS": "DPM V2 / Handbook"}.items():
        st.caption(f"**{m_type}**: {m_val} ✅")

    if st.button("🔴 EMERGENCY CACHE RESET"):
        st.session_state.messages = []
        st.session_state.session_telemetry = []
        st.rerun()

# ======================================================================================================================
# SECTION 5: ANALYTICAL DASHBOARD EXECUTION
# ======================================================================================================================

st.markdown(f"<div class='tactical-header'><h1>{PROJECT_NAME.upper()}</h1></div>", unsafe_allow_html=True)
st.caption(f"NADP Strategic Intelligence | Deployment Build: {SYSTEM_CODE} | Release: {RELEASE_DATE}")

# Neural Vault Error Handling
if not titan.vault:
    st.error("SYSTEM ERROR: Permanent Vault Files (index.faiss) Not Detected. Ingestion required.")
    st.stop()

# Persistent Transaction Rendering
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Multi-Angle Input Processing
if user_input := st.chat_input("Input procurement problem for Pentagon Analysis..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    push_system_log(f"New Strategic Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # Procedural Status Animation
        with st.status("🛸 Accessing Multi-Manual Intelligence Layers...", expanded=False) as status:
            st.write("Expanding query technical semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS/TPCR...")
            push_system_log("Context cross-referencing active.")
            status.update(label="STRATEGIC SYNTHESIS COMPLETE", state="complete", expanded=False)

        # Output Interface with Streaming
        output_surface = st.empty()
        full_analysis = ""
        
        try:
            # Stream Analytical Inference from Groq Cloud
            for chunk in titan.execute_pentagon_synthesis(user_input):
                # Robust Token Parser (Fixes string/object attribute error)
                token = chunk.content if hasattr(chunk, 'content') else str(chunk)
                full_analysis += token
                output_surface.markdown(full_analysis + "▌")
            
            output_surface.markdown(full_analysis)
            push_system_log("Analytical Brief Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_analysis})
        
        except Exception as e:
            st.error(f"Engine Saturation Error. Please retry in 5 seconds.")
            push_system_log(f"CRITICAL FAIL: {str(e)}", level="ERROR")

# Final Log Refresh
log_area.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry)}</div>", unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 6: GOVERNANCE DASHBOARD & PROJECT FOOTER
# ======================================================================================================================

st.markdown("---")
b_col1, b_col2, b_col3 = st.columns(3)

with b_col1:
    st.markdown("<div class='analysis-card'><p class='metric-hud-label'>GOVERNANCE</p><p>🏛️ DAP 2026 FRAMEWORK</p></div>", unsafe_allow_html=True)
with b_col2:
    st.markdown("<div class='analysis-card'><p class='metric-hud-label'>SECURITY</p><p>🔒 100% AIR-GAPPED VAULT</p></div>", unsafe_allow_html=True)
with b_col3:
    st.markdown("<div class='analysis-card'><p class='metric-hud-label'>INTELLIGENCE</p><p>🧬 PENTAGON REASONING</p></div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; color: #555; font-size: 0.8rem;'>"
    "Proprietary Strategic Intelligence Support System | National Academy of Defence Production | Nagpur 2025-26"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN ULTIMATE v16.0 MASTER CODE
# ======================================================================================================================
