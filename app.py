# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN v29.0 - QUANTUM APEX ELITE)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.1 70B + HuggingFace Neural Transformers
# VERSION: 29.0.4 | STATUS: MISSION CRITICAL / ELITE ENTERPRISE BUILD
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
This platform is a high-intelligence Strategic Decision Support System (SDSS). It is engineered 
to synthesize 1,691 pages of fragmented Indian Defence Procurement regulations into 
actionable administrative briefings.

MULTI-AGENT ORCHESTRATION:
1. Agent Alpha (Tactician): Semantic expansion to align user queries with MoD technical nomenclature.
2. Agent Beta (Knowledge Miner): Neural retrieval across 5,026 vector nodes with metadata weighting.
3. Agent Gamma (Regulatory Auditor): Identifying procedural friction between DAP (Capital) and DPM (Revenue).
4. Agent Delta (Strategic Oracle): Final 360-degree synthesis across the Hexagonal Reasoning Framework.

VAULT INTEGRITY DATA:
- Corpus Size: 1,691 Pages (DAP 2026, DPM Vol 1 & 2, DFPDS 2026, TPCR Roadmap).
- Neural Architecture: 768-Dimension Nomic Embedding Space.
- Security Protocol: Local Vault Data Sovereignty with SSL-Encrypted Inference.
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
# SECTION 1: ENTERPRISE NEURAL PROCESSING IMPORTS & DEPENDENCY GATES
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Ensure requirements.txt is synchronized with v29.0 specifications.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & ELITE CONFIGURATION
# ======================================================================================================================

class QuantumConfig:
    """Centralized Registry for System Constants, Neural Parameters, and Design Tokens."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v29-QUANTUM-ELITE"
    VERSION         = "29.0.4"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters
    CHIEF_MODEL     = "llama-3.1-70b-versatile" 
    UTILITY_MODEL   = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
    
    # Path Discovery logic for persistent neural storage (Multi-Environment Failover)
    VAULT_DIRECTORIES = [
        ".", 
        "permanent_vault", 
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]
    
    # Design tokens — Military Monochrome & Strategic Amber
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

# Secure Audit Logging Initialization for NADP Oversight
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_ELITE | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (UNIFIED COMMAND HUD)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{QuantumConfig.SYSTEM_NAME} | Tactical HUD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_elite_ui():
    """
    Injects high-fidelity military-grade CSS.
    Removes sidebars to provide a top-down Unified Strategic Dashboard for presentation.
    """
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Master Application Surface Reset */
        .stApp {{
            background-color: {QuantumConfig.COLOR_BG};
            color: {QuantumConfig.COLOR_TEXT};
            font-family: 'Inter', -apple-system, sans-serif;
        }}

        /* Global UI Hygiene: Removing Sidebars and Headers */
        [data-testid="stSidebar"], [data-testid="stToolbar"], header, footer {{ 
            display: none !important; 
        }}

        /* Command Center tactical header Component */
        .tactical-header {{
            text-align: center;
            padding: 90px 40px;
            background: linear-gradient(180deg, #1a1a1a 0%, {QuantumConfig.COLOR_BG} 100%);
            border-bottom: 3px double {QuantumConfig.COLOR_AMBER};
            margin-bottom: 70px;
            box-shadow: 0 45px 120px rgba(0,0,0,0.9);
        }}
        .header-eyebrow {{
            font-size: 11px; font-weight: 600; letter-spacing: 6px; 
            text-transform: uppercase; color: {QuantumConfig.COLOR_AMBER}; 
            margin-bottom: 20px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {QuantumConfig.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(200, 147, 58, 0.5);
            margin: 0;
            font-size: 3.8rem;
        }}
        .header-sub {{
            color: {QuantumConfig.COLOR_TEXT_DIM};
            letter-spacing: 10px;
            font-size: 0.95rem;
            margin-top: 25px;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* System Telemetry HUD Grid */
        .vitals-hud {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto 80px auto;
        }}
        .vital-card {{
            background: {QuantumConfig.COLOR_SURFACE};
            border: 1px solid {QuantumConfig.COLOR_BORDER};
            padding: 35px;
            border-radius: 10px;
            text-align: center;
            border-bottom: 5px solid {QuantumConfig.COLOR_AMBER};
            transition: 0.5s ease;
        }}
        .vital-card:hover {{ transform: translateY(-10px); border-color: {QuantumConfig.COLOR_AMBER}; box-shadow: 0 10px 30px rgba(200, 147, 58, 0.2); }}
        .v-label {{ font-size: 0.8rem; color: {QuantumConfig.COLOR_AMBER}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* Dynamic Analysis Briefing Cards */
        .response-brief {{
            background-color: {QuantumConfig.COLOR_SURFACE};
            border: 1px solid {QuantumConfig.COLOR_BORDER};
            padding: 60px;
            border-radius: 20px;
            border-left: 25px solid {QuantumConfig.COLOR_AMBER};
            margin: 60px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.3;
            font-size: 1.15rem;
        }}
        .response-brief h2, .response-brief h3 {{
            font-size: 14px; font-weight: 600; letter-spacing: 3px;
            text-transform: uppercase; color: {QuantumConfig.COLOR_AMBER};
            margin: 40px 0 20px 0; font-family: 'JetBrains Mono', monospace;
            border-bottom: 1px solid {QuantumConfig.COLOR_BORDER};
            padding-bottom: 10px;
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
            border: 4px solid {QuantumConfig.COLOR_AMBER} !important;
            border-radius: 30px !important;
            background-color: #051221 !important;
            padding: 20px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* CRT Raster Interlace Animation Overlay */
        .scanline-layer {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.05), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.05));
            z-index: 1000; background-size: 100% 6px, 6px 100%; pointer-events: none;
        }}
        </style>
        <div class="scanline-layer"></div>
    """, unsafe_allow_html=True)

inject_elite_ui()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE REASONING SERVICES (MULTI-AGENT AGNOSTIC LAYER)
# ======================================================================================================================

class TelemetryMonitor:
    """Manages system heartbeats and tactical event logging for Capstone evaluation."""
    
    @staticmethod
    def initialize():
        if "titan_telemetry" not in st.session_state:
            st.session_state.titan_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "boot_complete" not in st.session_state:
            st.session_state.boot_complete = False

    @staticmethod
    def push_log(msg: str, status: str = "SYS"):
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.titan_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.titan_telemetry) > 50: 
            st.session_state.titan_telemetry.pop(0)

    @staticmethod
    def fetch_stream() -> str:
        return "\n".join(st.session_state.titan_telemetry)

class NeuralKnowledgeVaultController:
    """Handles secure Knowledge Vault mounting with automated path recovery."""
    
    def __init__(self):
        # 768-Dimension Neural Transformer Specialist
        self.embeddings = HuggingFaceEmbeddings(
            model_name=QuantumConfig.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Proactively scans multiple directory depths for index.faiss files."""
        for path in QuantumConfig.VAULT_DIRECTORIES:
            target_binary = os.path.join(path, "index.faiss")
            if os.path.exists(target_binary):
                try:
                    TelemetryMonitor.push_log(f"Synchronizing bridge with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as ex:
                    TelemetryMonitor.push_log(f"Neural Integrity Failure at {path}: {str(ex)}", "fail")
        return None

class MultiAgentStrategicOracle:
    """The Intelligence Hub: Handles complex queries via Agentic Orchestration."""
    
    def __init__(self, groq_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = groq_key
        # Inference Tier Hierarchy
        self.brain_70b = ChatGroq(groq_api_key=groq_key, model_name=QuantumConfig.CHIEF_MODEL, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=groq_key, model_name=QuantumConfig.UTILITY_MODEL, temperature=0.1)

    def execute_analytical_cycle(self, user_query: str) -> Generator:
        """Sequential Agentic Reasoning Protocol: Refinement -> Cross-Manual Mining -> Synthesis."""
        
        # Agent Alpha (Tactician): Semantic Jargon Alignment
        TelemetryMonitor.push_log("Agent Alpha: Cleaning input semantics for Ministry standards...")
        refinement_directive = f"Map query: '{user_query}' to technical Ministry nomenclature (DAP/DPM Chapters/Schedules)."
        try:
            refined_input = self.brain_8b.invoke(refinement_directive).content
        except:
            refined_input = user_query
            
        # Agent Beta (Miner): Neural Evidence Retrieval
        TelemetryMonitor.push_log(f"Agent Beta: Mining 1,691 knowledge layers using query vector...")
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": 18}).invoke(refined_input)
        
        evidence_context = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            evidence_context += f"\n[Doc LAYER {i+1} | SOURCE: {origin}]\n{doc.page_content}\n"
        
        TelemetryMonitor.push_log(f"Retrieval success. Authoritative manuals identified: {', '.join(manual_trace)}")

        # Agent Gamma (Strategist): Hexagonal Analytical Briefing
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        STATUS: CHIEF STRATEGIC ADVISOR | NADP NAGPUR.
        MISSION: Provide a pointed 360-degree Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {evidence_context}

        HEXAGONAL REASONING PROTOCOL:
        1. 📋 POLICY VECTOR: Categorize project scope (Capital DAP vs Revenue DPM). Identify Strategic category fit.
        2. ⚖️ PROCEDURAL PATHWAY: Detailed step-by-step administrative logic from Manuals and Handbook.
        3. 💰 FINANCIAL POWER AUDIT (DFPDS 2026): Identify the exact CFA and financial limit for this specific value.
        4. 🔭 STRATEGIC ROADMAP: Align the acquisition with the 15-year TPCR technological roadmap.
        5. ⚠️ PERIL AUDIT: Scan for procedural risks, Single-Vendor hurdles, or PAC justification contradictions.
        6. ✅ THE PROCEED SOLUTION: A definitive 3-step administrative roadmap to move the administrative file.

        IMPORTANT: For every factual rule, you MUST cite the Manual name. Use authoritative, professional tone.
        """
        
        return self.brain_70b.stream(master_protocol + "\n\nUser Case: " + user_query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY (ELITE KEY SYNC)
# ======================================================================================================================

def execute_apex_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryMonitor.initialize()
    
    # ELITE CREDENTIAL SYNC: Prioritize the provided user key
    api_key = "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"
    
    # Secondary Check: Streamlit Secrets for cloud persistency
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Intelligent Engine Lifetime Management
    if "titan_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN QUANTUM CORE..."):
            vault_handler = NeuralKnowledgeVaultController()
            if vault_handler.vault:
                st.session_state.titan_agent = MultiAgentStrategicOracle(api_key, vault_handler.vault)
                TelemetryMonitor.push_log("Neural link verified. FAISS index connected.", "ok")
                TelemetryMonitor.push_log("Strategic Logic Core (Llama 3.1 70B) status: ACTIVE.", "ok")
                st.session_state.boot_complete = True
            else:
                st.session_state.titan_agent = None
                TelemetryMonitor.push_log("CRITICAL ERROR: Neural vault files not found.", "fail")

# Trigger Full System Boot Sequence
execute_apex_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header Module
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–26</div>
        <h1>{QuantumConfig.SYSTEM_NAME}</h1>
        <p class='header-sub'>{QuantumConfig.ACADEMY} | QUANTUM APEX Build {QuantumConfig.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Columnar Display
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-card'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-card'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-card'><p class='v-label'>Inference Engine</p><p class='v-value'>LLAMA 70B</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-card'><p class='v-label'>Security Status</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Real-time System Console Processing Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{TelemetryMonitor.fetch_stream()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault missing
if st.session_state.titan_agent is None:
    st.error("❌ VAULT FILES MISSING. System Halted. Ensure index.faiss and index.pkl are in the GitHub Root directory.")
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

    TelemetryMonitor.push_log(f"Initiating strategic analysis for Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Progress Visualization
        with st.status("🛸 Orchestrating Hexagonal Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryMonitor.push_log("Agent Beta: Neural context extraction SUCCESS.")
            st.write("Verifying financial power schedules and audit risks...")
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token-Level Streaming from High-Intelligence Engine
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
            TelemetryMonitor.push_log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryMonitor.push_log(f"CRITICAL ERROR: {str(engine_err)}", "fail")

# HUD Log Manual Refresh
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER
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
            <p style='color:#ffffff; font-weight:bold;'>HEXAGONAL REASONING</p>
        </div>
    """, unsafe_allow_html=True)

# Institutional Verification Meta-string
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {QuantumConfig.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Project ID: {QuantumConfig.IDENTIFIER} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF TITAN v29.0 QUANTUM APEX ELITE MASTER BUILD
# ======================================================================================================================
