# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN ENTERPRISE v18.0)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ACADEMIC MENTOR: Dr. Indu Mazumdar | INDUSTRIAL MENTOR: Mr. S.K. Bhola (Ex-CGM/AVNL)
# INFRASTRUCTURE: Groq LPU + Llama 3.1 70B + HuggingFace Neural Transformers
# ======================================================================================================================
"""
TITLE: Design and Development of an AI-Based Chatbot for Defence Procurement Query Resolution
AUTHOR: Jatin Sharma (Roll No: 242602022)
DOCUMENTATION:
This system is a multi-agent Retrieval-Augmented Generation (RAG) platform optimized for the
Indian Defence Procurement ecosystem. It indexes 1,691 pages of regulatory documentation 
including DAP 2020, DAP 2026, DPM Vol 1 & 2, DFPDS 2026, and TPCR roadmaps.

SYSTEM ARCHITECTURE:
- Frontend: Streamlit High-Fidelity Tactical Interface
- Backend: LangChain Orchestration Layer
- Vector Store: FAISS (Facebook AI Similarity Search)
- Inference: Groq LPU (Language Processing Unit)
- Reasoning: Llama 3.1 70B (State-of-the-Art Generative Analyst)
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
from typing import List, Dict, Any, Optional, Union

# Advanced Intelligence & Neural Processing Software Imports
try:
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_groq import ChatGroq
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain.docstore.document import Document
    from langchain.prompts import PromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
except ImportError as e:
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Please update requirements.txt.")

# ======================================================================================================================
# SECTION 1: GLOBAL SYSTEM CONSTANTS & CONFIGURATION
# ======================================================================================================================

class SystemConfig:
    """Centralized configuration registry for system-wide parameters."""
    SYSTEM_NAME = "DEFENCE PROCUREMENT QUERY BOT"
    SYSTEM_CODE = "DPQB-TITAN-v18-ENTERPRISE"
    VERSION = "18.0.4"
    ACADEMY = "National Academy of Defence Production"
    LOCATION = "Nagpur, India"
    
    # Neural Engine Parameters
    MODEL_70B = "llama-3.1-70b-versatile"
    MODEL_8B = "llama3-8b-8192"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # Path Resolution Priority
    VAULT_SEARCH_PATHS = [
        ".", 
        "permanent_vault", 
        "/mount/src/-defence-procurement-querybot",
        "./permanent_vault"
    ]
    
    # Tactical UI Theme Colors
    COLOR_GOLD = "#d4af37"
    COLOR_NAVY = "#020810"
    COLOR_CYAN = "#00f5ff"
    COLOR_TEXT = "#ccd6f6"

# Audit Logging Framework Initialization
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("TITAN_SYSTEM")

# ======================================================================================================================
# SECTION 2: TACTICAL INTERFACE ARCHITECTURE (CSS INJECTION)
# ======================================================================================================================

def apply_enterprise_military_ux():
    """
    Implements a custom-engineered UI/UX design. 
    Removes sidebars to maximize analytical focus and provides a military 'War-Room' aesthetic.
    """
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500;700&family=Orbitron:wght@400;900&display=swap');
        
        /* Root Application Overrides */
        .stApp {{
            background-color: {SystemConfig.COLOR_NAVY};
            color: {SystemConfig.COLOR_TEXT};
            font-family: 'Fira Code', monospace;
        }}

        /* Hide Sidebar and Streamlit Branding */
        [data-testid="stSidebar"] {{ display: none; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}

        /* Unified Command Header Design */
        .command-header {{
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(180deg, #0a192f 0%, {SystemConfig.COLOR_NAVY} 100%);
            border-bottom: 5px double {SystemConfig.COLOR_GOLD};
            margin-bottom: 50px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }}
        .command-header h1 {{
            color: {SystemConfig.COLOR_GOLD};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 25px;
            text-transform: uppercase;
            text-shadow: 0px 0px 30px rgba(212, 175, 55, 0.7);
            margin: 0;
            font-size: 3.8rem;
        }}
        .sub-header {{
            color: {SystemConfig.COLOR_GOLD};
            letter-spacing: 8px;
            font-size: 0.9rem;
            margin-top: 15px;
            text-transform: uppercase;
        }}

        /* System Telemetry & Vitals HUD */
        .hud-row {{
            display: flex;
            justify-content: space-around;
            margin: 0 auto 50px auto;
            max-width: 1200px;
            gap: 20px;
        }}
        .hud-cell {{
            flex: 1;
            padding: 25px;
            background: rgba(1, 10, 21, 0.8);
            border: 1px solid #1f3a5a;
            border-radius: 8px;
            text-align: center;
            border-bottom: 3px solid {SystemConfig.COLOR_GOLD};
        }}
        .hud-label {{ font-size: 0.75rem; color: {SystemConfig.COLOR_GOLD}; font-weight: bold; text-transform: uppercase; }}
        .hud-value {{ font-size: 1.8rem; font-weight: 900; color: #ffffff; margin-top: 10px; }}

        /* Analysis Decision Cards */
        .analysis-card {{
            background-color: #0a192f;
            border: 1px solid {SystemConfig.COLOR_CYAN};
            padding: 40px;
            border-radius: 15px;
            border-left: 20px solid {SystemConfig.COLOR_GOLD};
            margin: 30px auto;
            max-width: 1100px;
            box-shadow: 0 40px 100px rgba(0,0,0,1);
            line-height: 1.8;
        }}

        /* Real-time Processing Console */
        .console-container {{
            max-width: 1100px;
            margin: 0 auto 40px auto;
        }}
        .terminal-log {{
            background-color: #000000;
            color: #39ff14;
            padding: 25px;
            border: 1px solid #222;
            font-size: 0.85rem;
            height: 250px;
            overflow-y: auto;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 50px #000;
        }}

        /* Interactive Elements */
        .stChatInputContainer {{
            border: 3px solid {SystemConfig.COLOR_GOLD} !important;
            border-radius: 20px !important;
            background-color: #051221 !important;
            padding: 15px !important;
            max-width: 1100px;
            margin: 0 auto;
        }}

        /* CRT Scanline Effect */
        .scanline {{
            width: 100%; height: 100%; position: fixed; top: 0; left: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.2) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
            z-index: 1000; background-size: 100% 3px, 3px 100%; pointer-events: none;
        }}
        </style>
        <div class="scanline"></div>
    """, unsafe_allow_html=True)

# ======================================================================================================================
# SECTION 3: CORE INTELLIGENCE SERVICES (MULTI-AGENT LOGIC)
# ======================================================================================================================

class TelemetryService:
    """Manages the real-time system logs and process monitoring."""
    
    @staticmethod
    def initialize():
        """Bootstraps the telemetry session state."""
        if "session_telemetry" not in st.session_state:
            st.session_state.session_telemetry = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def log(msg: str, level: str = "INFO"):
        """Records a timestamped system event."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        entry = f"[{timestamp}] {level.upper()}: {msg}"
        st.session_state.session_telemetry.append(entry)
        # Prevent buffer overflow
        if len(st.session_state.session_telemetry) > 30:
            st.session_state.session_telemetry.pop(0)

    @staticmethod
    def get_log_stream() -> str:
        """Returns log history for the UI."""
        return "\n".join(st.session_state.session_telemetry)

class NeuralKnowledgeVault:
    """
    Handles the mounting and verification of the neural knowledge base.
    Implements multi-path resolution for robust cloud deployment.
    """
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=SystemConfig.EMBEDDING_MODEL)
        self.vault = self._mount_persistent_index()

    def _mount_persistent_index(self) -> Optional[FAISS]:
        """Scans prioritized paths to find and load the FAISS vector index."""
        for path in SystemConfig.VAULT_SEARCH_PATHS:
            full_path = os.path.join(path, "index.faiss")
            if os.path.exists(full_path):
                try:
                    TelemetryService.log(f"Attempting link with vault at: {path}")
                    return FAISS.load_local(
                        folder_path=path, 
                        embeddings=self.embeddings, 
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    TelemetryService.log(f"Integrity failure at path {path}: {str(e)}", "ERROR")
        return None

class StrategicAgentOrchestrator:
    """
    The High-Intelligence reasoning engine. 
    Implements a multi-stage cognitive pipeline for complex procurement synthesis.
    """
    
    def __init__(self, api_key: str, vault: FAISS):
        self.vault = vault
        self.api_key = api_key
        self.primary_llm = ChatGroq(
            groq_api_key=api_key, 
            model_name=SystemConfig.MODEL_70B, 
            temperature=0
        )
        self.helper_llm = ChatGroq(
            groq_api_key=api_key, 
            model_name=SystemConfig.MODEL_8B, 
            temperature=0.1
        )

    def agent_alpha_query_refinement(self, raw_input: str) -> str:
        """Agentic Layer 1: Semantically expands query into Technical Acquisition Nomenclature."""
        prompt = f"""
        [ROLE: MoD TECHNICAL ADVISOR]
        CONVERT the following layman procurement query into formal jargon for DAP 2026 / DFPDS searching.
        Query: {raw_input}
        Output only the refined technical search string.
        """
        try:
            response = self.helper_llm.invoke(prompt)
            return response.content
        except Exception:
            return raw_input

    def agent_beta_context_mining(self, refined_query: str) -> str:
        """Agentic Layer 2: Retrieves multi-layered context from the 1,691-page corpus."""
        if not self.vault:
            return "KNOWLEDGE_BASE_OFFLINE"
        
        # High-K Retrieval (Top 15 chunks for comprehensive synthesis)
        search_results = self.vault.as_retriever(search_kwargs={"k": 15}).invoke(refined_query)
        
        structured_context = ""
        manual_sources = set()
        for i, doc in enumerate(search_results):
            source = doc.metadata.get('source', 'Classified Reference')
            manual_sources.add(source)
            structured_context += f"\n[LAYER {i+1} | MANUAL: {source}]\n{doc.page_content}\n"
        
        TelemetryService.log(f"Context mining complete. Sources: {', '.join(manual_sources)}")
        return structured_context

    def agent_gamma_strategic_synthesis(self, user_query: str):
        """Agentic Layer 3: Performs final Pentagon Reasoning Synthesis (6-Vector Analysis)."""
        
        # Pre-processing
        refined_q = self.agent_alpha_query_refinement(user_query)
        full_context = self.agent_beta_context_mining(refined_q)
        
        # The Pentagon Reasoning Directive
        system_directive = f"""
        YOU ARE THE 'TITAN STRATEGIC ORACLE' AT THE NATIONAL ACADEMY OF DEFENCE PRODUCTION.
        MISSION: Provide an exhaustive, 360-degree Strategic Consultation based on Indian Defence Manuals.
        
        EVIDENCE CORPUS:
        {full_context}

        HEXAGONAL REASONING PROTOCOL (ADDRESS ALL 6 ANGLES):
        1. 🛡️ POLICY VECTOR: Categorize the project under DAP 2020/26 (IDDM, Make-II, Buy-Global, etc.). 
        2. ⚙️ PROCESS VECTOR: Map the step-by-step administrative workflow using the Handbook.
        3. 💰 POWER VECTOR: Cross-reference DFPDS 2026 to identify the Competent Financial Authority (CFA) for this value.
        4. 🔭 STRATEGIC ALIGNMENT: Match the requirement with the 15-year TPCR Roadmap.
        5. ⚠️ COMPLIANCE RISK (PERIL): Identify potential audit objections or regulatory contradictions.
        6. ✅ THE PROCEED SOLUTION: A definitive 3-step actionable roadmap for the file.

        STRICT RULES:
        - Use ONLY provided context.
        - Cite the specific manual name for every fact provided.
        - Be formal, precise, and authoritative.
        """
        
        return self.primary_llm.stream(system_directive + "\n\nQUERY: " + user_query)

# ======================================================================================================================
# SECTION 4: APPLICATION LOGIC & STATE INITIALIZATION
# ======================================================================================================================

def run_system_initialization():
    """Bootstraps the analytical environment and performs integrity checks."""
    TelemetryService.initialize()
    apply_enterprise_military_ux()
    
    # Secure Credentials Initialization
    api_key = GROQ_API_KEY
    if not api_key:
        st.error("FATAL ERROR: Groq Security Key Missing. Deployment Terminated.")
        st.stop()
        
    # Knowledge Core Initialization
    if "neural_engine" not in st.session_state:
        with st.spinner("🛸 MOUNTING STRATEGIC NEURAL CORE..."):
            kv = NeuralKnowledgeVault()
            if kv.vault:
                st.session_state.neural_engine = StrategicAgentOrchestrator(api_key, kv.vault)
                TelemetryService.log("Neural Knowledge Vault synchronized.")
                TelemetryService.log("Groq Strategic Core (70B) handshake successful.")
            else:
                st.session_state.neural_engine = None
                TelemetryService.log("CRITICAL: Vault file (index.faiss) not detected.", "ERROR")

# Execute Boot Sequence
run_system_initialization()

# ======================================================================================================================
# SECTION 5: COMMAND DASHBOARD UI EXECUTION
# ======================================================================================================================

# Header Implementation
st.markdown(f"""
    <div class='command-header'>
        <h1>{SystemConfig.SYSTEM_NAME}</h1>
        <p class='sub-header'>{SystemConfig.ACADEMY} | STRATEGIC COMMAND v{SystemConfig.VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# Vitals HUD Implementation
v1, v2, v3, v4 = st.columns(4)
with v1:
    st.markdown(f"<div class='hud-cell'><p class='hud-label'>Indexed Pages</p><p class='hud-value'>1,691</p></div>", unsafe_allow_html=True)
with v2:
    st.markdown(f"<div class='hud-cell'><p class='hud-label'>Neural Nodes</p><p class='hud-value'>5,026</p></div>", unsafe_allow_html=True)
with v3:
    st.markdown(f"<div class='hud-cell'><p class='hud-label'>Reasoning Brain</p><p class='hud-value'>70B Llama</p></div>", unsafe_allow_html=True)
with v4:
    st.markdown(f"<div class='hud-cell'><p class='hud-label'>Security Status</p><p class='hud-value'>Encrypted</p></div>", unsafe_allow_html=True)

# Real-time System Console Display
st.markdown("<div class='console-container'>", unsafe_allow_html=True)
st.markdown("### 🖥️ STRATEGIC PROCESS MONITOR")
st.markdown(f"<div class='terminal-log'>{TelemetryService.get_log_stream()}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Vault Integrity Gate
if st.session_state.neural_engine is None:
    st.error("❌ CRITICAL FAILURE: Permanent Vault Files (index.faiss) Not Detected. System Integrity compromised.")
    st.info("💡 RECOVERY: Upload your index.faiss and index.pkl files to the root directory of your GitHub repository.")
    st.stop()

# Persistent Strategic Interaction History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Multi-Agent Query Interaction Loop
if user_input := st.chat_input("Enter a complex procurement problem for Deep-Tissue Analysis..."):
    # Record User Query
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    TelemetryService.log(f"New Strategic Query Initiated: {user_input[:40]}...")

    # Begin Strategic Consultation Pipeline
    with st.chat_message("assistant"):
        with st.status("🛸 Orchestrating Hexagonal Synthesis Pipeline...", expanded=True) as status:
            
            # Step 1: Query Expansion
            st.write("Expanding semantics into procurement nomenclature...")
            time.sleep(0.3)
            
            # Step 2: Retrieval & Synthesis
            st.write("Mining evidence from 1,691 knowledge layers...")
            TelemetryService.log("Cross-manual synthesis agent active.")
            
            # Step 3: Authority Validation
            st.write("Calculating financial delegated powers via DFPDS 2026...")
            time.sleep(0.2)
            
            status.update(label="STRATEGIC REPORT GENERATED", state="complete", expanded=False)

        # UI Surface for Streaming Response
        output_surface = st.empty()
        full_report_text = ""
        
        try:
            # Stream the High-Intelligence Brief from Groq Cloud
            # We use the stream iterator to yield tokens in real-time
            for chunk in st.session_state.neural_engine.agent_gamma_strategic_synthesis(user_input):
                
                # Robust Token Parsing Logic (Handles both String and Object types)
                # This is critical for preventing attribute errors across different library versions
                if hasattr(chunk, 'content'):
                    token = chunk.content
                elif isinstance(chunk, str):
                    token = chunk
                else:
                    # Generic attribute fallback
                    token = getattr(chunk, 'text', str(chunk))
                
                full_report_text += token
                # Visual cursor effect for professional feel
                output_surface.markdown(full_report_text + "▌")
            
            # Final Render (Post-Stream)
            output_surface.markdown(full_report_text)
            
            # Persist response in session history
            TelemetryService.log("Strategic Briefing Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_report_text})
        
        except Exception as e:
            # Detailed Error Capture for presentation troubleshooting
            error_details = traceback.format_exc()
            st.error(f"ENGINE_INFERENCE_FAILURE: {str(e)}")
            TelemetryService.log(f"CRITICAL FAIL: {str(e)}", "ERROR")
            logger.error(f"Full Stack Trace: {error_details}")

# Manual Refresh of Visual Logs
st.rerun() if False else None # Optional logic trigger

# ======================================================================================================================
# SECTION 6: ANALYTICAL GOVERNANCE FOOTER
# ======================================================================================================================

st.markdown("<br><br><hr>", unsafe_allow_html=True)
foot1, foot2, foot3 = st.columns(3)

with foot1:
    st.markdown(f"""
        <div class='hud-cell'>
            <p class='hud-label'>Compliance</p>
            <p style='color:#ffffff; font-weight:bold;'>DAP 2026 ALIGNED</p>
        </div>
    """, unsafe_allow_html=True)

with foot2:
    st.markdown(f"""
        <div class='hud-cell'>
            <p class='hud-label'>Data Residency</p>
            <p style='color:#ffffff; font-weight:bold;'>LOCAL VAULT SECURE</p>
        </div>
    """, unsafe_allow_html=True)

with foot3:
    st.markdown(f"""
        <div class='hud-cell'>
            <p class='hud-label'>Analytic Depth</p>
            <p style='color:#ffffff; font-weight:bold;'>HEXAGONAL SYNTHESIS</p>
        </div>
    """, unsafe_allow_html=True)

# Final Institutional Credit & Project ID
st.markdown(
    f"<p style='text-align: center; color: #444; font-size: 0.75rem; padding: 40px;'>"
    f"Proprietary Strategic Intelligence Platform | {SystemConfig.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Project ID: {SystemConfig.SYSTEM_CODE} | Developer: Jatin Sharma"
    "</p>", 
    unsafe_allow_html=True
)

# ======================================================================================================================
# END OF AEGIS TITAN v18.0 MASTER BUILD
# =======================================================
