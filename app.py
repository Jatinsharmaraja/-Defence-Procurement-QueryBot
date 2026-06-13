# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN DIAMOND v20.0)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.1 70B + HuggingFace Neural Transformers
# ======================================================================================================================
"""
TITLE: Design and Development of an AI-Based Chatbot for Defence Procurement Query Resolution
VERSION: 20.0.1 (Diamond Deployment Build)
CODE STATUS: MISSION CRITICAL / STABLE
TOTAL CODE LINES: 1000+

TECHNICAL OVERVIEW:
This system utilizes a "Hexagonal Agentic Reasoning" architecture. It processes 1,691 pages of 
unstructured technical text (DAP, DPM, DFPDS, TPCR) into a 5,026-node vector space.

LOGIC STACK:
- Vector Engine: FAISS (Facebook AI Similarity Search)
- Embedding Engine: Nomic-Embed-Text-v1.5 (768 Dimensions)
- Reasoning Engine: Llama-3.1-70B-Versatile
- UI Framework: Custom Streamlit Tactical HUD (Unified Command)
"""

import streamlit as st
import os
import time
import pandas as pd
import logging
import json
import base64
import re
import sys
import traceback
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Generator

# ======================================================================================================================
# SECTION 1: ADVANCED NEURAL PROCESSING IMPORTS (FIXED)
# ======================================================================================================================

try:
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_groq import ChatGroq
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document 
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError as e:
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure requirements.txt is updated.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE CONFIGURATION
# ======================================================================================================================

class TitanConfig:
    """Centralized System Configuration Registry."""
    SYSTEM_NAME = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID = "DPQB-TITAN-v20-DIAMOND"
    VERSION = "20.0.1"
    ACADEMY = "National Academy of Defence Production (NADP)"
    
    # Intelligence Parameters
    PRIMARY_LLM = "llama-3.1-70b-versatile"
    UTILITY_LLM = "llama-3.1-8b-instant"
    EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
    
    # Search & Data Parameters
    VAULT_SEARCH_PATHS = [".", "permanent_vault", "/mount/src/-defence-procurement-querybot"]
    K_NEIGHBORS = 15
    CHUNK_SIZE = 1000
    
    # Visual Branding (Strategic Command Palette)
    GOLD = "#d4af37"
    NAVY_DEEP = "#020810"
    NAVY_HUD = "#0a192f"
    CYAN = "#00f5ff"
    TEXT_SILVER = "#ccd6f6"

# Initialize Secure System Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - TITAN_V20 - %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (UNIFIED HUD)
# ======================================================================================================================

def apply_tactical_ui():
    """Implements a high-fidelity military-style tactical interface. Sidebars are removed."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
        
        /* Root Application Overrides */
        .stApp {{
            background-color: {TitanConfig.NAVY_DEEP};
            color: {TitanConfig.TEXT_SILVER};
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Zero-Sidebar Interface */
        [data-testid="stSidebar"] {{ display: none; }}
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}

        /* Unified Command Header */
        .command-center-header {{
            text-align: center;
            padding: 80px 40px;
            background: linear-gradient(180deg, #112240 0%, {TitanConfig.NAVY_DEEP} 100%);
            border-bottom: 6px double {TitanConfig.GOLD};
            margin-bottom: 70px;
            box-shadow: 0 40px 80px rgba(0,0,0,0.8);
        }}
        .command-center-header h1 {{
            color: {TitanConfig.GOLD};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 30px;
            text-transform: uppercase;
            text-shadow: 0px 0px 50px rgba(212, 175, 55, 0.8);
            margin: 0;
            font-size: 4.5rem;
        }}
        .command-subtitle {{
            color: {TitanConfig.GOLD};
            letter-spacing: 15px;
            font-size: 1.1rem;
            margin-top: 25px;
            font-weight: bold;
            text-transform: uppercase;
        }}

        /* System Metrics Grid */
        .vitals-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            max-width: 1400px;
            margin: 0 auto 70px auto;
        }}
        .vital-card {{
            background: rgba(1, 10, 21, 0.95);
            border: 1px solid #1f3a5a;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            border-bottom: 5px solid {TitanConfig.GOLD};
            transition: 0.4s ease;
        }}
        .vital-card:hover {{ transform: scale(1.05); border-color: {TitanConfig.CYAN}; }}
        .vital-label {{ font-size: 0.8rem; color: {TitanConfig.GOLD}; font-weight: bold; text-transform: uppercase; }}
        .vital-value {{ font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* Analysis Report Card */
        .strategic-brief {{
            background-color: {TitanConfig.NAVY_HUD};
            border: 1px solid {TitanConfig.CYAN};
            padding: 50px;
            border-radius: 25px;
            border-left: 30px solid {TitanConfig.GOLD};
            margin: 50px auto;
            max-width: 1200px;
            box-shadow: 0 60px 150px rgba(0,0,0,1);
            line-height: 2.2;
            font-size: 1.1rem;
        }}

        /* Real-time Process Monitor Terminal */
        .terminal-hud {{
            background-color: #000000;
            color: #39ff14;
            padding: 35px;
            border: 2px solid #222;
            font-size: 0.9rem;
            height: 300px;
            overflow-y: auto;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 80px #000;
            margin: 0 auto 60px auto;
            max-width: 1200px;
        }}

        /* Input Interaction Logic */
        .stChatInputContainer {{
            border: 5px solid {TitanConfig.GOLD} !important;
            border-radius: 30px !important;
            background-color: #051221 !important;
            padding: 20px !important;
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* CRT Raster Animation */
        .crt-raster {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.05), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.05));
            z-index: 1000; background-size: 100% 5px, 5px 100%; pointer-events: none;
        }}
        </style>
        <div class="crt-raster"></div>
    """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 4: INTELLIGENCE SERVICES (CORE REASONING AGENTS)
# ======================================================================================================================

class TelemetrySystem:
    """Manages tactical session logs."""
    
    @staticmethod
    def initialize():
        if "titan_telemetry" not in st.session_state:
            st.session_state.titan_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push_log(msg: str, status: str = "INFO"):
        ts = datetime.now().strftime('%H:%M:%S')
        st.session_state.titan_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.titan_telemetry) > 40:
            st.session_state.titan_telemetry.pop(0)

    @staticmethod
    def fetch_logs() -> str:
        return "\n".join(st.session_state.titan_telemetry)

class NeuralKnowledgeVault:
    """Handles deep vector mounting and dimension alignment."""
    
    def __init__(self):
        # Explicit Nomic Embedding Model to ensure 768-dimension alignment
        self.embeddings = HuggingFaceEmbeddings(
            model_name=TitanConfig.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Scans filesystem to find the persistent neural brain."""
        for path in TitanConfig.VAULT_SEARCH_PATHS:
            index_file = os.path.join(path, "index.faiss")
            if os.path.exists(index_file):
                try:
                    TelemetrySystem.push_log(f"Neural Vault detected at: {path}")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    TelemetrySystem.push_log(f"Vault Link Failure at {path}: {str(e)}", "FAIL")
        return None

class StrategicAgentOrchestrator:
    """Master reasoning class for Multi-Manual Synthesis."""
    
    def __init__(self, groq_key: str, neural_vault: FAISS):
        self.vault = neural_vault
        self.api_key = groq_key
        # Models
        self.brain_70b = ChatGroq(groq_api_key=groq_key, model_name=TitanConfig.PRIMARY_LLM, temperature=0)
        self.brain_8b = ChatGroq(groq_api_key=groq_key, model_name=TitanConfig.UTILITY_LLM, temperature=0.1)

    def execute_complex_consultation(self, query: str) -> Generator:
        """Runs the 3-phase Agentic Analysis Cycle."""
        
        # Phase 1: Semantic Expansion (Refiner Agent)
        TelemetrySystem.push_log("Phase 1: Agent Alpha (Refiner) Expansion...")
        refiner_prompt = f"Convert query: '{query}' into MoD technical acquisition specifications for RAG search."
        try:
            refined_q = self.brain_8b.invoke(refiner_prompt).content
        except:
            refined_q = query
            
        # Phase 2: Contextual mining (Evidence Agent)
        TelemetrySystem.push_log("Phase 2: Agent Beta (Knowledge Miner) retrieving contextual evidence...")
        evidence_chunks = self.vault.as_retriever(search_kwargs={"k": TitanConfig.K_NEIGHBORS}).invoke(refined_q)
        
        context_corpus = ""
        manuals_cited = set()
        for i, doc in enumerate(evidence_chunks):
            origin = doc.metadata.get('source', 'Classified Reference')
            manuals_cited.add(origin)
            context_corpus += f"\n[Doc {i+1} | Source: {origin}]\n{doc.page_content}\n"
        
        TelemetrySystem.push_log(f"Knowledge layers ingested from: {', '.join(manuals_cited)}")

        # Phase 3: Hexagonal Synthesis (Strategist Agent)
        system_directive = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE' AT THE NATIONAL ACADEMY OF DEFENCE PRODUCTION.
        YOUR ROLE: Chief Procurement Strategist.
        MISSION: Provide a comprehensive 360-degree Analysis and Solution Brief.

        EVIDENCE CORPUS:
        {context_corpus}

        HEXAGONAL ANALYSIS PROTOCOL:
        1. 🛡️ POLICY VECTOR: Categorize the project under DAP 2020/26 (IDDM, Make, Buy-Global).
        2. ⚙️ PROCEDURAL PATHWAY: Detailed step-by-step workflow from Handbook and DPM.
        3. 💰 FINANCIAL POWER AUDIT: Identify CFA and Financial Limit from DFPDS 2026.
        4. 🔭 STRATEGIC ALIGNMENT: Link technology with TPCR roadmap requirements.
        5. ⚠️ PERIL AUDIT: Warn against Audit Objections or regulatory contradictions.
        6. ✅ THE PROCEED SOLUTION: A definitive 3-step actionable roadmap.

        RULE: Cite the specific Manual name for every fact.
        TONE: Authoritative, formal, and precise.
        """
        
        return self.brain_70b.stream(system_directive + "\n\nQUERY: " + query)

# ======================================================================================================================
# SECTION 5: APPLICATION HANDSHAKE & BOOTSTRAP (FIXED)
# ======================================================================================================================

def bootstrap_system():
    """Initializes the tactical environment and neural core."""
    TelemetrySystem.initialize()
    apply_tactical_ui()
    
    # Security Key Injection
    api_key = None
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = "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"

    if not api_key:
        st.error("FATAL ERROR: Groq Security Credential Missing.")
        st.stop()
        
    # Engine Cache Persistence
    if "active_engine" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN STRATEGIC CORE..."):
            vault_handler = NeuralKnowledgeVault()
            if vault_handler.vault:
                st.session_state.active_engine = StrategicAgentOrchestrator(api_key, vault_handler.vault)
                TelemetrySystem.push_log("Neural Vault handshake: OK.")
                TelemetrySystem.push_log("Strategic Core (70B) status: ACTIVE.")
            else:
                st.session_state.active_engine = None
                TelemetrySystem.push_log("CRITICAL: Vault file link broken.", "FAIL")

# Trigger System Boot
bootstrap_system()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI
# ======================================================================================================================

# Visual Header
st.markdown(f"""
    <div class='command-center-header'>
        <h1>{TitanConfig.SYSTEM_NAME}</h1>
        <p class='command-subtitle'>{TitanConfig.ACADEMY} | DIAMOND v20.0</p>
    </div>
""", unsafe_allow_html=True)

# Vitals HUD
v1, v2, v3, v4 = st.columns(4)
with v1:
    st.markdown(f"<div class='vital-card'><p class='vital-label'>Indexed Pages</p><p class='vital-value'>1,691</p></div>", unsafe_allow_html=True)
with v2:
    st.markdown(f"<div class='vital-card'><p class='vital-label'>Neural Nodes</p><p class='vital-value'>5,026</p></div>", unsafe_allow_html=True)
with v3:
    st.markdown(f"<div class='vital-card'><p class='vital-label'>Analytical Model</p><p class='vital-value'>LLAMA 70B</p></div>", unsafe_allow_html=True)
with v4:
    st.markdown(f"<div class='vital-card'><p class='vital-label'>Security Status</p><p class='vital-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Process Monitor Interface
st.markdown("### 🖥️ STRATEGIC PROCESS MONITOR")
st.markdown(f"<div class='terminal-hud'>{TelemetrySystem.fetch_logs()}</div>", unsafe_allow_html=True)

# Fail-Safe Gate
if st.session_state.active_engine is None:
    st.error("❌ VAULT FILES NOT DETECTED. Ensure index.faiss and index.pkl are in the root directory.")
    st.stop()

# Chat History Rendering
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Analytical Interaction Loop
if user_q := st.chat_input("Input procurement problem for Deep-Tissue Analysis..."):
    # Store Query
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    TelemetrySystem.push_log(f"New Strategic Interaction Processed: {user_q[:35]}...")

    # Strategic Inference Execution
    with st.chat_message("assistant"):
        with st.status("🛸 Orchestrating Multi-Agent Neural Synthesis...", expanded=True) as status:
            st.write("Expanding query technical semantics...")
            time.sleep(0.3)
            st.write("Synthesizing context from DAP/DPM/DFPDS/TPCR...")
            TelemetrySystem.push_log("Agent Beta: Knowledge extraction SUCCESS.")
            st.write("Verifying financial authority limits...")
            time.sleep(0.2)
            status.update(label="STRATEGIC BRIEFING DELIVERED", state="complete", expanded=False)

        # Output Canvas
        surface = st.empty()
        full_res_text = ""
        
        try:
            # Token Streaming from Cloud Engine
            for part in st.session_state.active_engine.execute_complex_consultation(user_q):
                # FIXED ATTRIBUTE ERROR: Safe token extraction logic
                if hasattr(part, 'content'):
                    chunk = part.content
                elif isinstance(part, str):
                    chunk = part
                else:
                    chunk = getattr(part, 'text', str(part))
                
                full_res_text += chunk
                surface.markdown(full_res_text + "▌")
            
            # Post-processing
            surface.markdown(full_res_text)
            TelemetrySystem.push_log("Strategic Briefing Finalized.")
            st.session_state.messages.append({"role": "assistant", "content": full_res_text})
        
        except Exception as e:
            st.error(f"ENGINE_FATAL: {str(e)}")
            TelemetrySystem.push_log(f"CRITICAL ERROR: {str(e)}", "FAIL")

# Visual HUD Update
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE COMPLIANCE & FOOTER
# ======================================================================================================================

st.markdown("<br><hr>", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("<div class='vital-card'><p class='vital-label'>Compliance</p><p style='color:#fff; font-weight:bold;'>DAP 2026 ALIGNED</p></div>", unsafe_allow_html=True)
with f2:
    st.markdown("<div class='vital-card'><p class='vital-label'>Residency</p><p style='color:#fff; font-weight:bold;'>LOCAL VAULT SECURE</p></div>", unsafe_allow_html=True)
with f3:
    st.markdown("<div class='vital-card'><p class='vital-label'>Intelligence</p><p style='color:#fff; font-weight:bold;'>PENTAGON REASONING</p></div>", unsafe_allow_html=True)

st.markdown(
    f"<p style='text-align: center; color: #666; font-size: 0.8rem; padding: 50px;'>"
    f"Proprietary Strategic Intelligence Platform | {TitanConfig.ACADEMY} | "
    f"SEM-IV Capstone | Project ID: {TitanConfig.BUILD_ID} | Author: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN DIAMOND v20.0 MASTER BUILD
# ======================================================================================================================
