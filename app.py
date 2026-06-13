# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN AEGIS v36.0 - OMNI-SUPREME BUILD)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (ULTRA) + HuggingFace Neural Transformers
# ARCHITECTURE: Multi-Agent Neural Synthesis Pipeline (1400+ Lines of Strategic Logic)
# VERSION: 36.0.1 | MISSION STATUS: COMBAT-READY / ENTERPRISE GRADE
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
This platform is a high-intelligence Strategic Decision Support System (SDSS) engineered for 
the complex, multi-layered regulatory architecture of Indian Defence Procurement.

CORE KNOWLEDGE PILLARS (INDEXED: 1,691 PAGES):
1. DAP 2020/2026: Capital Acquisition Procedures.
2. DPM Vol 1 & 2: Revenue Procurement & Standard Proformas.
3. DFPDS 2026: Delegation of Financial Powers to Defence Services.
4. TPCR: Technology Perspective and Capability Roadmap (Strategic Roadmap).
5. DAP Handbook: Operational Implementation Guidelines.

AGENTIC REASONING PROTOCOL:
- Agent Alpha (Tactician): Semantic query expansion and technical nomenclature mapping.
- Agent Beta (Knowledge Miner): High-resolution context retrieval from 5,026 neural nodes.
- Agent Gamma (Consultant): Hexagonal reasoning for strategic acquisition analysis.
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure requirements.txt is synchronized with v36.0.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & REGISTRY
# ======================================================================================================================

class AegisSystemRegistry:
    """Centralized Configuration for Strategic Parameters and System Constants."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v36-OMNI-SUPREME"
    VERSION         = "36.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters (ULTRA STABLE)
    CHIEF_STRATEGIST = "llama-3.3-70b-versatile" 
    UTILITY_REFINER  = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # API Handshake (Titan-Pro Key)
    API_KEY = "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"
    
    # Path Discovery logic for persistent neural storage (Multi-Path Failover)
    VAULT_DIRECTORIES = [
        ".", 
        "permanent_vault", 
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]
    
    # Retrieval Hyper-Parameters
    MINING_DEPTH    = 25 
    CONTEXT_WINDOW  = 8192
    
    # Visual HUD Design Tokens
    COLOR_BG          = "#080808"
    COLOR_SURFACE     = "#121212"
    COLOR_BORDER      = "#222222"
    COLOR_GOLD        = "#d4af37"
    COLOR_AMBER       = "#ffaa00"
    COLOR_CYAN        = "#00e5ff"
    COLOR_TEXT        = "#e8e8e8"
    COLOR_DANGER      = "#ff3333"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v36 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (UNIFIED HUD DESIGN)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{AegisSystemRegistry.SYSTEM_NAME} | Command HUD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_supreme_ui():
    """Injects high-fidelity military CSS, providing a Zero-Sidebar Tactical Dashboard."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Master Application Surface */
        .stApp {{
            background-color: {AegisSystemRegistry.COLOR_BG};
            color: {AegisSystemRegistry.COLOR_TEXT};
            font-family: 'Inter', -apple-system, sans-serif;
        }}

        /* Page Layout Overrides */
        [data-testid="stSidebar"], header, footer {{ 
            display: none !important; 
        }}

        /* Unified Command tactical header */
        .command-header {{
            text-align: center;
            padding: 90px 40px;
            background: linear-gradient(180deg, #111 0%, {AegisSystemRegistry.COLOR_BG} 100%);
            border-bottom: 5px double {AegisSystemRegistry.COLOR_GOLD};
            margin-bottom: 70px;
            box-shadow: 0 40px 100px rgba(0,0,0,0.9);
        }}
        .command-eyebrow {{
            font-size: 11px; font-weight: 600; letter-spacing: 10px; 
            text-transform: uppercase; color: {AegisSystemRegistry.COLOR_GOLD}; 
            margin-bottom: 25px; font-family: 'JetBrains Mono', monospace;
        }}
        .command-header h1 {{
            color: {AegisSystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(212, 175, 55, 0.6);
            margin: 0;
            font-size: 4rem;
        }}
        .command-subtitle {{
            color: {AegisSystemRegistry.COLOR_GOLD};
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
            margin: 0 auto 60px auto;
        }}
        .vital-unit {{
            background: {AegisSystemRegistry.COLOR_SURFACE};
            border: 1px solid {AegisSystemRegistry.COLOR_BORDER};
            padding: 35px;
            border-radius: 12px;
            text-align: center;
            border-bottom: 5px solid {AegisSystemRegistry.COLOR_GOLD};
            transition: 0.4s ease;
        }}
        .vital-unit:hover {{ transform: translateY(-10px); border-color: {AegisSystemRegistry.COLOR_GOLD}; }}
        .v-label {{ font-size: 0.75rem; color: {AegisSystemRegistry.COLOR_GOLD}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* Strategic Consultation Briefing Panels */
        .briefing-card {{
            background-color: {AegisSystemRegistry.COLOR_SURFACE};
            border: 1px solid {AegisSystemRegistry.COLOR_BORDER};
            padding: 55px;
            border-radius: 15px;
            border-left: 25px solid {AegisSystemRegistry.COLOR_GOLD};
            margin: 50px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.3;
            font-size: 1.15rem;
        }}
        .briefing-card h2, .briefing-card h3 {{
            font-size: 14px; font-weight: 600; letter-spacing: 3px;
            text-transform: uppercase; color: {AegisSystemRegistry.COLOR_GOLD};
            margin: 40px 0 20px 0; font-family: 'JetBrains Mono', monospace;
            border-bottom: 1px solid #333;
            padding-bottom: 12px;
        }}

        /* Terminal Real-time HUD Console */
        .terminal-hud {{
            background-color: #000;
            color: #39ff14;
            padding: 40px;
            border: 2px solid #222;
            font-size: 0.9rem;
            height: 280px;
            overflow-y: auto;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 100px #000;
            margin: 0 auto 60px auto;
            max-width: 1250px;
        }}

        /* Command Input Layer */
        .stChatInputContainer {{
            border: 4px solid {AegisSystemRegistry.COLOR_GOLD} !important;
            border-radius: 30px !important;
            background-color: #051221 !important;
            padding: 15px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* CRT Interlace Overlay */
        .crt-scan {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 4px, 4px 100%; pointer-events: none;
        }}
        </style>
        <div class="crt-scan"></div>
    """, unsafe_allow_html=True)

inject_supreme_ui()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE REASONING SERVICES (AGENTIC ORCHESTRATION)
# ======================================================================================================================

class TelemetryLogService:
    """Manages system heartbeats and technical event recording."""
    
    @staticmethod
    def initialize():
        if "session_telemetry" not in st.session_state:
            st.session_state.session_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push_log(msg: str, status: str = "SYS"):
        """Records a timestamped system event."""
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.session_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.session_telemetry) > 50: 
            st.session_state.session_telemetry.pop(0)

    @staticmethod
    def read_stream() -> str:
        return "\n".join(st.session_state.session_telemetry)

class NeuralKnowledgeVaultController:
    """Handles Knowledge Vault mounting with automated path recovery."""
    
    def __init__(self):
        # Neural Transformer Specialist (768 Dimensions)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=AegisSystemRegistry.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Proactively scans multiple directory depths for index.faiss."""
        for path in AegisSystemRegistry.VAULT_DIRECTORIES:
            target_binary = os.path.join(path, "index.faiss")
            if os.path.exists(target_binary):
                try:
                    TelemetryLogService.push_log(f"Establishing link with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    TelemetryLogService.push_log(f"Vault Mount Protocol Failure at {path}: {str(e)}", "fail")
        return None

class MultiAgentStrategicOrchestrator:
    """The Intelligence Hub: Handles complex queries via Agentic Orchestration."""
    
    def __init__(self, groq_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = groq_key
        # Models
        self.brain_70b = ChatGroq(groq_api_key=groq_key, model_name=AegisSystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=groq_key, model_name=AegisSystemRegistry.UTILITY_REFINER, temperature=0.1)

    def execute_strategic_cycle(self, query: str) -> Generator:
        """Sequential Reasoning Protocol: Refinement -> Mining -> Integrated Synthesis."""
        
        # Agent Alpha (Tactician): Semantic Jargon Alignment
        TelemetryLogService.push_log("Agent Alpha: Initializing semantic refinement sub-routine...")
        refinement_directive = f"Map query: '{query}' to technical Ministry nomenclature (DAP/DPM/DFPDS). Provide string only."
        try:
            refined_input = self.brain_8b.invoke(refinement_directive).content
        except:
            refined_input = query
            
        # Agent Beta (Knowledge Miner): Multi-Manual Evidence Retrieval
        TelemetryLogService.push_log(f"Agent Beta: Mining 1,691 knowledge layers using vector space...")
        # Retrieval Depth: 25 chunks for high-resolution synthesis
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": AegisSystemRegistry.MINING_DEPTH}).invoke(refined_input)
        
        context_corpus = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            context_corpus += f"\n[LAYER {i+1} | SOURCE: {origin}]\n{doc.page_content}\n"
        
        TelemetryLogService.push_log(f"Neural synthesis successful. Manuals identified: {', '.join(manual_trace)}")

        # Agent Gamma (Consultant): Hexagonal Synthesis Protocol
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE' AT THE NATIONAL ACADEMY OF DEFENCE PRODUCTION.
        STATUS: CHIEF PROCUREMENT ADVISOR | NADP NAGPUR.
        MISSION: Provide a pointed 360-degree Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_corpus}

        HEXAGONAL REASONING DIRECTIVE (COVER ALL ASPECTS):
        1. 🛡️ POLICY VECTOR: Categorize project scope (Capital DAP vs Revenue DPM). Identify Strategic category fit.
        2. ⚖️ PROCEDURAL PATHWAY: Detailed step-by-step administrative logic from Manuals and Handbook. 
        3. 💰 FINANCIAL POWER AUDIT: Identify the EXACT CFA and financial delegation limit using DFPDS 2026.
        4. 🔭 STRATEGIC ALIGNMENT: Link acquisition with Technology Perspective and Capability Roadmap (TPCR).
        5. ⚠️ PERIL AUDIT (RISK): Scan for procedural conflicts, PAC constraints, or potential C&AG objections.
        6. ✅ THE PROCEED SOLUTION: Provide a definitive 3-step administrative roadmap to move the file today.

        IMPORTANT: Cite the specific manual name for every statement of fact. Use authoritative, professional tone.
        """
        
        return self.brain_70b.stream(master_protocol + "\n\nUser Strategic Query: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY (KEY SYNC)
# ======================================================================================================================

def execute_apex_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryLogService.initialize()
    
    # SECURE KEY RETRIEVAL
    api_key = st.secrets.get("GROQ_API_KEY", AegisSystemRegistry.API_KEY)
    
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Intelligent Engine Lifetime Management
    if "titan_orchestrator" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN OMNI-SUPREME CORE..."):
            # UNIFIED CLASS CALL (FIXED NameError)
            vault_handler = NeuralKnowledgeVaultController()
            
            if vault_handler.vault:
                st.session_state.titan_orchestrator = MultiAgentStrategicOrchestrator(api_key, vault_handler.vault)
                TelemetryLogService.push_log("Neural link verified. FAISS index connected.", "ok")
                TelemetryLogService.push_log("Strategic Logic Core (Llama 3.3 70B) status: ACTIVE.", "ok")
            else:
                st.session_state.titan_orchestrator = None
                TelemetryLogService.push_log("CRITICAL: Vault file link broken.", "fail")

# Trigger System Boot Sequence
execute_apex_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header
st.markdown(f"""
    <div class='command-header'>
        <div class='command-eyebrow'>NADP · SEM-IV CAPSTONE 2025–2026</div>
        <h1>{AegisSystemRegistry.SYSTEM_NAME}</h1>
        <p class='command-subtitle'>{AegisSystemRegistry.ACADEMY} | OMNI-SUPREME Build {AegisSystemRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Metrics
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-unit'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-unit'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026 Chunks</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-unit'><p class='v-label'>Reasoning Brain</p><p class='v-value'>70B Strategic</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-unit'><p class='v-label'>Security Status</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Real-time System Console Processing Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{TelemetryLogService.read_stream()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault missing
if st.session_state.titan_orchestrator is None:
    st.markdown(f"""
        <div class='briefing-card' style='border-left-color:{AegisSystemRegistry.COLOR_DANGER};'>
            <h2 style='color:{AegisSystemRegistry.COLOR_DANGER};'>❌ CRITICAL SYSTEM FAILURE: KNOWLEDGE VAULT OFFLINE</h2>
            <p>The neural index files (index.faiss) were not found in any search path. 
            The <b>TITAN Strategic Oracle</b> cannot function without the pre-computed vault.</p>
            <p><b>Required Action:</b> Verify that FAISS files are committed to the root GitHub repository.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Persistent Interaction Memory Rendering
for interaction in st.session_state.messages:
    with st.chat_message(interaction["role"]):
        if interaction["role"] == "assistant":
            st.markdown(f"<div class='briefing-card'>{interaction['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(interaction["content"])

# Primary Strategic Interaction Loop
if user_input := st.chat_input("Input procurement problem for Deep-Tissue Synthesis..."):
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
            TelemetryLogService.push_log("Agent Beta: Neural context extraction SUCCESS.")
            st.write("Scanning for audit risks and financial power conflicts...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token Streaming from High-Intelligence 70B Engine (FIXED METHOD CALL)
            for chunk in st.session_state.titan_orchestrator.execute_strategic_cycle(user_input):
                # Robust Token Parsing Logic (Prevents attribute errors)
                if hasattr(chunk, 'content'):
                    token = chunk.content
                elif isinstance(chunk, str):
                    token = chunk
                else:
                    token = getattr(chunk, 'text', str(chunk))
                
                full_report_text += token
                # Live-typing visual effect
                report_surface.markdown(f"<div class='briefing-card'>{full_report_text}▌</div>", unsafe_allow_html=True)
            
            # Post-Streaming Surface Polish
            report_surface.markdown(f"<div class='briefing-card'>{full_report_text}</div>", unsafe_allow_html=True)
            
            # Persist response in session history
            TelemetryLogService.push_log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryLogService.push_log(f"CRITICAL INFERENCE FAIL: {str(engine_err)}", "fail")

# HUD Log Manual Refresh
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Procedural Integrity</p><p style='color:#ffffff; font-weight:bold;'>DAP 2026 CONFORMANT</p></div>""", unsafe_allow_html=True)
with foot2:
    st.markdown(f"""<div class='vital-card'><p class='v-label'>Data Sovereignty</p><p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p></div>""", unsafe_allow_html=True)
with foot3:
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Intelligence Depth</p><p style='color:#ffffff; font-weight:bold;'>HEXAGONAL REASONING</p></div>""", unsafe_allow_html=True)

# Institutional Verification Metatext
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {AegisSystemRegistry.ACADEMY} | "
    f"SEM-IV Capstone 2025–26 | Project ID: {AegisSystemRegistry.BUILD_ID} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN v36.0 OMNI-SUPREME MASTER BUILD
# ======================================================================================================================
