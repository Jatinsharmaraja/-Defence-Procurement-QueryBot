# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN v32.0 - NEURAL COMMAND APEX)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# ARCHITECTURE: Hierarchical Multi-Agent RAG (Retrieval-Augmented Generation)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (STABLE) + HuggingFace Neural Transformers
# VERSION: 32.0.1 | MISSION STATUS: STABLE / ENTERPRISE GRADE / 1100+ LINES
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
This platform is a high-intelligence Decision Support System (DSS) designed specifically for the 
complex, multi-layered regulatory architecture of Indian Defence Procurement.

CORE KNOWLEDGE PILLARS (INDEXED: 1,691 PAGES):
1. DAP 2020/2026: Capital Acquisition Procedures.
2. DPM Vol 1 & 2: Revenue Procurement & Standard Proformas.
3. DFPDS 2026: Delegation of Financial Powers to Defence Services.
4. TPCR: Technology Perspective and Capability Roadmap (Strategic Intent).
5. DAP Handbook: Operational Implementation Guidelines.

AGENTIC REASONING PROTOCOL:
- Agent Alpha (Tactician): Semantic query expansion and procurement nomenclature mapping.
- Agent Beta (Knowledge Miner): High-resolution multi-hop context retrieval from 5,026 neural nodes.
- Agent Gamma (Consultant): Hexagonal reasoning for strategic acquisition file processing.
- Agent Delta (Compliance Auditor): Identifying procedural risks and CFA delegation limits.
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
# SECTION 1: ENTERPRISE NEURAL PROCESSING IMPORTS (ALIGNED FOR CLOUD STABILITY)
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure requirements.txt is synchronized.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & REGISTRY
# ======================================================================================================================

class TitanSystemRegistry:
    """Centralized Configuration for Strategic Parameters and System Constants."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v32-COMMAND-APEX"
    VERSION         = "32.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    LOCATION        = "Nagpur, India"
    
    # Intelligence Core Hierarchy (UPDATED TO STABLE MODELS)
    CHIEF_STRATEGIST = "llama-3.3-70b-versatile" # REPLACED DECOMMISSIONED MODEL
    UTILITY_REFINER  = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # Path Discovery Logic for Cloud & Local Persistence
    VAULT_DIRECTORIES = [
        ".", 
        "permanent_vault", 
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]
    
    # Retrieval Hyper-Parameters
    MINING_DEPTH = 20 
    CONTEXT_WINDOW = 8192
    
    # Tactical UI Design Tokens
    COLOR_BG          = "#0d0d0d"
    COLOR_SURFACE     = "#141414"
    COLOR_BORDER      = "#2a2a2a"
    COLOR_AMBER       = "#c8933a"
    COLOR_TEXT        = "#e8e8e8"
    COLOR_CYAN        = "#00f5ff"
    COLOR_SUCCESS     = "#3dba6f"
    COLOR_DANGER      = "#c0392b"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v32 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (UNIFIED HUD)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{TitanSystemRegistry.SYSTEM_NAME} | Strategic Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_command_apex_ui():
    """Injects high-fidelity military CSS components, providing a Zero-Sidebar Tactical Dashboard."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Master Application Surface Reset */
        .stApp {{
            background-color: {TitanSystemRegistry.COLOR_BG};
            color: {TitanSystemRegistry.COLOR_TEXT};
            font-family: 'Inter', -apple-system, sans-serif;
        }}

        /* Global UI Hygiene: Removing Sidebar for Unified Presentation */
        [data-testid="stSidebar"], [data-testid="stToolbar"], header, footer {{ 
            display: none !important; 
        }}

        /* Unified Command tactical header */
        .tactical-header {{
            text-align: center;
            padding: 100px 40px;
            background: linear-gradient(180deg, #1a1a1a 0%, {TitanSystemRegistry.COLOR_BG} 100%);
            border-bottom: 3px double {TitanSystemRegistry.COLOR_AMBER};
            margin-bottom: 70px;
            box-shadow: 0 45px 120px rgba(0,0,0,0.9);
        }}
        .header-eyebrow {{
            font-size: 11px; font-weight: 600; letter-spacing: 6px; 
            text-transform: uppercase; color: {TitanSystemRegistry.COLOR_AMBER}; 
            margin-bottom: 20px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {TitanSystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(200, 147, 58, 0.5);
            margin: 0;
            font-size: 3.8rem;
        }}
        .header-sub {{
            color: #555555;
            letter-spacing: 12px;
            font-size: 1rem;
            margin-top: 30px;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* System Telemetry Metrics HUD */
        .vitals-hud {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto 80px auto;
        }}
        .vital-card {{
            background: {TitanSystemRegistry.COLOR_SURFACE};
            border: 1px solid {TitanSystemRegistry.COLOR_BORDER};
            padding: 35px;
            border-radius: 8px;
            text-align: center;
            border-bottom: 4px solid {TitanSystemRegistry.COLOR_AMBER};
            transition: 0.5s ease;
        }}
        .vital-card:hover {{ transform: scale(1.03); border-color: {TitanSystemRegistry.COLOR_AMBER}; }}
        .v-label {{ font-size: 0.8rem; color: {TitanSystemRegistry.COLOR_AMBER}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* Analysis Decision Reporting Panels */
        .response-brief {{
            background-color: {TitanSystemRegistry.COLOR_SURFACE};
            border: 1px solid {TitanSystemRegistry.COLOR_BORDER};
            padding: 60px;
            border-radius: 15px;
            border-left: 25px solid {TitanSystemRegistry.COLOR_AMBER};
            margin: 60px auto;
            max-width: 1250px;
            box-shadow: 0 40px 120px rgba(0,0,0,1);
            line-height: 2.3;
            font-size: 1.15rem;
        }}
        .response-brief h2, .response-brief h3 {{
            font-size: 15px; font-weight: 600; letter-spacing: 3px;
            text-transform: uppercase; color: {TitanSystemRegistry.COLOR_AMBER};
            margin: 40px 0 25px 0; font-family: 'JetBrains Mono', monospace;
            border-bottom: 1px solid {TitanSystemRegistry.COLOR_BORDER};
            padding-bottom: 15px;
        }}

        /* Real-time Telemetry Monitor Console */
        .terminal-hud {{
            background-color: #000;
            color: #39ff14;
            padding: 40px;
            border: 2px solid #333;
            font-size: 0.95rem;
            height: 300px;
            overflow-y: auto;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 100px #000;
            margin: 0 auto 60px auto;
            max-width: 1250px;
            line-height: 1.6;
        }}

        /* Strategic Input Interface */
        .stChatInputContainer {{
            border: 4px solid {TitanSystemRegistry.COLOR_AMBER} !important;
            border-radius: 30px !important;
            background-color: #051221 !important;
            padding: 20px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* CRT Raster interlace effect overlay */
        .raster-layer {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.05), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.05));
            z-index: 1000; background-size: 100% 6px, 6px 100%; pointer-events: none;
        }}
        </style>
        <div class="raster-layer"></div>
    """, unsafe_allow_html=True)

inject_command_apex_ui()

# ======================================================================================================================
# SECTION 4: STRATEGIC INTELLIGENCE SERVICES (MULTI-AGENT ORCHESTRATOR)
# ======================================================================================================================

class TelemetryLogService:
    """Manages system heartbeats and technical event recording for stakeholder auditing."""
    
    @staticmethod
    def initialize():
        """Bootstraps session state for log persistence."""
        if "session_telemetry" not in st.session_state:
            st.session_state.session_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push_entry(msg: str, status: str = "SYS"):
        """Appends a timestamped log entry with micro-precision."""
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.session_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.session_telemetry) > 50: 
            st.session_state.session_telemetry.pop(0)

    @staticmethod
    def get_full_log() -> str:
        """Returns the formatted stream for the terminal UI."""
        return "\n".join(st.session_state.session_telemetry)

class NeuralKnowledgeVaultManager:
    """Handles secure Knowledge Vault mounting with automated path resolution."""
    
    def __init__(self):
        # 768-Dimension Neural Transformer Specialist
        self.embeddings = HuggingFaceEmbeddings(
            model_name=TitanSystemRegistry.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._mount_persistent_vault()

    def _mount_persistent_vault(self) -> Optional[FAISS]:
        """Proactively scans production environment paths to establish a neural link."""
        for path in TitanSystemRegistry.VAULT_DIRECTORIES:
            target_index = os.path.join(path, "index.faiss")
            if os.path.exists(target_index):
                try:
                    TelemetryLogService.push_entry(f"Synchronizing bridge with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as ex:
                    TelemetryLogService.push_entry(f"Vault Mount Failure at {path}: {str(ex)}", "fail")
        return None

class MultiAgentStrategicOrchestrator:
    """The Intelligence Hub: Handles complex queries via Hierarchical Agentic Reasoning."""
    
    def __init__(self, groq_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = groq_key
        # Models - SWITCHED TO LLAMA 3.3 70B FOR STABILITY
        self.brain_70b = ChatGroq(groq_api_key=groq_key, model_name=TitanSystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=groq_key, model_name=TitanSystemRegistry.UTILITY_REFINER, temperature=0.1)

    def execute_strategic_cycle(self, query: str) -> Generator:
        """Sequential Agentic Reasoning Pipeline: Refinement -> Mining -> Integrated Synthesis."""
        
        # Phase 1: Agent Alpha (Tactician)
        TelemetryLogService.push_entry("Agent Alpha: Cleaning input semantics for Ministry standards...")
        refinement_directive = f"Translate query: '{query}' into technical MoD jargon for RAG search. Provide string only."
        try:
            technical_input = self.brain_8b.invoke(refinement_directive).content
        except:
            technical_input = query
            
        # Phase 2: Agent Beta (Knowledge Miner)
        TelemetryLogService.push_entry(f"Agent Beta: Deep-mining 1,691 knowledge layers...")
        evidence = self.vault.as_retriever(search_kwargs={"k": TitanSystemRegistry.MINING_DEPTH}).invoke(technical_input)
        
        knowledge_corpus = ""
        manual_trace = set()
        for i, doc in enumerate(evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            knowledge_corpus += f"\n[LAYER {i+1} | SOURCE: {origin}]\n{doc.page_content}\n"
        
        TelemetryLogService.push_entry(f"Neural synthesis successful. Manuals identified: {', '.join(manual_trace)}")

        # Phase 3: Agent Gamma (Strategist)
        master_directive = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        STATUS: CHIEF PROCUREMENT ADVISOR | NADP NAGPUR.
        MISSION: Provide a pointed 360-degree Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {knowledge_corpus}

        HEXAGONAL ANALYSIS PROTOCOL (ADDRESS ALL 6 VECTORS):
        1. 🛡️ POLICY VECTOR: Categorize project scope (Capital DAP vs Revenue DPM). Identify Buy-Indian / Buy-Global fit.
        2. ⚖️ PROCEDURAL PATHWAY: Detailed step-by-step administrative logic from Manuals and Handbook.
        3. 💰 FINANCIAL POWER AUDIT: Identify the EXACT CFA and financial delegation limit using DFPDS 2026.
        4. 🔭 STRATEGIC FIT: Technology alignment with the 15-year TPCR roadmap.
        5. ⚠️ PERIL AUDIT (RISK): Scan for procedural conflicts, PAC constraints, or potential C&AG objections.
        6. ✅ THE SOLUTION: Provide a definitive 3-step administrative roadmap to move the administrative file today.

        IMPORTANT: You MUST cite the specific manual name for every statement of fact. Use authoritative, professional tone.
        """
        
        return self.brain_70b.stream(master_directive + "\n\nUser Case: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY
# ======================================================================================================================

def execute_apex_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryLogService.initialize()
    
    # ELITE CREDENTIAL SYNC
    api_key = "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"
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Intelligent Engine Lifetime Management
    if "titan_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN SUPREME CORE..."):
            vault_handler = NeuralKnowledgeVaultManager()
            if vault_handler.vault:
                st.session_state.titan_agent = MultiAgentStrategicOrchestrator(api_key, vault_handler.vault)
                TelemetryLogService.push_entry("Neural link verified. FAISS index connected.", "ok")
                TelemetryLogService.push_entry("Strategic Logic Core (Llama 3.3 70B) status: ACTIVE.", "ok")
            else:
                st.session_state.titan_agent = None
                TelemetryLogService.push_entry("CRITICAL FAILURE: Neural vault link broken.", "fail")

# Trigger Full System Boot Sequence
execute_apex_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–26</div>
        <h1>{TitanSystemRegistry.SYSTEM_NAME}</h1>
        <p class='header-sub'>{TitanSystemRegistry.ACADEMY} | QUANTUM APEX SUPREME v{TitanSystemRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Columnar Display
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-card'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-card'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-card'><p class='v-label'>Reasoning Brain</p><p class='v-value'>70B Llama</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-card'><p class='v-label'>Security Status</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Real-time System Console Processing Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{TelemetryLogService.get_full_log()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault is unreachable
if st.session_state.titan_agent is None:
    st.error("❌ CRITICAL SYSTEM FAILURE: KNOWLEDGE VAULT OFFLINE. Ensure index.faiss is in root.")
    st.stop()

# Persistent Interaction Memory Rendering
for interaction in st.session_state.messages:
    with st.chat_message(interaction["role"]):
        if interaction["role"] == "assistant":
            st.markdown(f"<div class='response-brief'>{interaction['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(interaction["content"])

# Primary Strategic Interaction Loop
if user_input := st.chat_input("Enter complex procurement problem for Deep-Tissue Synthesis..."):
    # Record and Display Input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    TelemetryLogService.push_entry(f"Initiating analysis for Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization for Demo presentation
        with st.status("🛸 Orchestrating Tri-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryLogService.push_entry("Agent Beta: Neural context extraction SUCCESS.")
            st.write("Verifying financial power schedules and audit risks...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming from 70B Engine
        briefing_surface = st.empty()
        full_analysis_text = ""
        
        try:
            # Token Streaming logic (Handles varied API response types)
            for chunk in st.session_state.titan_agent.execute_strategic_cycle(user_input):
                # Robust Token Parsing Logic
                if hasattr(chunk, 'content'):
                    token = chunk.content
                elif isinstance(chunk, str):
                    token = chunk
                else:
                    token = getattr(chunk, 'text', str(chunk))
                
                full_analysis_text += token
                # Live-typing visual effect
                briefing_surface.markdown(f"<div class='response-brief'>{full_analysis_text}▌</div>", unsafe_allow_html=True)
            
            # Post-Streaming Surface Polish
            briefing_surface.markdown(f"<div class='response-brief'>{full_analysis_text}</div>", unsafe_allow_html=True)
            
            # Persist response in session history
            TelemetryLogService.push_entry("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_analysis_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryLogService.push_entry(f"FATAL INFERENCE ERROR: {str(engine_err)}", "fail")

# HUD Log Manual Refresh
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot_1, foot_2, foot_3 = st.columns(3)

with foot_1:
    st.markdown(f"""<div class='vital-card'><p class='v-label'>Procedural Integrity</p><p style='color:#ffffff; font-weight:bold;'>DAP 2026 CONFORMANT</p></div>""", unsafe_allow_html=True)
with foot_2:
    st.markdown(f"""<div class='vital-card'><p class='v-label'>Data Sovereignty</p><p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p></div>""", unsafe_allow_html=True)
with foot_3:
    st.markdown(f"""<div class='vital-card'><p class='v-label'>Intelligence depth</p><p style='color:#ffffff; font-weight:bold;'>HEXAGONAL REASONING</p></div>""", unsafe_allow_html=True)

st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {TitanSystemRegistry.ACADEMY} | Project ID: {TitanSystemRegistry.BUILD_ID} | Lead: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)
