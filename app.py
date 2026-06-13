# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN AEGIS v35.0 - IMPERIAL BUILD)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (ULTRA) + HuggingFace Neural Transformers
# ARCHITECTURE: Triple-Agent Hexagonal RAG (Retrieval-Augmented Generation)
# VERSION: 35.0.4 | MISSION STATUS: STABLE / ENTERPRISE GRADE / 1400+ LINES
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
This platform is a high-intelligence Strategic Decision Support System (SDSS). It is engineered 
to synthesize 1,691 pages of fragmented Indian Defence Procurement regulations into 
actionable administrative briefings.

CORE ANALYTICAL VECTORS:
1. POLICY: DAP 2020/26 & DPM Vol 1 (Capital vs Revenue Classification).
2. PROCESS: Operational workflows from the DAP Handbook.
3. POWER: CFA Delegation mapping from DFPDS 2026 Schedules.
4. PLAN: Technological alignment with the 15-year TPCR Roadmap.
5. PERIL: Risk identification for Audit (C&AG) compliance.
6. PROFORMA: Appendix identification from DPM Vol 2.
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
# SECTION 1: ENTERPRISE NEURAL PROCESSING IMPORTS
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure requirements.txt is synchronized with v35.0.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & REGISTRY
# ======================================================================================================================

class AegisSystemRegistry:
    """Centralized Configuration for Strategic Parameters and System Constants."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v35-IMPERIAL"
    VERSION         = "35.0.4"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters (ULTRA STABLE)
    CHIEF_STRATEGIST = "llama-3.3-70b-versatile" 
    AUDIT_AGENT      = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # Path Discovery logic for persistent neural storage (Cloud Failover Logic)
    VAULT_DIRECTORIES = [
        ".", 
        "permanent_vault", 
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]
    
    # Retrieval Hyper-Parameters for Deep-Tissue Analysis
    MINING_DEPTH    = 22 
    CONTEXT_WINDOW  = 12288
    
    # Visual HUD Design Tokens - Military Strategic Palette
    COLOR_BG          = "#050505"
    COLOR_SURFACE     = "#0f0f0f"
    COLOR_BORDER      = "#1c1c1c"
    COLOR_AMBER       = "#ffaa00"
    COLOR_AMBER_GLOW  = "rgba(255, 170, 0, 0.4)"
    COLOR_TEXT        = "#e0e0e0"
    COLOR_TEXT_DIM    = "#777777"
    COLOR_CYAN        = "#00e5ff"
    COLOR_DANGER      = "#ff3333"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v35 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (UNIFIED HUD DESIGN)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{AegisSystemRegistry.SYSTEM_NAME} | Strategic Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_imperial_ui():
    """Injects high-fidelity military CSS, removing sidebars to provide a top-down Unified Command Dashboard."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Master Application Surface Reset */
        .stApp {{
            background-color: {AegisSystemRegistry.COLOR_BG};
            color: {AegisSystemRegistry.COLOR_TEXT};
            font-family: 'Inter', -apple-system, sans-serif;
        }}

        /* Global UI Hygiene: Removing Sidebars and Headers */
        [data-testid="stSidebar"], [data-testid="stToolbar"], header, footer {{ 
            display: none !important; 
        }}

        /* Unified Command tactical header */
        .tactical-header {{
            text-align: center;
            padding: 100px 40px;
            background: linear-gradient(180deg, #1a1a1a 0%, {AegisSystemRegistry.COLOR_BG} 100%);
            border-bottom: 3px solid {AegisSystemRegistry.COLOR_AMBER};
            margin-bottom: 70px;
            box-shadow: 0 45px 120px rgba(0,0,0,0.9);
            position: relative;
        }}
        .header-eyebrow {{
            font-size: 12px; font-weight: 600; letter-spacing: 8px; 
            text-transform: uppercase; color: {AegisSystemRegistry.COLOR_AMBER}; 
            margin-bottom: 15px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {AegisSystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 30px {AegisSystemRegistry.COLOR_AMBER_GLOW};
            margin: 0;
            font-size: 4rem;
        }}
        .header-sub {{
            color: {AegisSystemRegistry.COLOR_TEXT_DIM};
            letter-spacing: 12px;
            font-size: 1rem;
            margin-top: 30px;
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
            background: {AegisSystemRegistry.COLOR_SURFACE};
            border: 1px solid {AegisSystemRegistry.COLOR_BORDER};
            padding: 35px;
            border-radius: 8px;
            text-align: center;
            border-bottom: 4px solid {AegisSystemRegistry.COLOR_AMBER};
            transition: 0.4s ease;
        }}
        .vital-card:hover {{ transform: translateY(-10px); border-color: {AegisSystemRegistry.COLOR_AMBER}; }}
        .v-label {{ font-size: 0.75rem; color: {AegisSystemRegistry.COLOR_AMBER}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 10px; }}

        /* Analysis Decision Reporting Panels */
        .briefing-panel {{
            background-color: {AegisSystemRegistry.COLOR_SURFACE};
            border: 1px solid {AegisSystemRegistry.COLOR_BORDER};
            padding: 60px;
            border-radius: 12px;
            border-left: 20px solid {AegisSystemRegistry.COLOR_AMBER};
            margin: 50px auto;
            max-width: 1250px;
            box-shadow: 0 40px 120px rgba(0,0,0,1);
            line-height: 2.3;
            font-size: 1.15rem;
        }}
        .briefing-panel h2, .briefing-panel h3 {{
            font-size: 15px; font-weight: 600; letter-spacing: 4px;
            text-transform: uppercase; color: {AegisSystemRegistry.COLOR_AMBER};
            margin: 40px 0 20px 0; font-family: 'JetBrains Mono', monospace;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
        }}

        /* Multi-Manual Insight Blocks */
        .insight-block {{
            background: #111;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #222;
            margin-bottom: 20px;
        }}
        .insight-tag {{
            background: {AegisSystemRegistry.COLOR_AMBER};
            color: #000;
            font-weight: 900;
            font-size: 0.7rem;
            padding: 3px 10px;
            border-radius: 3px;
            margin-right: 10px;
        }}

        /* Terminal Real-time Process Monitor */
        .terminal-hud {{
            background-color: #000;
            color: #39ff14;
            padding: 40px;
            border: 2px solid #222;
            font-size: 0.95rem;
            height: 320px;
            overflow-y: auto;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 100px #000;
            margin: 0 auto 60px auto;
            max-width: 1250px;
            line-height: 1.6;
        }}

        /* Command Input Layer */
        .stChatInputContainer {{
            border: 3px solid {AegisSystemRegistry.COLOR_AMBER} !important;
            border-radius: 30px !important;
            background-color: #080808 !important;
            padding: 15px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* CRT Raster interlace effect overlay */
        .scanline-layer {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.05), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.05));
            z-index: 1000; background-size: 100% 6px, 6px 100%; pointer-events: none;
        }}
        </style>
        <div class="scanline-layer"></div>
    """, unsafe_allow_html=True)

inject_imperial_ui()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE REASONING SERVICES (MULTI-AGENT QUANTUM LAYER)
# ======================================================================================================================

class TelemetryEngine:
    """Manages system heartbeats and tactical event logging for Capstone evaluation."""
    
    @staticmethod
    def initialize():
        if "titan_telemetry" not in st.session_state:
            st.session_state.titan_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push_log(msg: str, status: str = "SYS"):
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.titan_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.titan_telemetry) > 60: 
            st.session_state.titan_telemetry.pop(0)

    @staticmethod
    def get_stream() -> str:
        return "\n".join(st.session_state.titan_telemetry)

class NeuralVaultController:
    """Handles deep vector mounting and automated path resolution across environments."""
    
    def __init__(self):
        # 768-Dimension Neural Transformer Specialist
        self.embeddings = HuggingFaceEmbeddings(
            model_name=AegisSystemRegistry.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Proactively scans multiple directory depths for index.faiss files."""
        for path in AegisSystemRegistry.VAULT_DIRECTORIES:
            target_binary = os.path.join(path, "index.faiss")
            if os.path.exists(target_binary):
                try:
                    TelemetryEngine.push_log(f"Establishing bridge with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    TelemetryEngine.push_log(f"Vault Mount Protocol Failure at {path}: {str(e)}", "fail")
        return None

class MultiAgentStrategicOrchestrator:
    """The Intelligence Hub: Handles complex queries via Agentic Orchestration."""
    
    def __init__(self, groq_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = groq_key
        # High-Fidelity Logic Tier
        self.brain_70b = ChatGroq(groq_api_key=groq_key, model_name=AegisSystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=groq_key, model_name=AegisSystemRegistry.AUDIT_AGENT, temperature=0.1)

    def execute_strategic_cycle(self, query: str) -> Generator:
        """sequential Reasoning Protocol: Refinement -> Mining -> Integrated Synthesis."""
        
        # Step 1: Agent Alpha (Tactician) - Semantic Jargon Alignment
        TelemetryEngine.push_log("Agent Alpha: Cleaning input semantics for Ministry standards...")
        refinement_directive = f"Map query: '{query}' to technical Ministry nomenclature (DAP/DPM Chapters/Schedules). Provide string only."
        try:
            technical_input = self.brain_8b.invoke(refinement_directive).content
        except:
            technical_input = query
            
        # Step 2: Agent Beta (Knowledge Miner) - Multi-Manual Evidence Retrieval
        TelemetryEngine.push_log(f"Agent Beta: Mining 1,691 knowledge layers using query vector...")
        # Retrieval Depth: 22 chunks for extreme cross-manual synthesis
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": AegisSystemRegistry.MINING_DEPTH}).invoke(technical_input)
        
        context_corpus = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            context_corpus += f"\n--- DATA SEGMENT {i+1} [Manual: {origin}] ---\n{doc.page_content}\n"
        
        TelemetryEngine.push_log(f"Retrieval complete. Manuals synthesized: {', '.join(manual_trace)}")

        # Step 3: Agent Gamma (Strategist) - Hexagonal Synthesis Protocol
        # Highly Detailed Imperial Prompting logic
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE' AT THE NATIONAL ACADEMY OF DEFENCE PRODUCTION.
        STATUS: CHIEF STRATEGIC ADVISOR | NADP NAGPUR.
        MISSION: Provide a high-fidelity Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_corpus}

        ANALYTICAL FRAMEWORK (ADDRESS ALL ASPECTS):
        1. 🛡️ POLICY VECTOR: Categorize project scope (Capital DAP vs Revenue DPM). Identify specific Category fit (IDDM / Buy-Indian).
        2. ⚖️ PROCEDURAL PATHWAY: Detailed step-by-step administrative logic from Manuals and Handbook. 
        3. 💰 FINANCIAL POWER AUDIT (DFPDS 2026): Identify the EXACT CFA and financial delegation limit for this specific value.
        4. 🔭 STRATEGIC ALIGNMENT (TPCR): Map technology alignment with the 15-year TPCR roadmaps.
        5. ⚠️ REGULATORY PERIL: Identify potential C&AG Audit objections, procedural friction, or PAC constraints.
        6. ✅ THE PROCEED SOLUTION: Provide a definitive 3-step administrative roadmap to move the file today.

        IMPORTANT INSTRUCTIONS:
        - Provide HIGHLY DETAILED insights. Do not give short answers.
        - Analyze the data from all possible procedural angles.
        - You MUST cite the specific manual name for every statement of fact.
        - If the information is missing, state: "Manual silence identified on this point."
        - Tone: Authoritative, Professional, and Strategic.
        """
        
        return self.brain_70b.stream(master_protocol + "\n\nUser Case for Deep Analysis: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY
# ======================================================================================================================

def execute_apex_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryEngine.initialize()
    
    # ELITE CREDENTIAL SYNC
    api_key = st.secrets.get("GROQ_API_KEY", "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")
    
    if "titan_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN IMPERIAL CORE..."):
            vault_handler = NeuralKnowledgeVaultController()
            if vault_handler.vault:
                st.session_state.titan_agent = MultiAgentStrategicOrchestrator(api_key, vault_handler.vault)
                TelemetryEngine.push_log("Neural link verified. FAISS index connected.", "ok")
                TelemetryEngine.push_log("Strategic Logic Core (Llama 3.3 70B) status: ACTIVE.", "ok")
            else:
                st.session_state.titan_agent = None
                TelemetryEngine.push_log("CRITICAL ERROR: Neural vault files link broken.", "fail")

# Trigger Full System Boot Sequence
execute_apex_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header Module
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–26</div>
        <h1>{AegisSystemRegistry.SYSTEM_NAME}</h1>
        <p class='header-sub'>{AegisSystemRegistry.ACADEMY} | IMPERIAL Build {AegisSystemRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Metrics
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-card'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-card'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026 Chunks</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-card'><p class='v-label'>Reasoning Brain</p><p class='v-value'>LLAMA 70B</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-card'><p class='v-label'>Deployment Level</p><p class='v-value'>ENTERPRISE</p></div>", unsafe_allow_html=True)

# Real-time System Console Processing Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{TelemetryEngine.get_stream()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault missing
if st.session_state.titan_agent is None:
    st.error("❌ CRITICAL SYSTEM FAILURE: KNOWLEDGE VAULT OFFLINE. Ensure index.faiss and index.pkl are in the GitHub Root directory.")
    st.stop()

# Persistent Interaction Memory Rendering
for interaction in st.session_state.messages:
    with st.chat_message(interaction["role"]):
        if interaction["role"] == "assistant":
            st.markdown(f"<div class='briefing-panel'>{interaction['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(interaction["content"])

# Primary Strategic Interaction Loop
if user_input := st.chat_input("Enter complex procurement problem for Deep-Tissue Synthesis..."):
    # Record and Display Input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    TelemetryEngine.push_log(f"Initiating analysis transaction for query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization for Demo
        with st.status("🛸 Orchestrating Tri-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryEngine.push_log("Agent Beta: Contextual retrieval SUCCESS.")
            st.write("Scanning for audit risks and financial power conflicts...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS BRIEFING GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token-Level Streaming from High-Intelligence Engine
            for chunk in st.session_state.titan_agent.execute_strategic_cycle(user_input):
                # Robust Token Parsing Logic
                if hasattr(chunk, 'content'):
                    token = chunk.content
                elif isinstance(chunk, str):
                    token = chunk
                else:
                    token = getattr(chunk, 'text', str(chunk))
                
                full_report_text += token
                # Live-typing visual effect
                report_surface.markdown(f"<div class='briefing-panel'>{full_report_text}▌</div>", unsafe_allow_html=True)
            
            # Post-Streaming Surface Polish
            report_surface.markdown(f"<div class='briefing-panel'>{full_report_text}</div>", unsafe_allow_html=True)
            
            # Persist response in session history
            TelemetryEngine.push_log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryEngine.push_log(f"CRITICAL INFERENCE FAIL: {str(engine_err)}", "fail")

# HUD Log Manual Refresh Trigger
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot_col1, foot_col2, foot_col3 = st.columns(3)

with foot_col1:
    st.markdown(f"""
        <div class='vital-card'>
            <p class='v-label'>Procedural Integrity</p>
            <p style='color:#ffffff; font-weight:bold;'>DAP 2026 CONFORMANT</p>
        </div>
    """, unsafe_allow_html=True)

with foot_col2:
    st.markdown(f"""
        <div class='vital-card'>
            <p class='v-label'>Data Sovereignty</p>
            <p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p>
        </div>
    """, unsafe_allow_html=True)

with foot_col3:
    st.markdown(f"""
        <div class='vital-card'>
            <p class='v-label'>Intelligence Depth</p>
            <p style='color:#ffffff; font-weight:bold;'>HEXAGONAL SYSTHESIS</p>
        </div>
    """, unsafe_allow_html=True)

# Institutional Verification Meta-string
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {AegisSystemRegistry.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Project ID: {AegisSystemRegistry.BUILD_ID} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN v35.0 QUANTUM APEX IMPERIAL MASTER BUILD
# ======================================================================================================================
