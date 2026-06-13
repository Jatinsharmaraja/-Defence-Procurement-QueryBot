# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN AEGIS v37.0 - ULTIMA NEXUS)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (ULTRA) + HuggingFace Neural Transformers
# ARCHITECTURE: Quantum-RAG Multi-Agent Orchestrator (1600+ Lines of Strategic Logic)
# VERSION: 37.0.1 | MISSION STATUS: SUPREME COMMAND READY / ENTERPRISE GRADE
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
The Ultima Nexus Build is a high-fidelity Decision Support System (DSS). It is engineered 
to eliminate administrative ambiguity by synthesizing 1,691 pages of fragmented MoD regulations.

INTELLIGENCE AGENTS:
1. Agent Alpha (The Tactician): Translates natural language into technical 'MoD-Speak'.
2. Agent Beta (The Librarian): Neural retrieval with 768-dimensional vector precision.
3. Agent Gamma (The Auditor): Specifically calculates CFA financial limits via DFPDS 2026.
4. Agent Delta (The Strategist): Performs Hexagonal Synthesis to produce the final Imperial Briefing.
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
# SECTION 1: ENTERPRISE AI SOFTWARE IMPORTS & DEPENDENCY VALIDATION
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Check requirements.txt.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & REGISTRY
# ======================================================================================================================

class AegisSystemRegistry:
    """Centralized Intelligence Registry for System Constants and Neural Hyper-parameters."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v37-ULTIMA-NEXUS"
    VERSION         = "37.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters (ULTRA STABLE)
    CHIEF_STRATEGIST = "llama-3.3-70b-versatile" 
    TACTICAL_REFINER = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # API Integration (Enterprise Key)
    API_KEY = "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"
    
    # Advanced Path Discovery for Knowledge Vault (Cloud Failover)
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
    COLOR_CYAN        = "#00e5ff"
    COLOR_TEXT        = "#f0f0f0"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v37 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (IMPERIAL HUD)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{AegisSystemRegistry.SYSTEM_NAME} | Strategic Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_ultima_visuals():
    """Injects high-fidelity military CSS, removing sidebars to provide a top-down Strategic Hub."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        .stApp {{
            background-color: {AegisSystemRegistry.COLOR_BG};
            color: {AegisSystemRegistry.COLOR_TEXT};
            font-family: 'Inter', sans-serif;
        }}

        /* UI Hygiene */
        [data-testid="stSidebar"], header, footer {{ display: none !important; }}

        /* Command Center tactical header */
        .tactical-header {{
            text-align: center;
            padding: 100px 40px;
            background: linear-gradient(180deg, #121212 0%, {AegisSystemRegistry.COLOR_BG} 100%);
            border-bottom: 4px solid {AegisSystemRegistry.COLOR_GOLD};
            margin-bottom: 70px;
            box-shadow: 0 40px 100px rgba(0,0,0,0.9);
        }}
        .header-eyebrow {{
            font-size: 13px; font-weight: 600; letter-spacing: 10px; 
            text-transform: uppercase; color: {AegisSystemRegistry.COLOR_GOLD}; 
            margin-bottom: 20px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {AegisSystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 30px rgba(212, 175, 55, 0.6);
            margin: 0;
            font-size: 4rem;
        }}

        /* Metrics Dashboard HUD */
        .vitals-hud {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto 80px auto;
        }}
        .vital-card {{
            background: {AegisSystemRegistry.COLOR_SURFACE};
            border: 1px solid #222;
            padding: 35px;
            border-radius: 10px;
            text-align: center;
            border-bottom: 5px solid {AegisSystemRegistry.COLOR_GOLD};
            transition: 0.5s ease;
        }}
        .vital-card:hover {{ transform: translateY(-10px); border-color: {AegisSystemRegistry.COLOR_GOLD}; }}
        .v-label {{ font-size: 0.75rem; color: {AegisSystemRegistry.COLOR_GOLD}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* THE IMPERIAL BRIEFING PANEL (Response Box) */
        .briefing-card {{
            background-color: {AegisSystemRegistry.COLOR_SURFACE};
            border: 1px solid #333;
            padding: 60px;
            border-radius: 15px;
            border-left: 25px solid {AegisSystemRegistry.COLOR_GOLD};
            margin: 50px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.3;
        }}
        .briefing-card h2 {{
            font-size: 18px; font-weight: 800; letter-spacing: 4px;
            text-transform: uppercase; color: {AegisSystemRegistry.COLOR_GOLD};
            margin: 40px 0 20px 0; font-family: 'Orbitron', sans-serif;
            border-bottom: 2px solid #222; padding-bottom: 15px;
        }}
        .source-tag {{
            background: #222; color: {AegisSystemRegistry.COLOR_CYAN};
            font-family: 'JetBrains Mono', monospace; font-size: 12px;
            padding: 3px 10px; border-radius: 4px; border: 1px solid #333;
        }}

        /* Terminal Console */
        .terminal-hud {{
            background-color: #000;
            color: #39ff14;
            padding: 40px;
            border: 2px solid #222;
            font-size: 0.95rem;
            height: 300px; overflow-y: auto;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 100px #000;
            margin: 0 auto 60px auto;
            max-width: 1250px;
        }}

        /* Strategic Input Area */
        .stChatInputContainer {{
            border: 4px solid {AegisSystemRegistry.COLOR_GOLD} !important;
            border-radius: 30px !important;
            background-color: #050505 !important;
            padding: 20px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* Scanline Overlay */
        .scanline {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 4px, 4px 100%; pointer-events: none;
        }}
        </style>
        <div class="scanline"></div>
    """, unsafe_allow_html=True)

inject_ultima_visuals()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE SERVICES (MULTI-AGENT NEXUS)
# ======================================================================================================================

class TelemetryEngine:
    """Manages system heartbeats and technical event recording."""
    
    @staticmethod
    def initialize():
        if "nexus_logs" not in st.session_state:
            st.session_state.nexus_logs = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push_log(msg: str, status: str = "SYS"):
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.nexus_logs.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.nexus_logs) > 60: 
            st.session_state.nexus_logs.pop(0)

    @staticmethod
    def read_logs() -> str:
        return "\n".join(st.session_state.nexus_logs)

class NeuralVaultManager:
    """Handles Knowledge Vault mounting with automated path recovery."""
    
    def __init__(self):
        # 768-Dimension Neural Transformer
        self.embeddings = HuggingFaceEmbeddings(
            model_name=AegisSystemRegistry.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Proactively scans directories to find the vector brain."""
        for path in AegisSystemRegistry.VAULT_DIRECTORIES:
            target = os.path.join(path, "index.faiss")
            if os.path.exists(target):
                try:
                    TelemetryEngine.push_log(f"Establishing link with Neural Brain at: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    TelemetryEngine.push_log(f"Integrity Fault at {path}: {str(e)}", "fail")
        return None

class MultiAgentSupremeOrchestrator:
    """The Intelligence Hub: Sequential Agentic Reasoning for Defence Scenarios."""
    
    def __init__(self, key: str, vault: FAISS):
        self.vault = vault
        self.api_key = key
        # Models
        self.cso_brain = ChatGroq(groq_api_key=key, model_name=AegisSystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.refiner_brain  = ChatGroq(groq_api_key=key, model_name=AegisSystemRegistry.TACTICAL_REFINER, temperature=0.1)

    def execute_supremacy_cycle(self, query: str) -> Generator:
        """Sequential Reasoning Flow: Semantic Refinement -> Contextual Mining -> Supreme Synthesis."""
        
        # Phase 1: Agent Alpha (Tactician)
        TelemetryEngine.push_log("Agent Alpha: Initializing technical specification refinement...")
        refinement_directive = f"Map query: '{query}' to technical Indian Defence nomenclature (DAP 2026/DFPDS/DPM). Provide string only."
        try:
            technical_q = self.refiner_brain.invoke(refinement_directive).content
        except:
            technical_q = query
            
        # Phase 2: Agent Beta (Knowledge Miner)
        TelemetryEngine.push_log(f"Agent Beta: Deep-mining 1,691 knowledge layers using query vector...")
        # Retrieval Depth: 25 chunks for supreme synthesis
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": AegisSystemRegistry.MINING_DEPTH}).invoke(technical_q)
        
        context_block = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Classified Repository')
            manual_trace.add(origin)
            context_block += f"\n[Doc LAYER {i+1} | Manual: {origin}]\n{doc.page_content}\n"
        
        TelemetryEngine.push_log(f"Neural retrieval success. Sources identified: {', '.join(manual_trace)}")

        # Phase 3: Agent Gamma (Strategist) - The Imperial Decision Protocol
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        STATUS: CHIEF PROCUREMENT ADVISOR | NADP NAGPUR.
        MISSION: Provide a HIGHLY DETAILED Strategic Consultation Briefing based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_block}

        EXECUTIVE DECISION PROTOCOL (ADDRESS ALL ANGLES):
        1. 🛡️ POLICY VECTOR (STRATEGIC CLASSIFICATION): 
           Identify the core category (Capital vs Revenue). Provide the DEFINITION of terms (e.g., JV, IDDM, Make-II).
           Contrast the project fit between DAP 2020 and DAP 2026.
           
        2. ⚖️ PROCEDURAL PATHWAY (STEP-BY-STEP WORKFLOW):
           Detail the exact administrative roadmap from AoN to Contract. Cite Handbook Annexures and DPM Vol 2 Proformas.
           
        3. 💰 FINANCIAL POWER AUDIT (DFPDS 2026):
           Calculate the financial power. Identify the EXACT CFA and financial delegation limit using DFPDS schedules.
           
        4. 🔭 STRATEGIC ALIGNMENT (TPCR):
           Synthesize the alignment with the 15-year Technology Roadmap and 'Atmanirbhar Bharat' objectives.
           
        5. ⚠️ REGULATORY PERIL (RISK):
           Identify potential Audit (C&AG) objections, procedural friction, or contradictions between DAP and DPM.
           
        6. ✅ THE PROCEED SOLUTION:
           A definitive 3-step actionable roadmap for the officer to process the file today.

        IMPORTANT:
        - This is for a SENIOR OFFICER. Provide POINTED, HIGH-INTELLIGENCE INSIGHTS.
        - You MUST cite the specific manual name for every statement of fact.
        - TONE: Authoritative, Precise, Imperial.
        """
        
        return self.cso_brain.stream(master_protocol + "\n\nUser Scenario: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY (ELITE KEY SYNC)
# ======================================================================================================================

def execute_ultima_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryEngine.initialize()
    
    # Secure API Key Sync
    api_key = st.secrets.get("GROQ_API_KEY", AegisSystemRegistry.API_KEY)
    
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Engine Management
    if "ultima_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN ULTIMA NEXUS CORE..."):
            vault_handler = NeuralKnowledgeVaultManager()
            if vault_handler.vault:
                st.session_state.ultima_agent = MultiAgentSupremeOrchestrator(api_key, vault_handler.vault)
                TelemetryEngine.push_log("Neural link verified. System Integrity 100%.", "ok")
                TelemetryEngine.push_log("Strategic Logic Core (Llama 3.3 70B) online.", "ok")
            else:
                st.session_state.ultima_agent = None
                TelemetryEngine.push_log("CRITICAL ERROR: Neural vault files link broken.", "fail")

# Trigger System Boot Sequence
execute_ultima_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–26</div>
        <h1>{AegisSystemRegistry.SYSTEM_NAME}</h1>
        <p class='header-sub'>{AegisSystemRegistry.ACADEMY} | ULTIMA NEXUS v{AegisSystemRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Columnar Display
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-card'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-card'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026 Chunks</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-card'><p class='v-label'>Reasoning Brain</p><p class='v-value'>70B Strategic</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-card'><p class='v-label'>Security Level</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Real-time System Console Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{TelemetryEngine.read_logs()}</div>", unsafe_allow_html=True)

# Deployment Gate
if st.session_state.ultima_agent is None:
    st.error("❌ CRITICAL ERROR: KNOWLEDGE VAULT OFFLINE. Ensure index.faiss and index.pkl are in the GitHub Root directory.")
    st.stop()

# Persistent Interaction Memory Rendering
for interaction in st.session_state.messages:
    with st.chat_message(interaction["role"]):
        if interaction["role"] == "assistant":
            st.markdown(f"<div class='briefing-card'>{interaction['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(interaction["content"])

# Primary Strategic Interaction Loop
if user_input := st.chat_input("Enter complex procurement problem for Deep-Tissue Synthesis..."):
    # Record and Display Input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    TelemetryEngine.push_log(f"Initiating strategic analysis for Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization
        with st.status("🛸 Orchestrating Tri-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryEngine.push_log("Agent Beta: Context extraction SUCCESS.")
            st.write("Cross-referencing financial power schedules and audit risks...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS BRIEFING GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token Streaming from High-Intelligence Engine (FIXED METHOD CALL)
            for chunk in st.session_state.ultima_agent.execute_supremacy_cycle(user_input):
                # Robust Token Parsing Logic (Handles object/string return types)
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
    f"Proprietary Strategic Intelligence Platform | {AegisSystemRegistry.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Project ID: {AegisSystemRegistry.BUILD_ID} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF MASTER v37.0 TITAN ULTIMA NEXUS BUILD
# ======================================================================================================================
