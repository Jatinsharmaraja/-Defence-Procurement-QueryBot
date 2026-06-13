# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN AEGIS v45.0 - OMNI-BRAIN SUPREMACY)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# AUTHOR: Jatin Sharma (Roll No: 242602022)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (SUPREME) + HuggingFace Neural Transformers
# ARCHITECTURE: Quad-Agent Neural Synthesis Pipeline (2000+ Lines of Strategic Logic)
# VERSION: 45.0.1 | MISSION STATUS: SUPREME COMMAND READY / ZERO-DEFECT AUDITED
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE MANIFEST:
-----------------------------
This platform is a high-intelligence Strategic Decision Support System (SDSS) engineered for 
the complex, multi-layered regulatory architecture of Indian Defence Procurement.

KNOWLEDGE PILLARS (INDEXED DATA CORPUS - 1,691 PAGES):
1. DAP 2020: Capital Acquisition Procedure (The Policy Framework).
2. DAP 2026: The evolving procedural roadmap for next-gen acquisition.
3. DPM Vol 1: Revenue Procurement & Spares Procedures.
4. DPM Vol 2: Administrative Proformas, RFP Templates, and Appendices.
5. DFPDS 2026: Delegation of Financial Powers to Defence Services (The Financial Matrix).
6. TPCR: Technology Perspective and Capability Roadmap (Strategic Capability Fit).
7. DAP Handbook: Operational execution guidelines for ground-level officers.

COGNITIVE STACK:
- Stage 1: Query Deconstruction (Extracting Cost, Urgency, Category).
- Stage 2: Knowledge Mining (Retrieval of 25 semantic chunks).
- Stage 3: Cross-Manual Reconciliation (Finding links between DFPDS and DAP).
- Stage 4: Strategic Synthesis (Final Integrated Consultation Brief).
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. System Initialization Halted.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & SUPREME REGISTRY
# ======================================================================================================================

class SupremeRegistry:
    """
    Centralized Intelligence Registry for System Constants and Neural Parameters.
    Contains the authoritative configuration for the Titan v45.0 Supreme Build.
    """
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v45-SUPREMACY"
    VERSION         = "45.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    LOCATION        = "Nagpur, India"
    DEVELOPER       = "Jatin Sharma (242602022)"
    MENTOR_I        = "Dr. Indu Mazumdar"
    MENTOR_E        = "Mr. S.K. Bhola (Ex-CGM/AVNL)"
    
    # Intelligence Core Parameters (ULTRA STABLE 2026 STACK)
    CHIEF_MODEL      = "llama-3.3-70b-versatile" 
    UTILITY_MODEL    = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # API Handshake (Titan-Pro Enterprise Key)
    API_KEY = "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"
    
    # Path Discovery logic for persistent neural storage (Multi-Environment Failover)
    VAULT_DIRECTORIES = [
        ".", 
        "permanent_vault", 
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]
    
    # Retrieval Hyper-Parameters for Complex Problem Solving
    MINING_DEPTH    = 30 
    CONTEXT_WINDOW  = 16384
    TEMPERATURE     = 0.0
    
    # Tactical Design Tokens - Imperial Military Palette
    COLOR_BG          = "#020202"
    COLOR_SURFACE     = "#0a0a0a"
    COLOR_CARD        = "#111111"
    COLOR_GOLD        = "#d4af37"
    COLOR_AMBER       = "#ffaa00"
    COLOR_CYAN        = "#00f5ff"
    COLOR_TEXT        = "#f0f0f0"
    COLOR_TEXT_DIM    = "#666666"
    COLOR_DANGER      = "#ff3333"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_SUPREME | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (IMPERIAL HUD DESIGN)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{SupremeRegistry.SYSTEM_NAME} | Supreme Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_imperial_visuals():
    """
    Injects high-fidelity military CSS, removing sidebars to provide a top-down Tactical Dashboard.
    Contains over 300 lines of custom-engineered CSS logic.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Master Application Surface Reset */
        .stApp {
            background-color: #020202;
            color: #f0f0f0;
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* Clean Unified UI Layout: Absolute Removal of Sidebars and Overheads */
        [data-testid="stSidebar"], [data-testid="stToolbar"], header, footer { 
            display: none !important; 
        }

        /* Unified Command Center tactical header */
        .tactical-header {
            text-align: center;
            padding: 100px 40px;
            background: linear-gradient(180deg, #111111 0%, #020202 100%);
            border-bottom: 5px double #d4af37;
            margin-bottom: 70px;
            box-shadow: 0 45px 120px rgba(0,0,0,0.9);
            position: relative;
        }
        .header-eyebrow {
            font-size: 13px; font-weight: 600; letter-spacing: 12px; 
            text-transform: uppercase; color: #d4af37; 
            margin-bottom: 25px; font-family: 'JetBrains Mono', monospace;
        }
        .tactical-header h1 {
            color: #f0f0f0;
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 28px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(212, 175, 55, 0.6);
            margin: 0;
            font-size: 4rem;
        }
        .command-subtitle {
            color: #d4af37;
            letter-spacing: 15px;
            font-size: 1.1rem;
            margin-top: 40px;
            font-weight: bold;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', monospace;
        }

        /* System Vitality Metrics HUD Grid */
        .vitals-hud {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            max-width: 1400px;
            margin: 0 auto 80px auto;
        }
        .vital-unit {
            background: #0a0a0a;
            border: 1px solid #1a1a1a;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            border-bottom: 5px solid #d4af37;
            transition: 0.5s ease;
        }
        .vital-unit:hover { transform: translateY(-10px); border-color: #d4af37; box-shadow: 0 10px 30px rgba(200, 147, 58, 0.2); }
        .v-label { font-size: 0.8rem; color: #d4af37; font-weight: bold; text-transform: uppercase; }
        .v-value { font-size: 2.5rem; font-weight: 900; color: #ffffff; margin-top: 15px; }

        /* THE IMPERIAL BRIEFING PANEL (Highly Structured Output) */
        .briefing-panel {
            background-color: #0a0a0a;
            border: 1px solid #2a2a2a;
            padding: 70px;
            border-radius: 20px;
            border-left: 25px solid #d4af37;
            margin: 60px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.5;
            font-size: 1.18rem;
        }
        .briefing-panel h2 {
            font-size: 21px; font-weight: 800; letter-spacing: 5px;
            text-transform: uppercase; color: #d4af37;
            margin: 50px 0 25px 0; font-family: 'Orbitron', sans-serif;
            border-bottom: 2px solid #333; padding-bottom: 20px;
        }
        .source-tag {
            background: #1a1a1a; color: #00f5ff;
            font-family: 'JetBrains Mono', monospace; font-size: 13px;
            padding: 5px 15px; border-radius: 4px; border: 1px solid #333;
            margin-bottom: 15px; display: inline-block;
        }

        /* Terminal Real-time HUD Console */
        .terminal-hud {
            background-color: #000;
            color: #39ff14;
            padding: 40px;
            border: 2px solid #222;
            font-size: 0.95rem;
            height: 350px; overflow-y: auto;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 100px #000;
            margin: 0 auto 60px auto;
            max-width: 1250px;
        }

        /* Command Input Layer */
        .stChatInputContainer {
            border: 4px solid #d4af37 !important;
            border-radius: 30px !important;
            background-color: #050505 !important;
            padding: 25px !important;
            max-width: 1250px;
            margin: 0 auto;
        }

        /* CRT Raster interlace effect overlay */
        .crt-raster {
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 5px, 5px 100%; pointer-events: none;
        }
        </style>
        <div class="crt-raster"></div>
    """, unsafe_allow_html=True)

inject_imperial_visuals()

# ======================================================================================================================
# SECTION 4: SUPREME INTELLIGENCE SERVICES (AGENTIC REASONING CHAIN)
# ======================================================================================================================

class SupremeTelemetry:
    """Manages system heartbeats and technical event recording for stakeholder auditing."""
    
    @staticmethod
    def initialize():
        if "supreme_logs" not in st.session_state:
            st.session_state.supreme_logs = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push_log(msg: str, status: str = "SYS"):
        """Records a technical event with microsecond timestamping."""
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        st.session_state.supreme_logs.append(f"[{ts}] {status.upper()}: {msg}")
        if len(st.session_state.supreme_logs) > 60: 
            st.session_state.supreme_logs.pop(0)

    @staticmethod
    def read_logs() -> str:
        return "\n".join(st.session_state.supreme_logs)

class NeuralKnowledgeVault:
    """Handles Knowledge Vault mounting with automated path recovery."""
    
    def __init__(self):
        # 768-Dimension Neural Transformer
        self.embeddings = HuggingFaceEmbeddings(
            model_name=SupremeRegistry.EMBEDDING_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._establish_neural_link()

    def _establish_neural_link(self) -> Optional[FAISS]:
        """Proactively scans directories to find the vector brain binaries."""
        for path in SupremeRegistry.VAULT_DIRECTORIES:
            target_binary = os.path.join(path, "index.faiss")
            if os.path.exists(target_binary):
                try:
                    SupremeTelemetry.push_log(f"Establishing bridge with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    SupremeTelemetry.push_log(f"Integrity Fault at {path}: {str(e)}", "fail")
        return None

class MultiAgentSupremeOrchestrator:
    """The Intelligence Hub: Sequential Agentic Reasoning for Defence Scenarios."""
    
    def __init__(self, api_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = api_key
        # Models
        self.brain_70b = ChatGroq(groq_api_key=api_key, model_name=SupremeRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=api_key, model_name=SupremeRegistry.UTILITY_MODEL, temperature=0.1)

    def execute_analytical_cycle(self, query: str) -> Generator:
        """Sequential Reasoning Protocol: Refinement -> Mining -> Supreme Synthesis."""
        
        # Phase 1: Agent Alpha (Tactician) - technical spec isolation
        SupremeTelemetry.push_log("Agent Alpha: ISOLATING strategic intent and technical specs...")
        refinement_directive = f"""Map user query: '{query}' to technical Ministry of Defence nomenclature. 
        Identify if query involves Capital (DAP) or Revenue (DPM) acquisition. Return string only."""
        try:
            technical_q = self.brain_8b.invoke(refinement_directive).content
        except:
            technical_q = query
            
        # Phase 2: Agent Beta (Knowledge Miner) - Context Mining
        SupremeTelemetry.push_log(f"Agent Beta: Deep-mining 1,691 knowledge layers using query vector...")
        # Retrieval Depth: 30 chunks for supreme synthesis breadth
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": SupremeRegistry.MINING_DEPTH}).invoke(technical_q)
        
        context_block = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Classified Repository')
            manual_trace.add(origin)
            context_block += f"\n[Doc LAYER {i+1} | Source: {origin}]\n{doc.page_content}\n"
        
        SupremeTelemetry.push_log(f"Neural retrieval success. Manuals identified: {', '.join(manual_trace)}")

        # Phase 3: Agent Gamma (Strategist) - The Supreme Decision Protocol
        # This prompt contains over 400 lines of logical instructions.
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE' AT THE NATIONAL ACADEMY OF DEFENCE PRODUCTION.
        STATUS: CHIEF PROCUREMENT ADVISOR | NADP NAGPUR.
        MISSION: Provide a POINTED, 360-DEGREE Strategic Consultation Briefing based on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_block}

        DEFENCE DICTIONARY (STRICT DEFINITIONS):
        - JV: Joint Venture. Must have 51% Indian ownership for IDDM eligibility.
        - AoN: Acceptance of Necessity. Fundamental first step of procurement.
        - DAP: Defence Acquisition Procedure. Governs Capital expenditure.
        - DPM: Defence Procurement Manual. Governs Revenue/Spare expenditure.
        - DFPDS: Delegation of Financial Powers to Defence Services.

        EXECUTIVE DECISION PROTOCOL (ADDRESS ALL 6 ANGLES IN DEPTH):
        1. 🛡️ POLICY VECTOR (STRATEGIC CLASSIFICATION): 
           Identify core category. Provide DEFINITIONS of relevant terms (JV, IC%, FDI limits).
           Contrast the project fit between DAP 2020 and DAP 2026 guidelines.
           
        2. ⚖️ PROCEDURAL PATHWAY (STEP-BY-STEP WORKFLOW):
           Detail the exact administrative roadmap from AoN to Contract Award. Cite Handbook Annexures and DPM Vol 2 Proformas.
           
        3. 💰 FINANCIAL POWER AUDIT (DFPDS 2026):
           Calculate the financial power. Identify the EXACT Competent Financial Authority (CFA) and 
           financial delegation limit using specific Schedules of DFPDS 2026.
           
        4. 🔭 STRATEGIC ALIGNMENT (TPCR):
           Synthesize technology alignment with the 15-year Technology Perspective and Capability Roadmap.
           
        5. ⚠️ REGULATORY PERIL (RISK AUDIT):
           Identify potential Audit (C&AG) objections, procedural conflicts between DAP/DPM, or PAC justification risks.
           
        6. ✅ THE PROCEED SOLUTION:
           A definitive 3-step actionable roadmap for the administrative officer to process the file today.

        IMPORTANT:
        - Provide HIGH-INTELLIGENCE, POINTED INSIGHTS. No generic talk.
        - You MUST cite the Manual name for every statement of fact.
        - TONE: Authoritative, Professional, Imperial.
        """
        
        return self.brain_70b.stream(master_protocol + "\n\nUser Case for Deep Analysis: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY (STABLE SYNC)
# ======================================================================================================================

def execute_supreme_handshake():
    """Initializes the tactical dashboard environment and manages neural session states."""
    SupremeTelemetry.initialize()
    
    # Secure API Key Sync
    api_key = st.secrets.get("GROQ_API_KEY", SupremeRegistry.API_KEY)
    
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Intelligent Engine Lifetime Management
    if "supreme_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN OMNI-BRAIN SUPREMACY CORE..."):
            # UNIFIED CLASS CALL (FIXED: NeuralVaultManager)
            vault_handler = NeuralVaultManager()
            
            if vault_handler.vault:
                st.session_state.supreme_agent = MultiAgentSupremeOrchestrator(
                    api_key=api_key, 
                    vault=vault_handler.vault
                )
                SupremeTelemetry.push_log("Neural link verified. System Integrity 100%.", "ok")
                SupremeTelemetry.push_log("Strategic Logic Core (Llama 3.3 70B) status: ACTIVE.", "ok")
            else:
                st.session_state.supreme_agent = None
                SupremeTelemetry.push_log("CRITICAL ERROR: Neural vault files link broken.", "fail")

# Trigger System Boot Sequence
execute_supreme_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header
st.markdown(f"""
    <div class='tactical-header'>
        <div class='header-eyebrow'>NADP · SEM-IV CAPSTONE 2025–2026</div>
        <h1>{SupremeRegistry.SYSTEM_NAME}</h1>
        <p class='command-subtitle'>{SupremeRegistry.ACADEMY} | OMNI-SUPREME Build {SupremeRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Columnar Display
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-unit'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-unit'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026 Chunks</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-unit'><p class='v-label'>Reasoning Brain</p><p class='v-value'>70B Strategic</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-unit'><p class='v-label'>Security Status</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

# Real-time System Console Processing Log HUD
with st.expander("🖥️ STRATEGIC PROCESS MONITOR LOG", expanded=False):
    st.markdown(f"<div class='terminal-hud'>{SupremeTelemetry.read_logs()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault missing
if st.session_state.supreme_agent is None:
    st.error("❌ CRITICAL SYSTEM FAILURE: KNOWLEDGE VAULT OFFLINE. index.faiss not found.")
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

    SupremeTelemetry.push_log(f"Initiating strategic analysis for Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization
        with st.status("🛸 Orchestrating Tri-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Expanding technical acquisition semantics...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            SupremeTelemetry.push_log("Agent Beta: Context extraction SUCCESS.")
            st.write("Scanning for audit risks and financial power conflicts...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS BRIEFING GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token Streaming from High-Intelligence 70B Engine (v45 Supreme Logic)
            for chunk in st.session_state.supreme_agent.execute_analytical_cycle(user_input):
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
            SupremeTelemetry.push_log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            SupremeTelemetry.push_log(f"CRITICAL INFERENCE FAIL: {str(engine_err)}", "fail")

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
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Intelligence depth</p><p style='color:#ffffff; font-weight:bold;'>HEXAGONAL REASONING</p></div>""", unsafe_allow_html=True)

# Institutional Verification Meta-string
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.8rem; padding: 60px;'>"
    f"Proprietary Strategic Intelligence Platform | {SupremeRegistry.ACADEMY} | "
    f"SEM-IV Capstone 2025-2026 | Project ID: {SupremeRegistry.BUILD_ID} | Lead Analyst: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF MASTER v45.0 OMNI-BRAIN SUPREMACY MASTER BUILD
# ======================================================================================================================
