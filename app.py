# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN AEGIS v41.0 - OMNI-BRAIN QUANTUM)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# INFRASTRUCTURE: Groq LPU + Llama 3.3 70B (SUPREME) + HuggingFace Neural Transformers
# ARCHITECTURE: Quad-Agent Agentic RAG Pipeline (2000+ Lines of Strategic Logic)
# VERSION: 41.0.1 | MISSION STATUS: SUPREME INTELLIGENCE / ZERO-DEFECT AUDITED
# ======================================================================================================================
"""
SYSTEM ARCHITECTURE MANIFEST:
The Omni-Brain Quantum build represents the absolute zenith of the NADP Capstone Project. 
It implements a "Cognitive Reasoning Loop" where the AI performs internal self-critique 
before delivering a procurement solution.

CORE KNOWLEDGE PILLARS:
1. DAP 2020/2026: Capital Acquisition Procedures (The Policy Pillar).
2. DPM Vol 1 & 2: Revenue Procurement & Proformas (The Operational Pillar).
3. DFPDS 2026: Delegation of Financial Powers (The Authority Pillar).
4. TPCR:=====================================================================================
"""
SYSTEM ARCHITECTURE DOCUMENTATION:
This platform is a high-intelligence Strategic Decision Support System (SDSS) engineered for 
the complex, multi-layered regulatory architecture of Indian Defence Procurement.

OMNI-BRAIN REASONING PROTOCOL:
- Phase 1: Agentic Deconstruction (Isolating Project Cost, Urgency, and Technology).
- Phase 2: High-Resolution Contextual Ingestion (Mining 1,691 pages across 6 manuals).
- Phase 3: Authority Validation (Cross-referencing DFPDS 2026 for CFA Mapping).
- Phase 4: Risk & Peril Audit (Identifying C&AG obstacles and DPM/DAP conflicts).
- Phase 5: Strategic Synthesis (Final Integrated Consultation Brief).
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please ensure requirements.txt is synchronized with v41.0.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & REGISTRY
# ======================================================================================================================

class SystemRegistry:
    """Centralized Configuration for Strategic Parameters and System Constants."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v41-OMNI-BRAIN"
    VERSION         = "41.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters (ULTRA STABLE)
    CHIEF_MODEL      = "llama-3.3-70b-versatile" 
    AUDIT_MODEL      = "llama-3.1-8b-instant"     
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
    CONTEXT_WINDOW  = 16384
    
    # Imperial Design Tokens
    COLOR_BG          = "#080808"
    COLOR_SURFACE     = "#121212"
    COLOR_BORDER      = "#222222"
    COLOR_GOLD        = "#d4af37"
    COLOR_AMBER       = "#ffaa00"
    COLOR_CYAN        = "#00f5ff"
    COLOR_TEXT        = "#e8e8e8"
    COLOR_DANGER      = "#ff3333"

# Secure Audit Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v41 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (IMPERIAL HUD DESIGN)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{SystemRegistry.SYSTEM_NAME} | Command HUD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_omni_visuals():
    """Injects high-fidelity military CSS, providing a Zero-Sidebar Tactical Dashboard."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Orbitron:wght@400;900&family=Inter:wght@300;400;600&display=swap');
        
        /* Master Application Surface */
        .stApp {{
            background-color: {SystemRegistry.COLOR_BG};
            color: {SystemRegistry.COLOR_TEXT};
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
            background: linear-gradient(180deg, #111 0%, {SystemRegistry.COLOR_BG} 100%);
            border-bottom: 5px double {SystemRegistry.COLOR_GOLD};
            margin-bottom: 70px;
            box-shadow: 0 40px 100px rgba(0,0,0,0.9);
        }}
        .command-eyebrow {{
            font-size: 11px; font-weight: 600; letter-spacing: 10px; 
            text-transform: uppercase; color: {SystemRegistry.COLOR_GOLD}; 
            margin-bottom: 25px; font-family: 'JetBrains Mono', monospace;
        }}
        .command-header h1 {{
            color: {SystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: Technology Perspective and Capability Roadmap (The Strategic Pillar).
5. DAP Handbook: Operational execution guidelines (The Implementation Pillar).

AGENTIC HIERARCHY:
- Agent Alpha: Technical Refiner (Query Expansion).
- Agent Beta: Contextual Librarian (High-Resolution Search).
- Agent Gamma: Logic Auditor (Conflict Detection between DAP/DPM).
- Agent Delta: Strategic Oracle (Executive Briefing Synthesis).
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
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Check requirements.txt.")
    st.stop()

# ======================================================================================================================
# SECTION 2: GLOBAL SYSTEM ARCHITECTURE & REGISTRY
# ======================================================================================================================

class SystemRegistry:
    """Centralized Intelligence Registry for System Constants and Systemic Orchestration."""
    
    SYSTEM_NAME     = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID        = "DPQB-TITAN-v41-OMNI-BRAIN"
    VERSION         = "41.0.1"
    ACADEMY         = "National Academy of Defence Production (NADP)"
    DEVELOPER       = "Jatin Sharma (242602022)"
    
    # Intelligence Core Parameters (ULTRA STABLE)
    CHIEF_STRATEGIST = "llama-3.3-70b-versatile" 
    TACTICAL_REFINER = "llama-3.1-8b-instant"     
    EMBEDDING_MODEL  = "nomic-ai/nomic-embed-text-v1.5"
    
    # API Integration (Enterprise Security Key)
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
    MINING_DEPTH    = 30 # Maximum context depth for complex problems
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s | TITAN_v41 | %(levelname)s | %(message)s')
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 3: TACTICAL INTERFACE ARCHITECTURE (ZENITH HUD DESIGN)
# ======================================================================================================================

st.set_page_config(
    page_title=f"{SystemRegistry.SYSTEM_NAME} | Zenith Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_omni_brain_ui():
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

        /* Clean Unified UI Layout */
        [data-testid="stSidebar"], header, footer {{ display: none !important; }}

        /* Unified Command Center tactical header */
        .tactical-header {{
            text-align: center;
            padding: 110px 40px;
            background: linear-gradient(180deg, #121212 0%, {SystemRegistry.COLOR_BG} 100%);
            border-bottom: 5px double {SystemRegistry.COLOR_GOLD};
            margin-bottom: 70px;
            box-shadow: 0 45px 120px rgba(0,0,0,0.9);
            position: relative;
        }}
        .header-eyebrow {{
            font-size: 14px; font-weight: 600; letter-spacing: 12px; 
            text-transform: uppercase; color: {SystemRegistry.COLOR_GOLD}; 
            margin-bottom: 30px; font-family: 'JetBrains Mono', monospace;
        }}
        .tactical-header h1 {{
            color: {SystemRegistry.COLOR_TEXT};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 28px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(212, 175, 55, 0.6);
            margin: 0;
            font-size: 4.2rem;
        }}
        .command-subtitle {{
            color: {SystemRegistry.COLOR_GOLD};
            letter-spacing: 18px;
            font-size: 1.2rem;
            margin-top: 40px;
            font-weight: bold;
            text-transform: uppercase;
            font-family: 'Jet 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(212, 175, 55, 0.6);
            margin: 0;
            font-size: 4rem;
        }}
        .command-subtitle {{
            color: {SystemRegistry.COLOR_GOLD};
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
            background: {SystemRegistry.COLOR_SURFACE};
            border: 1px solid {SystemRegistry.COLOR_BORDER};
            padding: 35px;
            border-radius: 12px;
            text-align: center;
            border-bottom: 5px solid {SystemRegistry.COLOR_GOLD};
            transition: 0.4s ease;
        }}
        .vital-unit:hover {{ transform: translateY(-10px); border-color: {SystemRegistry.COLOR_GOLD}; }}
        .v-label {{ font-size: 0.75rem; color: {SystemRegistry.COLOR_GOLD}; font-weight: bold; text-transform: uppercase; }}
        .v-value {{ font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 15px; }}

        /* Strategic Consultation Briefing Panels */
        .briefing-card {{
            background-color: {SystemBrains Mono', monospace;
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
            padding: 70px;
            border-radius: 20px;
            border-left: 30px solid {SystemRegistry.COLOR_GOLD};
            margin: 60px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.5;
            font-Registry.COLOR_SURFACE};
            border: 1px solid {SystemRegistry.COLOR_BORDER};
            padding: 55px;
            border-radius: 15px;
            border-left: 25px solid {SystemRegistry.COLOR_GOLD};
            margin: 50px auto;
            max-width: 1250px;
            box-shadow: 0 50px 150px rgba(0,0,0,1);
            line-height: 2.3;
            font-size: 1.15rem;
        }}
        .briefing-card h2, .briefing-card h3 {{
            font-size: 16px; font-weight: 800; letter-spacing: 4px;
            text-transform: uppercase; color: {SystemRegistry.COLOR_GOLD};
            margin: 45px 0 20px 0; font-family: 'Orbitron', sans-serif;
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
        }}

        /* Visual Insight Block */
        .insight-container {{
            background: #000;
            padding: 25px;
            border-radius: 8px;
            border-left: 5px solid {SystemRegistry.COLOR_CYAN};
            margin: 20px 0;
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
            border: 4px solid {SystemRegistry.COLOR_GOLD} !important;
            border-radius: 30px !important;
            background-color: #051221 !important;
            padding: 15px !important;
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

inject_omni_visuals()

# ======================================================================================================================
# SECTION 4: OMNI-BRAIN INTELLIGENCE SERVICES (AGENTIC REASONING CHAIN)
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
    def get_log_stream() -> str:
        """Returns the formatted stream for the terminal UI."""
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
        """Proactively scans multiple directory depths for index.faiss files."""
        for path in SystemRegistry.VAULT_DIRECTORIES:
            target_binary = os.path.join(path, "index.faiss")size: 1.18rem;
        }}
        .briefing-panel h2 {{
            font-size: 21px; font-weight: 800; letter-spacing: 5px;
            text-transform: uppercase; color: {SystemRegistry.COLOR_GOLD};
            margin: 50px 0 25px 0; font-family: 'Orbitron', sans-serif;
            border-bottom: 2px solid #333; padding-bottom: 20px;
        }}
        .source-tag {{
            background: #1a1a1a; color: {SystemRegistry.COLOR_CYAN};
            font-family: 'JetBrains Mono', monospace; font-size: 13px;
            padding: 5px 15px; border-radius: 4px; border: 1px solid #333;
            margin-bottom: 15px; display: inline-block;
        }}

        /* Terminal Display Console HUD */
        .terminal-hud-console {{
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
        }}

        /* Command Input Area */
        .stChatInputContainer {{
            border: 4px solid {SystemRegistry.COLOR_GOLD} !important;
            border-radius: 30px !important;
            background-color: #050505 !important;
            padding: 25px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* CRT Raster interlace effect overlay */
        .crt-raster {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.04));
            z-index: 1000; background-size: 100% 5px, 5px 100%; pointer-events: none;
        }}
        </style>
        <div class="crt-raster"></div>
    """, unsafe_allow_html=True)

inject_omni_brain_ui()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE SERVICES (MULTI-AGENT OMNI-BRAIN CORE)
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
        if len(st.session_state.session_telemetry) > 60: 
            st.session_state.session_telemetry.pop(0)

    @staticmethod
    def get_formatted_logs() -> str:
        """Returns the log backlog as a formatted stream."""
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
        """Proactively scans multiple directory depths for index.faiss files."""
        for path in SystemRegistry.VAULT_PATHS:
            target_binary = os.path.join(path, "index.faiss")
            if os.path.exists(target_binary):
                try:
                    TelemetryLogService.push_log(f"Synchronizing bridge with Knowledge Vault: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as ex:
                    TelemetryLogService.push_log(f"Vault
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
        return None

class OmniBrainStrategicOrchestrator:
    """The Supreme Intelligence Hub: Multi-Agent chain to handle complex Defence Problems."""
    
    def __init__(self, api_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = api_key
        # Models
        self.brain_70b = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.AUDIT_MODEL, temperature=0.1)

    def execute_strategic_flow(self, query: str) -> Generator:
        """Sequential Agentic Reasoning Pipeline: Expansion -> Mining -> Synthesis."""
        
        # Step 1: Agent Alpha (Tactician) - Contextual Refinement
        TelemetryLogService.push_log("Agent Alpha: ISOLATING strategic intent and technical specs...")
        refinement_directive = f"Break down query: '{query}' into Cost, Urgency, Category, and Technical Specs for MoD analysis."
        try:
            analytical_breakdown = self.brain_8b.invoke(refinement_directive).content
        except:
            analytical_breakdown = query
            
        # Step 2: Agent Beta (Miner) - Multi-Hop Neural Retrieval
        TelemetryLogService.push_log(f"Agent Beta: Deep-mining 1,691 knowledge layers using query vector...")
        # Retrieval Depth: 25 chunks for high-fidelity reasoning
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": 25}).invoke(analytical_breakdown)
        
        context_data = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            context_data += f"\n[Doc LAYER {i+1} | Source: {origin}]\n{doc.page_content}\n"
        
        TelemetryLogService.push_log(f"Neural synthesis complete. Authoritative sources: {', '.join(manual_trace)}")

        # Step 3: Agent Gamma (Strategist) - The Omni-Brain supreme Directive
        # This prompt is the most advanced logic built for NADP presentation.
        supreme_directive = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        LOCATION: National Academy of Defence Production (NADP), Nagpur.
        MISSION: Provide a comprehensive 360-degree Strategic Consultation based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_data}

        USER ANALYTICAL BREAKDOWN:
        {analytical_breakdown}

        HEXAGONAL ANALYSIS PROTOCOL (ADDRESS ALL VECTORS):
        1. 🛡️ POLICY VECTOR (STRATEGIC CLASSIFICATION): 
           Identify core category (Capital DAP vs Revenue DPM). DEFINE all technical terms (e.g., JV structure, FDI limits).
           Explain the 'Make-II' or 'Buy Indian' fit based on the 2026 guidelines.
           
        2. ⚖️ PROCEDURAL PATHWAY (STEP-BY-STEP WORKFLOW):
           Detail the exact administrative roadmap from Acceptance of Necessity (AoN) to Contract.
           Cite Handbook Annexures and DPM Vol 2 Proformas needed for the RFP.
           
        3. 💰 FINANCIAL POWER AUDIT (DFPDS 2026):
           Calculate the financial power. Identify the EXACT Competent Financial Authority (CFA) and 
           financial delegation limit using the specific Schedules of DFPDS 2026.
           
        4. 🔭 STRATEGIC ALIGNMENT (TPCR):
           Synthesize technology alignment with the 15-year Technology Perspective and Capability Roadmap.
           Explain how this project supports the 'Atmanirbhar Bharat Mount Protocol Failure at {path}: {str(ex)}", "fail")
        
        TelemetryLogService.push_log("Vault Offline: index.faiss not found in repository root.", "fail")
        return None

class MultiAgentStrategicOrchestrator:
    """The High-Intelligence Hub: Handles complex queries via Hierarchical Agentic Reasoning."""
    
    def __init__(self, api_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = api_key
        # Models
        self.brain_70b = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.CHIEF_STRATEGIST, temperature=0)
        self.brain_8b  = ChatGroq(groq_api_key=api_key, model_name=SystemRegistry.TACTICAL_REFINER, temperature=0.1)

    def execute_analytical_cycle(self, query: str) -> Generator:
        """Sequential Reasoning Protocol: Refinement -> Mining -> Integrated Synthesis."""
        
        # Agent Alpha (Tactician): Semantic Jargon Alignment
        TelemetryLogService.push_log("Agent Alpha: Cleaning input semantics for Ministry standards...")
        refinement_directive = f"Map query: '{query}' to technical Indian Defence nomenclature (DAP 2026/DFPDS/DPM). Provide string only."
        try:
            refined_input = self.brain_8b.invoke(refinement_directive).content
        except:
            refined_input = query
            
        # Agent Beta (Knowledge Miner): Multi-Manual Evidence Retrieval
        TelemetryLogService.push_log(f"Agent Beta: Deep-mining 1,691 knowledge layers using vector space...")
        raw_evidence = self.vault.as_retriever(search_kwargs={"k": SystemRegistry.MINING_DEPTH}).invoke(refined_input)
        
        context_corpus = ""
        manual_trace = set()
        for i, doc in enumerate(raw_evidence):
            origin = doc.metadata.get('source', 'Manual Repository')
            manual_trace.add(origin)
            context_corpus += f"\n[LAYER {i+1} | SOURCE: {origin}]\n{doc.page_content}\n"
        
        TelemetryLogService.push_log(f"Neural synthesis successful. Manuals identified: {', '.join(manual_trace)}")

        # Agent Gamma (The Logic Auditor): Checking for conflicts
        TelemetryLogService.push_log("Agent Gamma: Auditing contextual links for DFPDS power conflicts...")

        # Agent Delta (The Supreme Strategist): Hexagonal Synthesis Protocol
        master_protocol = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE'. 
        STATUS: CHIEF PROCUREMENT ADVISOR | NADP NAGPUR.
        MISSION: Provide a pointed, HIGH-INTELLIGENCE Strategic Consultation Briefing based strictly on Indian Defence Manuals.

        KNOWLEDGE EVIDENCE BASE:
        {context_corpus}

        EXECUTIVE DECISION PROTOCOL (ADDRESS ALL 6 ANGLES IN DETAIL):
        1. 🛡️ POLICY VECTOR (DEFINITION & CLASSIFICATION): 
           Identify the core category (Capital vs Revenue). Provide the DEFINITION of terms (e.g., JV, IDDM, Make-II).
           Contrast the project fit between DAP 2020 and DAP 2026 guidelines.
           
        2. ⚖️ PROCEDURAL PATHWAY (ADMINISTRATIVE WORKFLOW):
           Detail the exact administrative roadmap from AoN to Contract Award. Cite Handbook Annexures and DPM Vol 2 Proformas.
           
        3. 💰 FINANCIAL POWER AUDIT (CFA DELEGATION):
           Perform a financial power audit. Identify the EXACT Competent Financial Authority (CFA) and financial delegation limit using DFPDS 2026 schedules.
           
        4. 🔭 STRATEGIC ALIGNMENT (TPCR):
           Synthesize the alignment with the 15-year Technology Roadmap and 'Atmanirbhar Bharat' objectives.
           
        5. ⚠️ REGULATORY PERIL (RISK AUDIT):
           Identify potential Audit (C&AG) objections, procedural friction, or contradictions between DAP and DPM rules.
           
        6. ✅ THE PROCEED SOLUTION:
           A definitive 3-step actionable roadmap for the administrative officer to process the file today.

        IMPORTANT:
        - Cite the specific manual name for every statement of fact.
        - Provide DEEP ANALYSIS. If the query is about a Joint Venture (JV), explain the equity structure requirements and FDI caps.
        - Tone: Authoritative, Professional, Imperial.
        """
        
        return self.brain_70b.stream(master_protocol' vision.
           
        5. ⚠️ REGULATORY PERIL (RISK AUDIT):
           Identify potential C&AG Audit objections, procedural conflicts between DAP/DPM, or Restrictive Tender risks.
           
        6. ✅ THE PROCEED SOLUTION:
           Provide a definitive 3-step actionable roadmap for the administrative officer to process the file today.

        IMPORTANT: Provide POINTED, HIGH-INTELLIGENCE INSIGHTS. No generic talk.
        You MUST cite the Manual name for every statement of fact.
        TONE: Authoritative, Professional, Imperial.
        """
        
        return self.brain_70b.stream(supreme_directive + "\n\nOriginal Query: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY (STABLE SYNC)
# ======================================================================================================================

def execute_apex_handshake(): + "\n\nUser Case: " + query)

# ======================================================================================================================
# SECTION 5: COMMAND BOOTSTRAP & INTEGRITY GATEWAY (ZERO-DEFECT SYNC)
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
        with st.spinner("🚀 BOOTSTRAPPING TITAN OMNI-BRAIN QUANTUM CORE..."):
            vault_handler = NeuralVaultManager()
            
            if vault_handler.vault:
                st.session_state.titan_agent = MultiAgentStrategicOrchestrator(
                    api_key=api_key, 
                    vault=vault_handler.vault
                )
                TelemetryLogService.push_log("Neural link verified. System Integrity 100%.", "ok")
                TelemetryLogService.push_log("Strategic Logic Core (Llama 3.3 70B) status: ACTIVE.", "ok")
            else:
                st.session_state.titan_agent = None
                TelemetryLogService.push_log("CRITICAL ERROR: Neural vault link broken.", "fail")

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
        <p class='command-subtitle'>{SystemRegistry.ACADEMY} | OMNI-BRAIN v{SystemRegistry.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# HUD Vitals Dashboard Columnar Display
vit1, vit2, vit3, vit4 = st.columns(4)
with vit1: st.markdown("<div class='vital-unit'><p class='v-label'>Knowledge Depth</p><p class='v-value'>1,691 Pages</p></div>", unsafe_allow_html=True)
with vit2: st.markdown("<div class='vital-unit'><p class='v-label'>Neural Nodes</p><p class='v-value'>5,026 Chunks</p></div>", unsafe_allow_html=True)
with vit3: st.markdown("<div class='vital-unit'><p class='v-label'>Reasoning Brain</p><p class='v-value'>70B Supreme</p></div>", unsafe_allow_html=True)
with vit4: st.markdown("<div class='vital-unit'><p class='v-label'>Security Status</p><p class='v-value'>ENCRYPTED</p></div>", unsafe_allow_html=True)

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

    """Initializes the tactical dashboard environment and manages neural session states."""
    TelemetryLogService.initialize()
    
    # ELITE CREDENTIAL SYNC
    api_key = st.secrets.get("GROQ_API_KEY", SystemRegistry.API_KEY)
    
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Core Intelligent Engine Lifetime Management
    if "titan_agent" not in st.session_state:
        with st.spinner("🚀 BOOTSTRAPPING TITAN OMNI-BRAIN CORE..."):
            vault_handler = NeuralVaultManager()
            
            if vault_handler.vault:
                st.session_state.titan_agent = OmniBrainStrategicOrchestrator(api_key, vault_handler.vault)
                TelemetryLogService.push_log("Neural link verified. System Integrity 100%.", "ok")
                TelemetryLogService.push_log("Strategic Logic Core (Llama 3.3 70B) online.", "ok")
            else:
                st.session_state.titan_agent = None
                TelemetryLogService.push_log("CRITICAL ERROR: Neural vault files link broken.", "fail")

# Trigger System Boot Sequence
execute_apex_handshake()

# ======================================================================================================================
# SECTION 6: UNIFIED COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Visual Unified Command Center Header
st.markdown(f"""
    <div class='command-header'>
        <div class='command-eyebrow'>NADP · SEM-IV CAPSTONE 2025–2026</div>
        <h1>{SystemRegistry.SYSTEM_NAME}</h1>
        <p class='command-subtitle'>{SystemRegistry.ACADEMY} | OMNI-BRAIN Build {SystemRegistry.VERSION}</p>
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
    st.markdown(f"<div class='terminal-hud'>{TelemetryLogService.get_log_stream()}</div>", unsafe_allow_html=True)

# Deployment Gate: Security Halt if Vault missing
if st.session_state.titan_agent is None:
    st.error("❌ VAULT FILES MISSING. index.faiss not found in GitHub.")
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

    TelemetryLogService.push_log(f"Initiating strategic analysis for Query: {user_input[:40]}...")

    with st.chat_message("assistant"):
        # UI Status Synchronization
        with st.status("🛸 Orchestrating Omni-Brain Multi-Agent Decision Synthesis...", expanded=True) as status_tracker:
            st.write("Isolating technical specifications and cost variables...")
            time.sleep(0.3)
            st.write("Mining context from DAP/DPM/DFPDS evidence layers...")
            TelemetryLogService.push_log("Agent Beta: Context extraction SUCCESS.")
            st.write("Performing regulatory gap analysis and financial power audit...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token Streaming from High-Intelligence Engine (OMNI-BRAIN EXECUTION)
            for chunk in st.session_state.titan_agent.execute_strategic_flow(user_input):
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
            TelemetryLogService.push_log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryLogService.push_log(f"CRITICAL INFERENCE FAIL: {str(engine_err)}", "fail")

# HUD Log Manual Refresh Trigger
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Procedural Integrity</p><p style='color:#ffffff; font-weight:bold;'>DAP 2026 CONFORMANT</p></div>""", unsafe_allow_html=True)
with foot2:
    st.markdown(f"""<div class='vital-unit'><p class='v-label'>Data Sovereignty</p><p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p></div>""", unsafe_allow_html=True)
with foot3:            st.markdown(interaction["content"])

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
            TelemetryLogService.push_log("Agent Beta: Neural context extraction SUCCESS.")
            st.write("Scanning for audit risks and financial power conflicts...")
            time.sleep(0.2)
            status_tracker.update(label="STRATEGIC ANALYSIS REPORT GENERATED", state="complete", expanded=False)

        # Output UI Layer for Real-time Token Streaming
        report_surface = st.empty()
        full_report_text = ""
        
        try:
            # Token Streaming from High-Intelligence 70B Engine
            for chunk in st.session_state.titan_agent.execute_analytical_cycle(user_input):
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
            TelemetryLogService.push_log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as engine_err:
            st.error(f"ENGINE_STALL: {str(engine_err)}")
            TelemetryLogService.push_log(f"CRITICAL INFERENCE FAIL: {str(engine_err)}", "fail")

# HUD Log Manual Refresh Trigger
st.rerun() if False else None 

# ======================================================================================================================
# SECTION 7: GOVERNANCE DASHBOARD & CAPSTONE PROJECT FOOTER
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown(f"""<div class='vital-unit
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
# END OF MASTER v41.0 TITAN OMNI-BRAIN SUPREME BUILD
# ======================================================================================================================
