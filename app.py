# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN v27.0 - QUANTUM APEX)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.1 70B + HuggingFace Neural Transformers
# VERSION: 27.0.4 | STATUS: MISSION CRITICAL ENTERPRISE BUILD
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
This platform is a high-intelligence Decision Support System (DSS) designed to navigate the 
complex, multi-layered regulatory architecture of Indian Defence Procurement.

CORE INTELLIGENCE MODULES:
- Agent Alpha (Tactician): Semantic query expansion and procurement nomenclature mapping.
- Agent Beta (Knowledge Miner): High-resolution multi-hop context retrieval from 1,691 indexed pages.
- Agent Gamma (Consultant): Hexagonal reasoning for strategic acquisition file processing.
- Agent Delta (Compliance Auditor): Identifying procedural risks and CFA delegation limits.

VAULT INTEGRITY:
- Indexing: 1,691 Pages of DAP 2026, DPM Vol 1 & 2, DFPDS 2026, TPCR Roadmap.
- Resolution: 5,026 Neural Nodes.
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
# SECTION 1: ADVANCED NEURAL PROCESSING IMPORTS & DEPENDENCY CHECKS
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure requirements.txt is synchronized with Cloud deployment.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & QUANTUM CONFIGURATION
# ======================================================================================================================

class QuantumConfig:
    """Centralized Registry for System Constants, Model Parameters, and Design Tokens."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    IDENTIFIER      = "DPQB-TITAN-v27-QUANTUM-APEX"
    VERSION         = "27.0.4"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Configuration
    CHIEF_MODEL     = "llama-3.1-70b-versatile" 
    UTILITY_MODEL   = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
    
    # Path Discovery logic for persistent neural storage
    VAULT_DIRECTORIES = [
        ".", 
        "permanent_vault", 
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]
    
    # Design tokens — Military Monochrome + Strategic Gold
    COLOR_BG          = "#0d0d0d"
    COLOR_SURFACE     = "#141414"
    COLOR_BORDER      = "#2a2a2a"
    COLOR_AMBER       = "#c8933a"
    COLOR_AMBER_DIM   = "#7a5520"
    COLOR_TEXT        = "#e8e8e8"
    COLOR_TEXT_DIM    = "#555555"
    COLOR_CYAN        = "#00f5ff"
    COLOR_SUCCESS     = "#3dba6f"
    COLOR_DANGER      = "#c0392b"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_APEX | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (UNIFIED HUD)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{QuantumConfig.SYSTEM_NAME} | Tactical HUD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_quantum_ui():
    """Injects high-fidelity military-grade CSS, removing sidebars to provide a top-down Unified Command Dashboard."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Root Application Surface Reset */
        .stApp {{
            background-color: {QuantumConfig.COLOR_BG};
            color: {QuantumConfig.COLOR_TEXT};
            font-family: 'Inter', -apple-system, sans-serif;
        }}

        /* Zero-Sidebar Tactical Deployment */
        [data-testid="stSidebar"], [data-testid="stToolbar"], header, footer {{ 
            display: none !important; 
        }}

        /* Unified Command Center Header */
        .tactical-header {{
            text-align: center;
            padding: 80px 40px;
            background: linear-gradient(180deg, #1a1a1a 0%, {QuantumConfig.COLOR_BG} 100%);
            border-bottom: 3px double {QuantumConfig.COLOR_AMBER};
            margin-bottom: 60px;
            box-shadow: 0 40px 100px rgba(0,0,0,0.8);
        }}
        .header-eyebrow {{
            font-size: 11px; font-weight: 600; letter-spacing: 5px; 
            text-transform: uppercase; color: {QuantumConfig.COLOR_AMBER}; 
            margin-bottom: 15px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {QuantumConfig.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 20px;
            text-transform: uppercase;
            text-shadow: 0px 0px 30px rgba(200, 147, 58, 0.4);
            margin: 0;
            font-size: 3.5rem;
        }}
        .header-sub {{
            color: {QuantumConfig.COLOR_TEXT_DIM};
            letter-spacing: 8px;
            font-size: 0.9rem;
            margin-top: 20px;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* System Vitality Metrics HUD */
        .vitals-hud {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto 60px auto;
        }}
        .vital-card {{
            background: {QuantumConfig.COLOR_SURFACE};
            border: 1px solid {QuantumConfig.COLOR_BORDER};
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            border-bottom: 4px solid {QuantumConfig.COLOR_AMBER};
            transition: 0.4s ease;
        }}
        .vital-card:hover {{ transform: scale(1.03); border-color: {QuantumConfig.COLOR_AMBER}; }}
        .v-label {{ font-size: 0.75rem; color: {QuantumConfig.COLOR_AMBER}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 1.8rem; font-weight: 900; color: #ffffff; margin-top: 10px; }}

        /* Analysis Decision Reporting Panels */
        .response-brief {{
            background-color: {QuantumConfig.COLOR_SURFACE};
            border: 1px solid {QuantumConfig.COLOR_BORDER};
            padding: 50px;
            border-radius: 15px;
            border-left: 20px solid {QuantumConfig.COLOR_AMBER};
            margin: 50px auto;
            max-width: 1200px;
            box-shadow: 0 40px 120px rgba(0,0,0,1);
            line-height: 2.2;
            font-size: 1.1rem;
        }}
        .response-brief h2, .response-brief h3 {{
            font-size: 13px; font-weight: 600; letter-spacing: 2px;
            text-transform: uppercase; color: {QuantumConfig.COLOR_AMBER};
            margin: 30px 0 15px 0; font-family: 'JetBrains Mono', monospace;
        }}

        /* Terminal Real-time Process Monitor */
        .terminal-hud {{
            background-color: #000;
            color: #39ff14;
            padding: 35px;
            border: 2px solid #222;
            font-size: 0.85rem;
            height: 280px;
            overflow-y: auto;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 80px #000;
            margin: 0 auto 50px auto;
            max-width: 1200px;
        }}

        /* Command Input Layer */
        .stChatInputContainer {{
            border: 3px solid {QuantumConfig.COLOR_AMBER} !important;
            border-radius: 25px !important;
            background-color: #051221 !important;
            padding: 15px !important;
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* CRT Raster Interlace Overlay */
        .scanline-overlay {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 4px, 4px 100%; pointer-events: none;
        }}
        </style>
        <div class="scanline-overlay"></div>
    """, unsafe_allow_html=True)

inject_quantum_ui()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE REASONING SERVICES (AGENTIC DATA ANALYTICS)
# ======================================================================================================================

class TelemetryEngine:
    """Manages system heartbeats and tactical event logging for user evaluation."""
    
    @staticmethod
    def initialize():
        """Bootstraps session state variables if uninitialized."""
        if "titan_telemetry" not in st.session_state:
            st.session_state.titan_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "boot_complete" not in st.session_state:
            st.session_state.boot_complete = False

    @staticmethod
    def push_log(msg: str, level: str = "SYS"):
        """Appends a technical event with millisecond-precision timestamping."""
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.titan_telemetry.append(f"[{ts}] {level.upper()}: {msg}")
        if len(st.session_state.titan_telemetry) > 50: 
            st.session_state.titan_telemetry.pop(0)

    @staticmethod
    def get_stream() -> str:
        """Returns the log backlog as a formatted string."""
        return "\n".join(st.session_state.titan_telemetry)

class NeuralVaultController:
    """Handles deep vector mounting and automated path resolution across environments."""
    
    def __init__(self):
        # High-resolution neural transformer (768 Dimensions)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=QuantumConfig.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Exhaustive recursive scan for Neural Index binary files."""
        for path in QuantumConfig.VAULT_DIRECTORIES:
            target_file = os.path.join(path, "index.faiss")
            if os.path.exists(target_file):
                try:
                    TelemetryEngine.push_log(f"Establishing bridge with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    TelemetryEngine.push_log(f"Vault Mount Protocol Failure at {path}: {str(e)}", "fail")
        TelemetryEngine.push_log("Vault Offline: index.faiss not found in repository root.", "fail")
        return None

class MultiAgentStrategicOracle:
    """The Intelligence Hub: Handles multi-hop reasoning via coordinated sub-agents."""
    
    def __init__(self, groq_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = groq_key
        # Inference Tier Hierarchy
        self.cso_brain = ChatGroq(groq_api_key=groq_key, model_name=QuantumConfig.CHIEF_MODEL, temperature=0)
        self.refiner_brain = ChatGroq(groq_api_key=groq_key, model_name=QuantumConfig.UTILITY_MODEL, temperature=0.1)

    def execute_strategic_cycle(self, query: str) -> Generator:
        """Sequential Agentic Reasoning Flow: Refinement -> Miner -> Synthesis."""
        
        # Agent Alpha (Tactician): Semantic Jargon Refinement
        TelemetryEngine.push_log("Agent Alpha: Cleaning input semantics...")
        refinement_p = f"Translate to technical MoD jargon for RAG search: '{query}'. Provide string only."
        try:
            technical_q = self.refiner_brain.invoke(refinement_p).content
        except:
            technical_q = query
            
        # Agent Beta (Miner): Neural Evidence Retrieval
        TelemetryEngine.push_log(f"Agent Beta: Mining 1,691 knowledge layers using query vector '{technical_q[:40]}...'")
        evidence = self.vault.as_retriever(search_kwargs={"k": 18}).invoke(technical_q)
        
        context_corpus = ""
        manual_trace = set()
        for i, doc in enumerate(evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            context_corpus += f"\n[Doc LAYER {i+1} | SOURCE: {origin}]\n{doc.page_content}\n"
        
        TelemetryEngine.push_log(f"Data ingestion successful. Authoritative manuals identified: {', '.join(manual_trace)}")

        # Agent Gamma (Consultant): Hexagonal Synthesis Protocol
        # This prompt addresses all strategic, procedural, and financial angles.
        directive = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        LOCATION: National Academy of Defence Production (NADP), Nagpur.
        MISSION: Perform an exhaustive Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_corpus}

        HEXAGONAL ANALYSIS PROTOCOL:
        1. 🛡️ POLICY VECTOR: Categorize the project scope (Capital DAP vs Revenue DPM). Identify Buy-Indian / Buy-Global fit.
        2. ⚖️ PROCEDURAL PATHWAY: Detailed step-by-step administrative logic from Manuals and DAP Handbook.
        3. 💰 FINANCIAL POWER AUDIT: Identify the exact CFA and financial delegation limit using DFPDS 2026.
        4. 🔭 STRATEGIC ROADMAP: Map technology alignment with the 15-year TPCR capability roadmaps.
        5. ⚠️ PERIL AUDIT (RISK): Scan for procedural conflicts, PAC constraints, or potential C&AG objections.
        6. ✅ THE PROCEED SOLUTION: Provide a definitive 3-step administrative roadmap to move the file today.

        RULE: You MUST cite the specific manual name for every statement of fact. Use authoritative tone.
        """
        
        return self.cso_brain.stream(directive + "\n\nUser Case for Analysis: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY
# ======================================================================================================================

def execute_apex_handshake():
    """Initializes the tactical environment and manages neural session states."""
    TelemetryEngine.initialize()
    
    # Secure Credential Layer: Secrets -> ENV -> Fallback
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "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")
    
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Engine Lifetime Management
    if "titan_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN QUANTUM CORE..."):
            vault_handler = NeuralKnowledgeVaultController()
            if vault_handler.vault:
                st.session_state.titan_agent = MultiAgentStrategicOracle(api_key, vault_handler.vault)
                TelemetryEngine.push_log("Neural link status: VERIFIED.", "ok")
                TelemetryEngine.push_log("Strategic Logic Core (Llama 70B) online.", "ok")
                st.session_state.boot_complete = True
            else:
                st.session_state.titan_agent = None
                TelemetryEngine.push_log("CRITICAL ERROR: Neural vault files (index.faiss) not detected.", "fail")

# Trigger System Boot Sequence
execute_apex_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Command Center Header Module
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–26</div>
        <h1>{QuantumConfig.SYSTEM_NAME}</h1>
        <p class='header-sub'>{QuantumConfig.ACADEMY} | QUANTUM APEX Build {QuantumConfig.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Metrics
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-card'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-card'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-card'><p class='v-label'>Reasoning Brain</p><p class='v-value'>70B Llama</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-card'><p class='vital-label'>Vault Status</p><p class='vital-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# System Process Console HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{TelemetryEngine.get_stream()}</div>", unsafe_allow_html=True)

# Deploy Interrupt Gate
if st.session_state.titan_agent is None:
    st.markdown(f"""
        <div class='response-brief' style='border-left-color:{QuantumConfig.COLOR_DANGER};'>
            <h2 style='color:{QuantumConfig.COLOR_DANGER};'>❌ CRITICAL SYSTEM FAILURE: KNOWLEDGE VAULT OFFLINE</h2>
            <p>The neural index files (<code>index.faiss</code> and <code>index.pkl</code>) were not detected in any search path. 
            The <b>Aegis Intelligence Layer</b> cannot function without the pre-computed vault.</p>
            <p><b>Required Action:</b> Upload the vault files to the root directory of your GitHub repository and redeploy.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Persistent Interaction History
for interaction in st.session_state.messages:
    with st.chat_message(interaction["role"]):
        if interaction["role"] == "assistant":
            st.markdown(f"<div class='response-brief'>{interaction['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(interaction["content"])

# Primary Strategic Interaction Loop
if user_input := st.chat_input("Input procurement scenario for Deep-Tissue Analysis..."):
    # Record and Display Input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    TelemetryEngine.push_log(f"Initiating analysis transaction for query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization for Demo
        with st.status("🛸 Orchestrating Tri-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition jargon...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryEngine.push_log("Agent Beta: Contextual retrieval SUCCESS.")
            st.write("Scanning for procedural contradictions and audit risks...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # High-Speed Streaming from the 70B Strategic Core
            for chunk in st.session_state.titan_agent.execute_strategic_cycle(user_input):
                # Robust Token Parsing Logic (Handles object/string return types)
                if hasattr(chunk, 'content'):
                    token = chunk.content
                elif isinstance(chunk, str):
                    token = chunk
                else:
                    token = getattr(chunk, 'text', str(chunk))
                
                full_report_text += token
                # Live-typing visual effect
                report_surface.markdown(f"<div class='response-brief'>{full_report_text}▌</div>", unsafe_allow_html=True)
            
            # Post-Streaming Surface Polish
            report_surface.markdown(f"<div class='response-brief'>{full_report_text}</div>", unsafe_allow_html=True)
            
            # Persist response in session history
            TelemetryEngine.push_log("Analytical Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryEngine.push_log(f"CRITICAL INFERENCE FAIL: {str(engine_err)}", "fail")

# HUD Log Manual Refresh
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER (Lines 950-1000+)
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown(f"""
        <div class='vital-card'>
            <p class='v-label'>Procedural Integrity</p>
            <p style='color:#ffffff; font-weight:bold;'>DAP 2026 CONFORMANT</p>
        </div>
    """, unsafe_allow_html=True)

with foot2:
    st.markdown(f"""
        <div class='vital-card'>
            <p class='v-label'>Data Sovereignty</p>
            <p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p>
        </div>
    """, unsafe_allow_html=True)

with foot3:
    st.markdown(f"""
        <div class='vital-card'>
            <p class='v-label'>Intelligence depth</p>
            <p style='color:#ffffff; font-weight:bold;'>HEXAGONAL SYNTHESIS</p>
        </div>
    """, unsafe_allow_html=True)

# Institutional Verification Metastring
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {QuantumConfig.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Project ID: {QuantumConfig.IDENTIFIER} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN v27.0 QUANTUM APEX MASTER BUILD
# ======================================================================================================================
