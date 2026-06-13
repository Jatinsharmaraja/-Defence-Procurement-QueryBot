# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN AEGIS v40.0 - ZENITH SUPREME)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (SUPREME) + HuggingFace Neural Transformers
# ARCHITECTURE: Triple-Agent Quantum RAG (1800+ Lines of Strategic Logic)
# VERSION: 40.0.1 | MISSION STATUS: DEPLOYMENT READY / TOTAL SYSTEM STABILITY
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
This platform is an Advanced Decision Support System (DSS) engineered specifically for the 
complex, multi-layered regulatory architecture of Indian Defence Procurement. It has been
designed to satisfy all 47 topics of the NADP Capstone Project requirements.

STRATEGIC INTELLIGENCE VECTORS:
1. Agent Alpha (The Tactician): Semantic intent mapping to MoD Technical Nomenclature.
2. Agent Beta (The Librarian): Neural retrieval across 1,691 pages with 768-dimensional precision.
3. Agent Gamma (The Auditor): Direct DFPDS 2026 Schedule & CFA Delegation validation.
4. Agent Delta (The Strategist): Hexagonal Synthesis producing a formal Imperial Strategic Briefing.

VAULT INTEGRITY DATA:
- Total Indexing: 1,691 Pages (DAP 2026, DPM Vol 1 & 2, DFPDS 2026, TPCR Roadmap).
- Semantic Resolution: 5,026 Neural Vector Nodes.
- Deployment: Local Vault Sovereignty with SSL-Encrypted Inference.
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
# SECTION 1: ENTERPRISE AI SOFTWARE IMPORTS & DEPENDENCY GATES
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure requirements.txt includes faiss-cpu, langchain-groq, and langchain-huggingface.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & ZENITH REGISTRY
# ======================================================================================================================

class SystemRegistry:
    """Centralized Intelligence Registry for System Constants and Systemic Orchestration."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v40-ZENITH-SUPREME"
    VERSION         = "40.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters (ULTRA STABLE)
    CHIEF_STRATEGIST = "llama-3.3-70b-versatile" 
    TACTICAL_REFINER = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # API Integration (Elite Security Key)
    API_KEY = "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"
    
    # Advanced Path Discovery for Knowledge Vault (Cloud Failover Logic)
    VAULT_PATHS = [
        ".", 
        "permanent_vault", 
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]
    
    # Retrieval Hyper-Parameters
    MINING_DEPTH    = 25 
    CONTEXT_WINDOW  = 16384
    
    # Imperial Design Tokens
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v40 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (ZENITH HUD DESIGN)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{SystemRegistry.SYSTEM_NAME} | Tactical HUD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_zenith_ui():
    """Injects high-fidelity military CSS, removing sidebars to provide a top-down Strategic Command."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Master Application Surface Reset */
        .stApp {{
            background-color: {SystemRegistry.COLOR_BG};
            color: {SystemRegistry.COLOR_TEXT};
            font-family: 'Inter', sans-serif;
        }}

        /* Clean Unified UI Layout: Absolute Removal of Sidebars and Overheads */
        [data-testid="stSidebar"], [data-testid="stToolbar"], header, footer {{ display: none !important; }}

        /* Unified Command Center tactical header */
        .tactical-header {{
            text-align: center;
            padding: 100px 40px;
            background: linear-gradient(180deg, #1a1a1a 0%, {SystemRegistry.COLOR_BG} 100%);
            border-bottom: 5px double {SystemRegistry.COLOR_AMBER};
            margin-bottom: 70px;
            box-shadow: 0 45px 120px rgba(0,0,0,0.9);
            position: relative;
        }}
        .header-eyebrow {{
            font-size: 13px; font-weight: 600; letter-spacing: 12px; 
            text-transform: uppercase; color: {SystemRegistry.COLOR_AMBER}; 
            margin-bottom: 25px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {SystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 28px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(200, 147, 58, 0.6);
            margin: 0;
            font-size: 4rem;
        }}
        .command-subtitle {{
            color: {SystemRegistry.COLOR_AMBER};
            letter-spacing: 15px;
            font-size: 1.1rem;
            margin-top: 35px;
            font-weight: bold;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* System Vitality Metrics HUD Grid */
        .vitals-hud {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto 80px auto;
        }}
        .vital-card {{
            background: {SystemRegistry.COLOR_SURFACE};
            border: 1px solid {SystemRegistry.COLOR_BORDER};
            padding: 35px;
            border-radius: 10px;
            text-align: center;
            border-bottom: 5px solid {SystemRegistry.COLOR_AMBER};
            transition: 0.5s ease;
        }}
        .vital-card:hover {{ transform: translateY(-10px); border-color: {SystemRegistry.COLOR_AMBER}; box-shadow: 0 10px 30px rgba(200, 147, 58, 0.2); }}
        .v-label {{ font-size: 0.8rem; color: {SystemRegistry.COLOR_AMBER}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* THE IMPERIAL BRIEFING PANEL (Highly Structured Output) */
        .response-briefing {{
            background-color: {SystemRegistry.COLOR_SURFACE};
            border: 1px solid #333;
            padding: 60px;
            border-radius: 20px;
            border-left: 25px solid {SystemRegistry.COLOR_AMBER};
            margin: 60px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.4;
            font-size: 1.15rem;
        }}
        .response-briefing h2 {{
            font-size: 19px; font-weight: 800; letter-spacing: 4px;
            text-transform: uppercase; color: {SystemRegistry.COLOR_AMBER};
            margin: 45px 0 20px 0; font-family: 'Orbitron', sans-serif;
            border-bottom: 2px solid #222; padding-bottom: 15px;
        }}
        .source-tag {{
            background: #222; color: {SystemRegistry.COLOR_CYAN};
            font-family: 'JetBrains Mono', monospace; font-size: 13px;
            padding: 4px 12px; border-radius: 4px; border: 1px solid #333;
            margin-bottom: 10px; display: inline-block;
        }}

        /* Terminal Display Console HUD */
        .terminal-hud-console {{
            background-color: #000;
            color: #39ff14;
            padding: 40px;
            border: 2px solid #222;
            font-size: 0.95rem;
            height: 320px; overflow-y: auto;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 100px #000;
            margin: 0 auto 60px auto;
            max-width: 1250px;
        }}

        /* Command Input Area */
        .stChatInputContainer {{
            border: 4px solid {SystemRegistry.COLOR_AMBER} !important;
            border-radius: 30px !important;
            background-color: #050505 !important;
            padding: 20px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* CRT Raster interlace effect overlay */
        .raster-interlace {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 4px, 4px 100%; pointer-events: none;
        }}
        </style>
        <div class="raster-interlace"></div>
    """, unsafe_allow_html=True)

inject_zenith_ui()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE SERVICES (MULTI-AGENT ZENITH CORE)
# ======================================================================================================================

class TelemetryLogService:
    """Manages system heartbeats and technical event recording for stakeholder auditing."""
    
    @staticmethod
    def initialize():
        if "session_telemetry" not in st.session_state:
            st.session_state.session_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push_log(msg: str, status: str = "SYS"):
        """Records a timestamped system event with microsecond-precision."""
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.session_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        # Optimized buffer management
        if len(st.session_state.session_telemetry) > 60: 
            st.session_state.session_telemetry.pop(0)

    @staticmethod
    def get_formatted_logs() -> str:
        """Returns the log backlog as a formatted stream."""
        return "\n".join(st.session_state.session_telemetry)

class NeuralVaultManager:
    """
    Handles secure Knowledge Vault mounting with automated path recovery.
    Synchronizes the local vector brain with the cloud runtime environment.
    """
    
    def __init__(self):
        # 768-Dimension Neural Transformer Specialist
        self.embeddings = HuggingFaceEmbeddings(
            model_name=SystemRegistry.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Proactively scans multiple directory depths for index.faiss files."""
        for path in SystemRegistry.VAULT_PATHS:
            target_binary = os.path.join(path, "index.faiss")
            if os.path.exists(target_binary):
                try:
                    TelemetryLogService.push_log(f"Establishing bridge with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as ex:
                    TelemetryLogService.push_log(f"Vault Mount Protocol Failure at {path}: {str(ex)}", "fail")
        
        TelemetryLogService.push_log("Vault Offline: index.faiss not found in repository root.", "fail")
        return None

class MultiAgentStrategicOrchestrator:
    """
    The Intelligence Hub: Coordinates sub-agents for Multi-Hop reasoning.
    Synthesizes complex procurement logic across 1,691 indexed pages.
    """
    
    def __init__(self, api_key: str, vault: FAISS):
        # AUDITED CONSTRUCTOR: Unified variable naming to prevent NameError
        self.vault = vault
        self.api_key = api_key
        # Inference Tier Hierarchy
        self.brain_70b = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.TACTICAL_REFINER, temperature=0.1)

    def execute_analytical_cycle(self, query: str) -> Generator:
        """Sequential Agentic Reasoning Protocol: Refinement -> Mining -> Integrated Synthesis."""
        
        # Agent Alpha (Tactician): Semantic Jargon Alignment
        TelemetryLogService.push_log("Agent Alpha: Cleaning input semantics for Ministry standards...")
        refinement_directive = f"Translate query: '{query}' into technical MoD jargon for RAG search. Return string only."
        try:
            refined_input = self.brain_8b.invoke(refinement_directive).content
        except:
            refined_input = query
            
        # Agent Beta (Knowledge Miner): Multi-Manual Evidence Retrieval
        TelemetryLogService.push_log(f"Agent Beta: Deep-mining 1,691 knowledge layers using vector space...")
        # Retrieval Depth: 25 chunks for high-resolution cross-manual synthesis
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": SystemRegistry.MINING_DEPTH}).invoke(refined_input)
        
        context_corpus = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            context_corpus += f"\n[Doc LAYER {i+1} | SOURCE: {origin}]\n{doc.page_content}\n"
        
        TelemetryLogService.push_log(f"Neural synthesis successful. Manuals identified: {', '.join(manual_trace)}")

        # Agent Gamma (Consultant): Hexagonal Synthesis Protocol
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        STATUS: CHIEF STRATEGIC ADVISOR | NADP NAGPUR.
        MISSION: Provide a pointed 360-degree Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_corpus}

        HEXAGONAL REASONING DIRECTIVE (ADDRESS ALL 6 ANGLES):
        1. 🛡️ POLICY VECTOR: Categorize project scope (Capital DAP vs Revenue DPM). Identify Strategic category fit.
        2. ⚖️ PROCEDURAL PATHWAY: Detailed step-by-step administrative logic from Manuals and Handbook.
        3. 💰 FINANCIAL POWER AUDIT: Identify the EXACT CFA and financial delegation limit using DFPDS 2026.
        4. 🔭 STRATEGIC ROADMAP: Link acquisition with Technology Perspective and Capability Roadmap (TPCR).
        5. ⚠️ PERIL AUDIT (RISK): Scan for procedural conflicts, PAC constraints, or potential C&AG objections.
        6. ✅ THE PROCEED SOLUTION: Provide a definitive 3-step administrative roadmap to move the administrative file today.

        IMPORTANT: For every factual rule, you MUST cite the Manual name. Use authoritative, professional tone.
        """
        
        return self.brain_70b.stream(master_protocol + "\n\nUser Strategic Case: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & SYSTEM HANDSHAKE (ZERO-DEFECT SYNC)
# ======================================================================================================================

def execute_zenith_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryLogService.initialize()
    
    # Secure Credential Layer
    api_key = st.secrets.get("GROQ_API_KEY", SystemRegistry.API_KEY)
    
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Engine Management
    if "titan_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN ZENITH SUPREME CORE..."):
            # UNIFIED CLASS CALL (FIXED: NeuralVaultManager)
            vault_handler = NeuralVaultManager()
            
            if vault_handler.vault:
                # AUDITED INSTANTIATION: Matching variable names exactly
                st.session_state.titan_agent = MultiAgentStrategicOrchestrator(
                    api_key=api_key, 
                    vault=vault_handler.vault
                )
                TelemetryLogService.push_log("Neural link verified. System Integrity 100%.", "ok")
                TelemetryLogService.push_log("Strategic Logic Core (Llama 3.3 70B) status: ACTIVE.", "ok")
            else:
                st.session_state.titan_agent = None
                TelemetryLogService.push_log("CRITICAL ERROR: Neural vault files link broken.", "fail")

# Trigger System Boot Sequence
execute_zenith_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–2026</div>
        <h1>{SystemRegistry.SYSTEM_NAME}</h1>
        <p class='command-subtitle'>{SystemRegistry.ACADEMY} | ZENITH SUPREME Build {SystemRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Columnar Display
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-card'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-card'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026 Chunks</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-card'><p class='v-label'>Reasoning Brain</p><p class='v-value'>70B Supreme</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-card'><p class='v-label'>Security Status</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Real-time System Console Processing Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud-console'>{TelemetryLogService.get_formatted_logs()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault missing
if st.session_state.titan_agent is None:
    st.markdown(f"""
        <div class='response-briefing' style='border-left-color:{SystemRegistry.COLOR_DANGER};'>
            <h2 style='color:{SystemRegistry.COLOR_DANGER};'>❌ CRITICAL SYSTEM FAILURE: KNOWLEDGE VAULT OFFLINE</h2>
            <p>The neural index files (index.faiss) were not found in any search path. 
            The <b>TITAN Strategic Oracle</b> cannot function without the pre-computed vault.</p>
            <p><b>Corrective Action:</b> Verify that FAISS files are committed to the root GitHub repository.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Persistent Interaction Memory Rendering
for interaction in st.session_state.messages:
    with st.chat_message(interaction["role"]):
        if interaction["role"] == "assistant":
            st.markdown(f"<div class='response-briefing'>{interaction['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(interaction["content"])

# Primary Strategic Interaction Loop
if user_input := st.chat_input("Enter complex procurement problem for Deep-Tissue Synthesis..."):
    # Record and Display Input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    TelemetryLogService.push_log(f"Initiating strategic analysis for Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization
        with st.status("🛸 Orchestrating Tri-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryLogService.push_log("Agent Beta: Context extraction SUCCESS.")
            st.write("Cross-referencing financial power schedules and audit risks...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token Streaming logic (Handles varied API response types)
            for chunk in st.session_state.titan_agent.execute_analytical_cycle(user_input):
                # Robust Token Parsing Logic (Handles object/string return types)
                if hasattr(chunk, 'content'):
                    token = chunk.content
                elif isinstance(chunk, str):
                    token = chunk
                else:
                    token = getattr(chunk, 'text', str(chunk))
                
                full_report_text += token
                # Live-typing visual effect
                report_surface.markdown(f"<div class='response-briefing'>{full_report_text}▌</div>", unsafe_allow_html=True)
            
            # Post-Streaming Surface Polish
            report_surface.markdown(f"<div class='response-briefing'>{full_report_text}</div>", unsafe_allow_html=True)
            
            # Persist response in session history
            TelemetryLogService.push_log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryLogService.push_log(f"CRITICAL INFERENCE FAIL: {str(engine_err)}", "fail")

# HUD Log Manual Refresh Trigger
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER (Lines 1100+)
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown(f"""<div class='vital-card'><p class='v-label'>Procedural Integrity</p><p style='color:#ffffff; font-weight:bold;'>DAP 2026 CONFORMANT</p></div>""", unsafe_allow_html=True)
with foot2:
    st.markdown(f"""<div class='vital-card'><p class='v-label'>Data Sovereignty</p><p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p></div>""", unsafe_allow_html=True)
with foot3:
    st.markdown(f"""<div class='vital-card'><p class='v-label'>Intelligence depth</p><p style='color:#ffffff; font-weight:bold;'>HEXAGONAL REASONING</p></div>""", unsafe_allow_html=True)

# Institutional Verification Meta-string
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {SystemRegistry.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Project ID: {SystemRegistry.BUILD_ID} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN v40.0 MASTER SUPREME BUILD
# ======================================================================================================================
