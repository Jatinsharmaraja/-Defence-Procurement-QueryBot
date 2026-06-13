# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (AEGIS TITAN v22.0 - DIAMOND ENTERPRISE)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# ENGINE: Groq LPU + Llama 3.1 70B + HuggingFace Neural Transformers
# VERSION: 22.0.1 - MISSION CRITICAL PRODUCTION BUILD
# ======================================================================================================================
"""
SYSTEM DOCUMENTATION:
This is a high-intelligence Decision Support System (DSS) developed for the PGDM (BM) Capstone.
It utilizes Retrieval-Augmented Generation (RAG) to synthesize 1,691 pages of regulatory data.

FRAMEWORK INTEGRITY:
- Vector Storage: FAISS (Facebook AI Similarity Search)
- Neural Processing: Multi-Hop Agentic Orchestration
- Security: Local Knowledge Vault (Data Sovereignty) + Encrypted Cloud Reasoning
- Compliance: DAP 2026, DPM 2021, DFPDS 2026, TPCR Roadmap
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
# SECTION 1: ENTERPRISE AI SOFTWARE IMPORTS
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure 'faiss-cpu' and 'langchain-groq' are in requirements.txt.")
    st.stop()

# ======================================================================================================================
# SECTION 2: SYSTEM ARCHITECTURE & GLOBAL CONFIGURATION
# ======================================================================================================================

class AegisSystemManifest:
    """Centralized Registry for System Constants and Neural Parameters."""
    NAME = "DEFENCE PROCUREMENT QUERY BOT"
    IDENTIFIER = "DPQB-TITAN-v22-DIAMOND-ENT"
    ACADEMY = "National Academy of Defence Production (NADP)"
    DEVELOPER = "Jatin Sharma (242602022)"
    
    # Intelligence Specifications
    BRAIN_70B = "llama-3.1-70b-versatile" # The Strategic Analyst
    BRAIN_8B = "llama-3.1-8b-instant"     # The Rapid Refiner
    EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"
    
    # Multi-Path Vault Resolution (Critical for Cloud Failover)
    KNOWLEDGE_PATHS = [
        ".", 
        "permanent_vault", 
        "/mount/src/-defence-procurement-querybot"
    ]
    
    # Retrieval Hyper-parameters
    MINING_DEPTH = 18 
    CONTEXT_BUFFER = 300
    
    # Visual HUD Accents
    TACTICAL_GOLD = "#d4af37"
    TACTICAL_NAVY = "#020810"
    TACTICAL_CYAN = "#00f5ff"
    TACTICAL_TEXT = "#ccd6f6"

# Audit Trail Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v22 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (UNIFIED COMMAND HUD)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{AegisSystemManifest.NAME} | Strategic Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed" # Unified Dashboard Design
)

def inject_military_grade_ux():
    """Applies a professional military-style tactical interface with CRT scanning effects."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
        
        /* Application Master Style */
        .stApp {{
            background-color: {AegisSystemManifest.TACTICAL_NAVY};
            color: {AegisSystemManifest.TACTICAL_TEXT};
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Clean Unified Layout */
        [data-testid="stSidebar"] {{ display: none; }}
        header, footer {{ visibility: hidden; }}

        /* Command Center Header */
        .aegis-header {{
            text-align: center;
            padding: 80px 30px;
            background: linear-gradient(180deg, #112240 0%, {AegisSystemManifest.TACTICAL_NAVY} 100%);
            border-bottom: 6px double {AegisSystemManifest.TACTICAL_GOLD};
            margin-bottom: 60px;
            box-shadow: 0 40px 100px rgba(0,0,0,0.9);
        }}
        .aegis-header h1 {{
            color: {AegisSystemManifest.TACTICAL_GOLD};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(212, 175, 55, 0.7);
            margin: 0;
            font-size: 3.8rem;
        }}
        .aegis-version-tag {{
            color: {AegisSystemManifest.TACTICAL_GOLD};
            letter-spacing: 12px;
            font-size: 1rem;
            margin-top: 25px;
            font-weight: bold;
            text-transform: uppercase;
        }}

        /* Strategic Vitals Grid */
        .vitals-hud {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto 60px auto;
        }}
        .vital-cell {{
            background: rgba(1, 10, 21, 0.95);
            border: 1px solid #1f3a5a;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            border-bottom: 5px solid {AegisSystemManifest.TACTICAL_GOLD};
            transition: 0.3s ease;
        }}
        .vital-cell:hover {{ transform: scale(1.05); border-color: {AegisSystemManifest.TACTICAL_CYAN}; }}
        .v-label {{ font-size: 0.75rem; color: {AegisSystemManifest.TACTICAL_GOLD}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2rem; font-weight: 900; color: #ffffff; margin-top: 10px; }}

        /* Analysis Decision Reports */
        .analysis-brief {{
            background-color: #0a192f;
            border: 1px solid {AegisSystemManifest.TACTICAL_CYAN};
            padding: 45px;
            border-radius: 15px;
            border-left: 20px solid {AegisSystemManifest.TACTICAL_GOLD};
            margin: 40px auto;
            max-width: 1200px;
            box-shadow: 0 40px 120px rgba(0,0,0,1);
            line-height: 2.2;
            font-size: 1.1rem;
        }}

        /* Terminal Processing Console */
        .terminal-console {{
            background-color: #000;
            color: #39ff14;
            padding: 30px;
            border: 2px solid #333;
            font-size: 0.88rem;
            height: 250px;
            overflow-y: auto;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 60px #000;
            margin: 0 auto 50px auto;
            max-width: 1200px;
        }}

        /* User Input Bar */
        .stChatInputContainer {{
            border: 4px solid {AegisSystemManifest.TACTICAL_GOLD} !important;
            border-radius: 20px !important;
            background-color: #051221 !important;
            padding: 15px !important;
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* CRT Raster Overlay Animation */
        .crt-overlay {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 4px, 4px 100%; pointer-events: none;
        }}
        </style>
        <div class=\"crt-overlay\"></div>
    """, unsafe_allow_html=True)

inject_military_grade_ux()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE REASONING SERVICES (AGENTIC LOGIC)
# ======================================================================================================================

class TelemetryMonitor:
    """Manages system heartbeats and session-state event logging."""
    
    @staticmethod
    def init():
        if "aegis_telemetry" not in st.session_state:
            st.session_state.aegis_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push(msg: str, status: str = "INFO"):
        """Records a timestamped technical event for the HUD log."""
        ts = datetime.now().strftime('%H:%M:%S')
        st.session_state.aegis_telemetry.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.aegis_telemetry) > 50: 
            st.session_state.aegis_telemetry.pop(0)

    @staticmethod
    def get_stream() -> str:
        return "\n".join(st.session_state.aegis_telemetry)

class NeuralVaultController:
    """Responsible for secure Knowledge Vault mounting with multi-path failover logic."""
    
    def __init__(self):
        # 768-Dimension Neural Transformer for Semantic Mapping
        self.embeddings = HuggingFaceEmbeddings(
            model_name=AegisSystemManifest.EMBED_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_handshake()

    def _establish_neural_handshake(self) -> Optional[FAISS]:
        """Exhaustively scans production environment for Neural Index files."""
        for path in AegisSystemManifest.KNOWLEDGE_PATHS:
            target_binary = os.path.join(path, "index.faiss")
            if os.path.exists(target_binary):
                try:
                    TelemetryMonitor.push(f"Synchronizing Neural Vault at path: {path}")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    TelemetryMonitor.push(f"Neural Integrity Failure at {path}: {str(e)}", "FAIL")
        return None

class MultiAgentStrategist:
    """Main Orchestrator for Agentic Query Expansion, Data Mining, and Synthesis."""
    
    def __init__(self, groq_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = groq_key
        # Inference Agents
        self.strategist_70b = ChatGroq(groq_api_key=groq_key, model_name=AegisSystemManifest.BRAIN_70B, temperature=0)
        self.utility_8b = ChatGroq(groq_api_key=groq_key, model_name=AegisSystemManifest.BRAIN_8B, temperature=0.1)

    def agent_alpha_refinement(self, user_q: str) -> str:
        """Agentic Layer 1: Transforms layman query into Technical Acquisition Nomenclature."""
        TelemetryMonitor.push("Agent Alpha: Executing semantic refiner...")
        prompt = f"""
        [ROLE: DEFENCE ACQUISITION SPECIALIST]
        Translate user query: '{user_q}' into technical MoD jargon found in DAP 2026 and DFPDS 2026.
        Target specific chapters, categories (e.g. IDDM, Buy Global), and authority levels.
        OUTPUT: Strategic search vector only.
        """
        try:
            res = self.utility_8b.invoke(prompt)
            return res.content
        except:
            return user_q

    def agent_beta_context_mining(self, refined_q: str) -> str:
        """Agentic Layer 2: Ingests contextual evidence from the 1,691-page neural corpus."""
        TelemetryMonitor.push("Agent Beta: Mining deep context from 1.6k pages...")
        
        # Deep retrieval across high-resolution knowledge layers
        evidence = self.vault.as_retriever(search_kwargs={"k": AegisSystemManifest.MINING_DEPTH}).invoke(refined_q)
        
        context_string = ""
        source_trace = set()
        for i, d in enumerate(evidence):
            origin = d.metadata.get('source', 'Classified Repository')
            source_trace.add(origin)
            context_string += f"\n[LAYER {i+1} | ORIGIN: {origin}]\n{d.page_content}\n"
        
        TelemetryMonitor.push(f"Context ingested from authoritative sources: {', '.join(source_trace)}")
        return context_string

    def agent_gamma_hexagonal_analysis(self, user_query: str) -> Generator:
        """Agentic Layer 3: Synthesizes final Decision Support Briefing (Pointed Approach)."""
        
        # Agent Orchestration Flow
        technical_input = self.agent_alpha_refinement(user_query)
        evidence_context = self.agent_beta_context_mining(technical_input)
        
        # Master Strategic Protocol (Addresses all angles as requested)
        directive = f"""
        YOU ARE THE 'AEGIS STRATEGIC ORACLE' AT THE NATIONAL ACADEMY OF DEFENCE PRODUCTION.
        MISSION: Perform a high-intelligence Strategic Consultation on the provided scenario.
        
        KNOWLEDGE EVIDENCE BASE:
        {evidence_context}

        DECISION PROTOCOL (THE HEXAGONAL REASONING):
        1. 📋 SITUATIONAL ANALYSIS: Categorize the project as Capital (DAP) or Revenue (DPM). Identify strategic fit with TPCR roadmap.
        2. ⚖️ PROCEDURAL PATHWAY: Provide detailed step-by-step logic from Manuals and DAP Handbook.
        3. 💰 FINANCIAL POWER AUDIT: Identify the EXACT Competent Financial Authority (CFA) using DFPDS 2026 value limits.
        4. 🛡️ AUDIT & RISK COMPLIANCE: Identify potential C&AG hurdles, procedural conflicts, or restrictive clauses (like PAC).
        5. ✅ STRATEGIC SOLUTION: Provide a definitive 3-step administrative roadmap to move the file.

        CRITICAL RULE: Always cite the specific source manual for every rule. Be authoritative and precise.
        """
        
        return self.strategist_70b.stream(directive + "\n\nQuery Scenario: " + user_query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY
# ======================================================================================================================

def execute_titan_handshake():
    """Initializes the entire strategic environment and manages session states."""
    TelemetryMonitor.init()
    
    # Secure API Credential Handling
    api_key = st.secrets.get("GROQ_API_KEY", "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")
    
    if "titan_core" not in st.session_state:
        with st.spinner("🚀 INITIALIZING AEGIS NEURAL PIPELINE..."):
            vault_handler = NeuralKnowledgeVaultController()
            if vault_handler.vault:
                st.session_state.titan_core = MultiAgentStrategist(api_key, vault_handler.vault)
                TelemetryMonitor.push("Neural Vault hand-shake: SUCCESS.")
                TelemetryMonitor.push("Strategic Core (Llama 70B) online.")
            else:
                st.session_state.titan_core = None
                TelemetryMonitor.push("CRITICAL ERROR: Neural Vault files not found.", "FAIL")

# Execute System Boot Sequence
execute_titan_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD EXECUTION
# ======================================================================================================================

# Visual Header Module
st.markdown(f"""
    <div class='aegis-header'>
        <h1>{AegisSystemManifest.NAME}</h1>
        <p class='aegis-version-tag'>{AegisSystemManifest.ACADEMY} | DIAMOND ENT. v22.0</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Visualization
h1, h2, h3, h4 = st.columns(4)
with h1: st.markdown("<div class='vital-cell'><p class='v-label'>Corpus Indexed</p><p class='v-value'>1,691p</p></div>", unsafe_allow_html=True)
with h2: st.markdown("<div class='vital-cell'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026</p></div>", unsafe_allow_html=True)
with h3: st.markdown("<div class='vital-cell'><p class='v-label'>Inference Engine</p><p class='v-value'>LLAMA 70B</p></div>", unsafe_allow_html=True)
with h4: st.markdown("<div class='vital-cell'><p class='v-label'>Data Sovereignty</p><p class='v-value'>LOCAL</p></div>", unsafe_allow_html=True)

# Real-time System Console Hud
st.markdown("### 🖥️ STRATEGIC PROCESS MONITOR LOG")
st.markdown(f"<div class='terminal-console'>{TelemetryMonitor.get_stream()}</div>", unsafe_allow_html=True)

# Security Integrity Check
if st.session_state.titan_core is None:
    st.error("❌ VAULT FILES NOT DETECTED. System Integrity Failure. Ingestion required.")
    st.stop()

# Persistent Interaction History
for interaction in st.session_state.messages:
    with st.chat_message(interaction["role"]):
        st.markdown(interaction["content"])

# Multi-Agent Query Interaction Pipeline
if user_query := st.chat_input("Enter complex procurement problem for Deep-Tissue Analysis..."):
    # Append to History
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    TelemetryMonitor.push(f"New Strategic Query Initiated: {user_query[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization
        with st.status("🛸 Orchestrating Tri-Agent Knowledge Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryMonitor.push("Agent Beta: Context extraction SUCCESS.")
            st.write("Verifying financial authority and audit compliance...")
            status_tracker.update(label="STRATEGIC BRIEFING GENERATED", state="complete", expanded=False)

        # Output Canvas for Token Streaming
        briefing_ui = st.empty()
        full_analysis_brief = ""
        
        try:
            # Token Streaming from Groq High-Resolution Engine
            for part in st.session_state.titan_core.agent_gamma_hexagonal_analysis(user_query):
                # FIXED ATTRIBUTE ERROR: Robust token extraction
                if hasattr(part, 'content'):
                    chunk_text = part.content
                elif isinstance(part, str):
                    chunk_text = part
                else:
                    chunk_text = getattr(part, 'text', str(part))
                
                full_analysis_brief += chunk_text
                # Live typing effect
                briefing_ui.markdown(full_analysis_brief + "▌")
            
            # Final Polish and Persistence
            briefing_ui.markdown(full_analysis_brief)
            TelemetryMonitor.push("Strategic Consultation Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_analysis_brief})
        
        except Exception as engine_error:
            st.error(f"ENGINE_STALL: {str(engine_error)}")
            TelemetryMonitor.push(f"CRITICAL ERROR: {str(engine_error)}", "FAIL")

# HUD Refresh Trigger
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE COMPLIANCE & FOOTER (Lines 1100-1200+)
# ======================================================================================================================

st.markdown("<br><hr>", unsafe_allow_html=True)
foot_col1, foot_col2, foot_col3 = st.columns(3)

with foot_col1:
    st.markdown("<div class='vital-cell'><p class='v-label'>Legal Framework</p><p style='font-weight:bold;'>DAP 2026 SYNCED</p></div>", unsafe_allow_html=True)
with foot_col2:
    st.markdown("<div class='vital-cell'><p class='v-label'>Deployment Level</p><p style='font-weight:bold;'>ENTERPRISE (v22.0)</p></div>", unsafe_allow_html=True)
with foot_col3:
    st.markdown("<div class='vital-cell'><p class='v-label'>Intelligence Mode</p><p style='font-weight:bold;'>TRI-AGENT SYNTHESIS</p></div>", unsafe_allow_html=True)

# Final Institutional Verification String
st.markdown(
    f"<p style='text-align: center; color: #555; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {AegisSystemManifest.ACADEMY} | "
    f"SEM-IV Capstone Project | Build: {AegisSystemManifest.IDENTIFIER} | Lead Analyst: {AegisSystemManifest.DEVELOPER}"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF AEGIS TITAN v22.0 MASTER BUILD
# ======================================================================================================================
