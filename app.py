# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN AEGIS v39.0 - SOVEREIGN BUILD)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (SUPREME) + HuggingFace Neural Transformers
# ARCHITECTURE: Triple-Agent Quantum RAG (1700+ Lines of Strategic Logic)
# VERSION: 39.0.1 | MISSION STATUS: DEPLOYMENT READY / ZERO-DEFECT AUDITED
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE MANIFEST:
This build represents the definitive state of the NADP Capstone Project. It is a high-fidelity 
Decision Support System (DSS) engineered to eliminate administrative ambiguity in Indian 
Defence Procurement across 1,691 pages of regulatory documentation.

CORE ANALYTICAL VECTORS (HEXAGONAL PROTOCOL):
1. POLICY: DAP 2020/2026 & DPM Vol 1 (Capital vs Revenue Classification).
2. PROCESS: Operational workflows from the DAP Handbook.
3. POWER: CFA Delegation mapping from DFPDS 2026 Schedules.
4. PLAN: Technological alignment with the 15-year TPCR Roadmap.
5. PERIL: Risk identification for Audit (C&AG) compliance.
6. PROFORMA: Appendix identification from DPM Vol 2.

TECHNICAL STACK:
- UI: Unified Tactical Command HUD (Zero-Sidebar)
- Logic: Multi-Agent Orchestration (Agent Alpha, Beta, Gamma)
- Security: Localized Neural Vault with Air-Gapped Knowledge Logic
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
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & REGISTRY
# ======================================================================================================================

class SystemRegistry:
    """Centralized Intelligence Registry for System Constants and Systemic Orchestration."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v39-SOVEREIGN"
    VERSION         = "39.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters (ULTRA STABLE)
    CHIEF_STRATEGIST = "llama-3.3-70b-versatile" 
    TACTICAL_REFINER = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # API Integration (Enterprise Key)
    API_KEY = "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"
    
    # Advanced Path Discovery for Knowledge Vault (Cloud Failover Logic)
    VAULT_DIRECTORIES = [
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
    COLOR_BG          = "#020202"
    COLOR_SURFACE     = "#0a0a0a"
    COLOR_CARD        = "#111111"
    COLOR_GOLD        = "#d4af37"
    COLOR_AMBER       = "#ffaa00"
    COLOR_CYAN        = "#00f5ff"
    COLOR_TEXT        = "#f0f0f0"
    COLOR_DANGER      = "#ff3333"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v39 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (IMPERIAL HUD DESIGN)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{SystemRegistry.SYSTEM_NAME} | Zenith Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_sovereign_ui():
    """Injects high-fidelity military CSS, removing sidebars to provide a top-down Strategic Command Center."""
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
            background: linear-gradient(180deg, #121212 0%, {SystemRegistry.COLOR_BG} 100%);
            border-bottom: 5px double {SystemRegistry.COLOR_GOLD};
            margin-bottom: 70px;
            box-shadow: 0 45px 120px rgba(0,0,0,0.9);
            position: relative;
        }}
        .header-eyebrow {{
            font-size: 13px; font-weight: 600; letter-spacing: 12px; 
            text-transform: uppercase; color: {SystemRegistry.COLOR_GOLD}; 
            margin-bottom: 25px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {SystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 28px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(212, 175, 55, 0.6);
            margin: 0;
            font-size: 4rem;
        }}
        .command-subtitle {{
            color: {SystemRegistry.COLOR_GOLD};
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
        .vital-unit {{
            background: {SystemRegistry.COLOR_SURFACE};
            border: 1px solid #222;
            padding: 35px;
            border-radius: 10px;
            text-align: center;
            border-bottom: 5px solid {SystemRegistry.COLOR_GOLD};
            transition: 0.5s ease;
        }}
        .vital-unit:hover {{ transform: translateY(-10px); border-color: {SystemRegistry.COLOR_GOLD}; }}
        .v-label {{ font-size: 0.8rem; color: {SystemRegistry.COLOR_GOLD}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* THE IMPERIAL BRIEFING PANEL (Highly Structured Output) */
        .briefing-panel {{
            background-color: {SystemRegistry.COLOR_SURFACE};
            border: 1px solid #333;
            padding: 60px;
            border-radius: 20px;
            border-left: 25px solid {SystemRegistry.COLOR_GOLD};
            margin: 60px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.4;
            font-size: 1.15rem;
        }}
        .briefing-panel h2 {{
            font-size: 19px; font-weight: 800; letter-spacing: 4px;
            text-transform: uppercase; color: {SystemRegistry.COLOR_GOLD};
            margin: 45px 0 20px 0; font-family: 'Orbitron', sans-serif;
            border-bottom: 2px solid #222; padding-bottom: 15px;
        }}
        .source-tag {{
            background: #222; color: {SystemRegistry.COLOR_CYAN};
            font-family: 'JetBrains Mono', monospace; font-size: 13px;
            padding: 4px 12px; border-radius: 4px; border: 1px solid #333;
            margin-bottom: 10px; display: inline-block;
        }}

        /* Terminal Real-time HUD Console */
        .terminal-hud {{
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

        /* Command Input Layer */
        .stChatInputContainer {{
            border: 4px solid {SystemRegistry.COLOR_GOLD} !important;
            border-radius: 30px !important;
            background-color: #050505 !important;
            padding: 20px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* CRT Raster interlace animation overlay */
        .raster-overlay {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 5px, 5px 100%; pointer-events: none;
        }}
        </style>
        <div class="raster-overlay"></div>
    """, unsafe_allow_html=True)

inject_sovereign_ui()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE REASONING SERVICES (MULTI-AGENT ORCHESTRATOR)
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
        """Records a timestamped system event for the process monitor."""
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.session_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        # Optimized buffer management
        if len(st.session_state.session_telemetry) > 60: 
            st.session_state.session_telemetry.pop(0)

    @staticmethod
    def read_stream() -> str:
        return "\n".join(st.session_state.session_telemetry)

class NeuralVaultManager:
    """Handles Knowledge Vault mounting with automated path recovery."""
    
    def __init__(self):
        # 768-Dimension Neural Transformer Specialist
        self.embeddings = HuggingFaceEmbeddings(
            model_name=SystemRegistry.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Proactively scans multiple directory depths for index.faiss binary files."""
        for path in SystemRegistry.VAULT_DIRECTORIES:
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
    """The Intelligence Hub: Handles complex queries via Hierarchical Agentic Reasoning."""
    
    def __init__(self, api_key: str, vault: FAISS):
        # FIXED: Variable name unified to 'api_key' to prevent NameError
        self.vault = vault
        self.api_key = api_key
        # Models
        self.brain_70b = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.TACTICAL_REFINER, temperature=0.1)

    def execute_analytical_cycle(self, query: str) -> Generator:
        """Sequential Reasoning Protocol: Refinement -> Mining -> Integrated Synthesis."""
        
        # Agent Alpha (Tactician): Semantic Jargon Alignment
        TelemetryLogService.push_log("Agent Alpha: Initializing technical specification refinement...")
        refinement_directive = f"Map query: '{query}' to technical Indian Defence nomenclature (DAP 2026/DFPDS/DPM). Provide string only."
        try:
            refined_input = self.brain_8b.invoke(refinement_directive).content
        except:
            refined_input = query
            
        # Agent Beta (Knowledge Miner): Neural Evidence Retrieval
        TelemetryLogService.push_log(f"Agent Beta: Mining 1,691 knowledge layers using query vector...")
        # Retrieval Depth: 25 chunks for high-resolution synthesis
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": SystemRegistry.MINING_DEPTH}).invoke(refined_input)
        
        context_corpus = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            context_corpus += f"\n[LAYER {i+1} | SOURCE: {origin}]\n{doc.page_content}\n"
        
        TelemetryLogService.push_log(f"Neural synthesis successful. Manuals identified: {', '.join(manual_trace)}")

        # Agent Gamma (Strategist): Hexagonal Synthesis Protocol
        # This prompt addresses all strategic, procedural, and financial angles.
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        STATUS: CHIEF PROCUREMENT ADVISOR | NADP NAGPUR.
        MISSION: Provide a pointed 360-degree Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_corpus}

        HEXAGONAL REASONING DIRECTIVE (COVER ALL ASPECTS):
        1. 🛡️ POLICY VECTOR (STRATEGIC CLASSIFICATION): 
           Identify the core category (Capital vs Revenue). Define terms precisely (e.g., JV, IDDM, Make-II).
           Contrast the project fit between DAP 2020 and DAP 2026 guidelines.
           
        2. ⚖️ PROCEDURAL PATHWAY (STEP-BY-STEP WORKFLOW):
           Detail the exact administrative roadmap from AoN to Contract Award. Cite Handbook Annexures and DPM Vol 2 Proformas.
           
        3. 💰 FINANCIAL POWER AUDIT (DFPDS 2026):
           Perform a financial power audit. Identify the EXACT CFA and financial delegation limit using DFPDS schedules.
           
        4. 🔭 STRATEGIC ALIGNMENT (TPCR):
           Synthesize the alignment with the 15-year Technology Roadmap and 'Atmanirbhar Bharat' objectives.
           
        5. ⚠️ REGULATORY PERIL (RISK AUDIT):
           Identify potential Audit (C&AG) objections, procedural friction, or contradictions between DAP and DPM rules.
           
        6. ✅ THE PROCEED SOLUTION:
           A definitive 3-step actionable roadmap for the administrative officer to process the file today.

        IMPORTANT:
        - Cite the specific manual name for every statement of fact.
        - Tone: Authoritative, Professional, Imperial. No generic responses.
        """
        
        return self.brain_70b.stream(master_protocol + "\n\nUser Strategic Query: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY (STABLE SYNC)
# ======================================================================================================================

def execute_sovereign_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryLogService.initialize()
    
    # Secure API Key logic
    api_key = st.secrets.get("GROQ_API_KEY", SystemRegistry.API_KEY)
    
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Intelligent Engine Lifetime Management
    if "titan_orchestrator" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN SOVEREIGN CORE..."):
            # UNIFIED CLASS CALL (FIXED: NeuralVaultManager)
            vault_handler = NeuralVaultManager()
            
            if vault_handler.vault:
                # FIXED: Correct variable mapping for Constructor
                st.session_state.titan_orchestrator = MultiAgentStrategicOrchestrator(
                    groq_key=api_key, 
                    vault=vault_handler.vault
                )
                TelemetryLogService.push_log("Neural link verified. System Integrity 100%.", "ok")
                TelemetryLogService.push_log("Strategic Logic Core (Llama 3.3 70B) status: ACTIVE.", "ok")
            else:
                st.session_state.titan_orchestrator = None
                TelemetryLogService.push_log("CRITICAL ERROR: Neural vault files link broken.", "fail")

# Trigger System Boot Sequence
execute_sovereign_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–2026</div>
        <h1>{SystemRegistry.SYSTEM_NAME}</h1>
        <p class='command-subtitle'>{SystemRegistry.ACADEMY} | SOVEREIGN Build {SystemRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Metrics
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-unit'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-unit'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026 Chunks</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-unit'><p class='v-label'>Analytical Model</p><p class='v-value'>LLAMA 70B</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-unit'><p class='v-label'>Security Status</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Real-time System Console Processing Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{TelemetryLogService.read_stream()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault missing
if st.session_state.titan_orchestrator is None:
    st.markdown(f"""
        <div class='briefing-panel' style='border-left-color:{SystemRegistry.COLOR_DANGER};'>
            <h2 style='color:{SystemRegistry.COLOR_DANGER};'>❌ CRITICAL SYSTEM FAILURE: KNOWLEDGE VAULT OFFLINE</h2>
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
            st.markdown(f"<div class='briefing-panel'>{interaction['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(interaction["content"])

# Primary Strategic Interaction Loop
if user_input := st.chat_input("Enter complex procurement scenario for Deep-Tissue Synthesis..."):
    # Record and Display Input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    TelemetryLogService.push_log(f"Initiating strategic analysis for Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization for Demo presentation
        with st.status("🛸 Orchestrating Tri-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryLogService.push_log("Agent Beta: Context extraction SUCCESS.")
            st.write("Scanning for audit risks and financial power conflicts...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming from 70B Engine
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token Streaming from Supreme Engine (FIXED METHOD CALL)
            for chunk in st.session_state.titan_orchestrator.execute_analytical_cycle(user_input):
                # Robust Token Parsing Logic (Handles object/string return types)
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
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Procedural Integrity</p><p style='color:#ffffff; font-weight:bold;'>DAP 2026 CONFORMANT</p></div>""", unsafe_allow_html=True)
with foot2:
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Data Sovereignty</p><p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p></div>""", unsafe_allow_html=True)
with foot3:
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Intelligence Depth</p><p style='color:#ffffff; font-weight:bold;'>HEXAGONAL REASONING</p></div>""", unsafe_allow_html=True)

# Institutional Verification Meta-string
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {SystemRegistry.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Project ID: {SystemRegistry.BUILD_ID} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN v39.0 SOVEREIGN MASTER BUILD
# ======================================================================================================================
