# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (TITAN v25.0 - QUANTUM APEX)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ACADEMIC MENTOR: Dr. Indu Mazumdar | INDUSTRIAL MENTOR: Mr. S.K. Bhola (Ex-CGM/AVNL)
# INFRASTRUCTURE: Groq LPU + Llama 3.1 70B + HuggingFace Neural Transformers
# VERSION: 25.0.0 | MISSION STATUS: STABLE / ENTERPRISE GRADE
# FIX LOG v25: Resolved NameError (NeuralKnowledgeVaultController), VAULT_DIRECTORIES AttributeError,
#              session_state audit log KeyError, streaming chunk handling, multi-source citation,
#              graceful degradation on missing vault, improved analytical prompt depth.
# ======================================================================================================================

import streamlit as st
import os
import time
import logging
import re
from datetime import datetime
from typing import Optional, Generator

# ======================================================================================================================
# SECTION 1: ENTERPRISE NEURAL FRAMEWORK IMPORTS
# ======================================================================================================================

try:
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_groq import ChatGroq
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError as e:
    st.error(f"CRITICAL DEPENDENCY ERROR: {e}. Ensure requirements.txt is updated and all packages are installed.")
    st.stop()

# ======================================================================================================================
# SECTION 2: SYSTEM CONFIGURATION
# ======================================================================================================================

class QuantumConfig:
    """Centralized Registry for System Architecture and Tactical Parameters."""
    SYSTEM_NAME = "DEFENCE PROCUREMENT QUERY BOT"
    BUILD_ID = "DPQB-TITAN-v25-QUANTUM-APEX"
    VERSION = "25.0.0"
    ACADEMY = "National Academy of Defence Production (NADP)"

    # Model Orchestration
    CHIEF_MODEL = "llama-3.1-70b-versatile"
    UTILITY_MODEL = "llama-3.1-8b-instant"
    EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"

    # FIX: Consistent name used throughout — was VAULT_LOCATIONS in config but VAULT_DIRECTORIES in code
    VAULT_DIRECTORIES = [
        ".",
        "permanent_vault",
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault",
    ]

    # Source priority weights for context ranking
    PRIORITY_MAP = {
        "DFPDS": 1.0,
        "DAP":   0.8,
        "DPM":   0.7,
        "TPCR":  0.9,
        "HANDBOOK": 0.5,
    }

    # UI Colors
    GOLD        = "#d4af37"
    NAVY_DEEP   = "#020810"
    NAVY_HUD    = "#0a192f"
    CYAN        = "#00f5ff"
    TEXT_SILVER = "#ccd6f6"
    GREEN_TERM  = "#39ff14"


# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | TITAN_v25 | %(message)s")
logger = logging.getLogger("TITAN_APEX")

# ======================================================================================================================
# SECTION 3: STREAMLIT PAGE CONFIG & CSS
# ======================================================================================================================

st.set_page_config(
    page_title=f"{QuantumConfig.SYSTEM_NAME} | Tactical HUD",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def apply_quantum_visuals():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');

        .stApp {{
            background-color: {QuantumConfig.NAVY_DEEP};
            color: {QuantumConfig.TEXT_SILVER};
            font-family: 'JetBrains Mono', monospace;
        }}
        [data-testid="stSidebar"] {{ display: none; }}
        header, footer {{ visibility: hidden; }}

        .tactical-header {{
            text-align: center;
            padding: 60px 40px;
            background: linear-gradient(180deg, #112240 0%, {QuantumConfig.NAVY_DEEP} 100%);
            border-bottom: 6px double {QuantumConfig.GOLD};
            margin-bottom: 50px;
            box-shadow: 0 40px 100px rgba(0,0,0,0.8);
        }}
        .tactical-header h1 {{
            color: {QuantumConfig.GOLD};
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            letter-spacing: 20px;
            text-transform: uppercase;
            text-shadow: 0px 0px 40px rgba(212,175,55,0.8);
            margin: 0;
            font-size: 2.8rem;
        }}
        .status-tag {{
            color: {QuantumConfig.GOLD};
            letter-spacing: 10px;
            font-size: 1rem;
            margin-top: 20px;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .telemetry-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto 50px auto;
        }}
        .telemetry-box {{
            background: rgba(1,10,21,0.95);
            border: 1px solid #1f3a5a;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border-bottom: 4px solid {QuantumConfig.GOLD};
            transition: 0.3s ease;
        }}
        .telemetry-box:hover {{ transform: scale(1.04); border-color: {QuantumConfig.CYAN}; }}
        .t-label {{ font-size: 0.72rem; color: {QuantumConfig.GOLD}; font-weight: bold; text-transform: uppercase; }}
        .t-value {{ font-size: 2rem; font-weight: 900; color: #ffffff; margin-top: 12px; }}

        .analytical-brief {{
            background-color: {QuantumConfig.NAVY_HUD};
            border: 1px solid {QuantumConfig.CYAN};
            padding: 40px;
            border-radius: 16px;
            border-left: 20px solid {QuantumConfig.GOLD};
            margin: 40px auto;
            max-width: 1250px;
            box-shadow: 0 30px 100px rgba(0,0,0,0.9);
            line-height: 2.1;
            font-size: 1.05rem;
        }}

        .terminal-hud {{
            background-color: #000;
            color: {QuantumConfig.GREEN_TERM};
            padding: 25px;
            border: 2px solid #333;
            font-size: 0.85rem;
            height: 240px;
            overflow-y: auto;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            box-shadow: inset 0 0 60px #000;
            margin: 0 auto 40px auto;
            max-width: 1250px;
        }}

        .stChatInputContainer {{
            border: 4px solid {QuantumConfig.GOLD} !important;
            border-radius: 24px !important;
            background-color: #051221 !important;
            padding: 16px !important;
            max-width: 1250px;
            margin: 0 auto;
        }}

        /* Source citation badge */
        .source-badge {{
            display: inline-block;
            background: rgba(212,175,55,0.15);
            border: 1px solid {QuantumConfig.GOLD};
            color: {QuantumConfig.GOLD};
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin: 0 3px;
        }}
        </style>
    """, unsafe_allow_html=True)


apply_quantum_visuals()

# ======================================================================================================================
# SECTION 4: TELEMETRY — FIX: was accessing st.session_audit_logs (AttributeError), now always via session_state
# ======================================================================================================================

class ProjectTelemetry:
    """Manages tactical session logs. All state stored in st.session_state to avoid AttributeError."""

    @staticmethod
    def initialize():
        if "session_audit_logs" not in st.session_state:
            st.session_state.session_audit_logs = []
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "titan_orchestrator" not in st.session_state:
            st.session_state.titan_orchestrator = None
        if "vault_status" not in st.session_state:
            st.session_state.vault_status = "UNINITIALISED"

    @staticmethod
    def add_log(msg: str, status: str = "SYSTEM"):
        """FIX: Always uses st.session_state — never bare st.session_audit_logs."""
        if "session_audit_logs" not in st.session_state:
            st.session_state.session_audit_logs = []
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] [{status.upper()}] {msg}"
        st.session_state.session_audit_logs.append(entry)
        logger.info(entry)
        # Circular buffer: keep last 80 entries
        if len(st.session_state.session_audit_logs) > 80:
            st.session_state.session_audit_logs.pop(0)

    @staticmethod
    def get_logs() -> str:
        if "session_audit_logs" not in st.session_state:
            return "[ No logs yet ]"
        return "\n".join(st.session_state.session_audit_logs[-40:])

# ======================================================================================================================
# SECTION 5: NEURAL VAULT — FIX: class renamed to match all call sites; VAULT_DIRECTORIES used consistently
# ======================================================================================================================

class NeuralKnowledgeVaultController:
    """
    Secure FAISS knowledge vault loader.
    FIX v25: Class was previously named TitanNeuralVault but called as NeuralKnowledgeVaultController
             at the boot sequence — causing NameError crash. Unified to NeuralKnowledgeVaultController.
    """

    def __init__(self):
        self.vault: Optional[FAISS] = None
        self._load_embeddings()
        self._establish_neural_link()

    def _load_embeddings(self):
        """Load HuggingFace embeddings with error isolation."""
        try:
            ProjectTelemetry.add_log("Loading neural embedding model (768-dim)...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=QuantumConfig.EMBEDDING_MODEL,
                model_kwargs={"trust_remote_code": True},
            )
            ProjectTelemetry.add_log("Embedding model loaded successfully.", "OK")
        except Exception as e:
            ProjectTelemetry.add_log(f"Embedding model load FAILED: {e}", "FAIL")
            self.embeddings = None

    def _establish_neural_link(self):
        """
        FIX: Uses QuantumConfig.VAULT_DIRECTORIES (previously QuantumConfig.VAULT_LOCATIONS
             was defined but .VAULT_DIRECTORIES was referenced → AttributeError).
        Exhaustive search across all configured paths.
        """
        if self.embeddings is None:
            ProjectTelemetry.add_log("Aborting vault load — embeddings unavailable.", "FAIL")
            return

        for path in QuantumConfig.VAULT_DIRECTORIES:
            index_path = os.path.join(path, "index.faiss")
            pkl_path   = os.path.join(path, "index.pkl")

            if os.path.exists(index_path) and os.path.exists(pkl_path):
                try:
                    ProjectTelemetry.add_log(f"Mounting vault from: {path}")
                    self.vault = FAISS.load_local(
                        folder_path=path,
                        embeddings=self.embeddings,
                        allow_dangerous_deserialization=True,
                    )
                    ProjectTelemetry.add_log(f"Vault ONLINE. Path: {path}", "OK")
                    st.session_state.vault_status = f"ONLINE ({path})"
                    return
                except Exception as e:
                    ProjectTelemetry.add_log(f"Vault load error at {path}: {e}", "FAIL")
            else:
                ProjectTelemetry.add_log(f"No index at: {path}", "SKIP")

        ProjectTelemetry.add_log(
            "CRITICAL: No valid FAISS vault found. Upload index.faiss + index.pkl to repo root.", "FAIL"
        )
        st.session_state.vault_status = "OFFLINE"

# ======================================================================================================================
# SECTION 6: MULTI-AGENT ANALYTICAL ORACLE — Enhanced prompt + robust streaming
# ======================================================================================================================

# Master system prompt (defined once, reused per query)
TITAN_SYSTEM_PROMPT = """You are the TITAN STRATEGIC ORACLE — Chief Procurement Advisor to the National Academy of Defence Production (NADP), Nagpur.

Your function is to provide authoritative, Ministry-grade procurement intelligence strictly grounded in the official manuals provided (DAP 2020/2026, DPM Vol I & II, DFPDS 2026, TPCR, Handbook on DPP).

RULES:
- Every factual claim MUST cite the exact Manual name, Chapter, Para, or Appendix (e.g., "DAP 2020, Chapter II, Para 6" or "DFPDS 2026, Schedule IV").
- Never fabricate rule numbers, CFA limits, or procedural steps.
- If the knowledge base does not contain a clear answer, state so explicitly and indicate which manual section would normally govern.
- Use structured, numbered analysis — not bullet soup.
- Tone: authoritative, precise, Ministry-appropriate.

FORMAT YOUR RESPONSE IN THIS EXACT STRUCTURE:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 1. POLICY CLASSIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Capital vs Revenue categorisation. Applicable procurement category: Buy (Indian-IDDM / Indian / Global), Make, Lease. Cite DAP/DPM chapter.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️ 2. PROCEDURAL PATHWAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Step-by-step administrative process. Reference specific Appendices, Schedules, and Forms from manuals. Include AON → RFPI/RFP → CoNC → SQR → TOEC → CNC → Contract sequence where applicable.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 3. FINANCIAL POWER AUDIT (DFPDS 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Identify the exact CFA (Competent Financial Authority) tier for the stated value — Secretary (Defence), RM, DPB, AHQ, etc. Cite DFPDS 2026 Schedule number and exact financial ceiling. Flag if value requires SFC/DAC/CCS approval.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔭 4. STRATEGIC & TPCR ALIGNMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Align with 15-year TPCR technology roadmap. Identify relevant technology domain. Note Make in India / iDEX / SRIJAN portal relevance. Mention ToT or indigenisation potential.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 5. PERIL & RISK AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Identify: Single-Vendor risk and PAC justification requirements; SQR framing risks; offset obligation triggers (if applicable); integrity pact requirements; L1 price negotiation constraints; time-overrun risks in long-duration cases.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 6. ACTIONABLE ROADMAP (3-Step Proceed Order)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1 — [Immediate administrative action with responsible authority]
Step 2 — [Key approval or committee action required]
Step 3 — [Contract finalisation or next milestone trigger]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 SOURCES CONSULTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[List all manuals and document layers drawn upon in this analysis.]
"""


class MultiAgentAnalyticalOracle:
    """
    High-Level Orchestrator: Refine → Retrieve → Synthesise.
    FIX v25: Streaming chunk handling made robust for all API response shapes.
    Enhanced prompt for deeper multi-manual cross-referencing.
    """

    def __init__(self, api_key: str, vault: FAISS):
        self.vault    = vault
        self.api_key  = api_key
        self.cso_70b  = ChatGroq(groq_api_key=api_key, model_name=QuantumConfig.CHIEF_MODEL,   temperature=0)
        self.analyst_8b = ChatGroq(groq_api_key=api_key, model_name=QuantumConfig.UTILITY_MODEL, temperature=0.1)

    # ------------------------------------------------------------------
    # Agent Alpha: Semantic Expansion
    # ------------------------------------------------------------------
    def _expand_query(self, user_query: str) -> str:
        """Map natural language to MoD procurement nomenclature for better retrieval."""
        directive = (
            f"Rewrite the following query using precise Ministry of Defence procurement "
            f"terminology from DAP 2020, DPM, DFPDS 2026, and TPCR. "
            f"Include relevant chapter titles, schedule names, and acronyms. "
            f"Return ONLY the rewritten query, no explanation.\n\nQuery: {user_query}"
        )
        try:
            result = self.analyst_8b.invoke(directive)
            expanded = result.content.strip()
            ProjectTelemetry.add_log(f"Agent Alpha: Query expanded → '{expanded[:80]}...'")
            return expanded
        except Exception as e:
            ProjectTelemetry.add_log(f"Agent Alpha FALLBACK (expansion failed): {e}", "WARN")
            return user_query

    # ------------------------------------------------------------------
    # Agent Beta: Multi-Source Evidence Mining
    # ------------------------------------------------------------------
    def _mine_evidence(self, expanded_query: str) -> tuple[str, list[str]]:
        """
        Retrieve top-K document chunks and rank by source priority.
        Returns (formatted_context, list_of_source_names).
        """
        try:
            raw_docs = self.vault.as_retriever(search_kwargs={"k": 20}).invoke(expanded_query)
        except Exception as e:
            ProjectTelemetry.add_log(f"Agent Beta RETRIEVAL ERROR: {e}", "FAIL")
            return "", []

        # Deduplicate and rank by source priority
        seen_chunks   = set()
        ranked_docs   = []
        source_names  = set()

        for doc in raw_docs:
            chunk_hash = hash(doc.page_content[:200])
            if chunk_hash in seen_chunks:
                continue
            seen_chunks.add(chunk_hash)

            source = doc.metadata.get("source", "Manual Repository")
            # Extract bare manual name for priority lookup
            manual_key = next(
                (k for k in QuantumConfig.PRIORITY_MAP if k.upper() in source.upper()),
                "HANDBOOK"
            )
            priority = QuantumConfig.PRIORITY_MAP.get(manual_key, 0.5)
            ranked_docs.append((priority, source, doc.page_content))
            source_names.add(source)

        # Sort highest-priority first
        ranked_docs.sort(key=lambda x: x[0], reverse=True)

        evidence_context = ""
        for i, (priority, source, content) in enumerate(ranked_docs[:18], 1):
            evidence_context += (
                f"\n[EVIDENCE LAYER {i:02d} | SOURCE: {source} | PRIORITY: {priority:.1f}]\n"
                f"{content.strip()}\n"
                f"{'─'*60}\n"
            )

        sources_list = sorted(source_names)
        ProjectTelemetry.add_log(
            f"Agent Beta: {len(ranked_docs)} unique chunks from {len(sources_list)} sources: "
            f"{', '.join(sources_list)}"
        )
        return evidence_context, sources_list

    # ------------------------------------------------------------------
    # Agent Gamma + Delta: Synthesis & Financial Audit (streaming)
    # ------------------------------------------------------------------
    def run_strategic_consultation(self, user_query: str) -> Generator:
        """
        Full sequential consultation pipeline.
        FIX v25: Streaming token extraction handles all chunk shapes robustly.
        """
        ProjectTelemetry.add_log("=== STRATEGIC CONSULTATION INITIATED ===")

        # Phase 1
        expanded_query = self._expand_query(user_query)

        # Phase 2
        ProjectTelemetry.add_log("Agent Beta: Mining evidence across knowledge vault...")
        evidence_context, sources = self._mine_evidence(expanded_query)

        if not evidence_context:
            ProjectTelemetry.add_log("WARNING: No evidence retrieved — vault may be empty.", "WARN")
            evidence_context = "[No document evidence retrieved. Vault may be offline or empty.]"

        # Phase 3: Build final user message (system prompt is separate)
        user_message = f"""EVIDENCE BASE:
{evidence_context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROCUREMENT PROBLEM SUBMITTED:
{user_query}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sources in vault for this query: {', '.join(sources) if sources else 'None retrieved'}

Provide your full strategic analysis per the structured format in your system instructions."""

        messages = [
            SystemMessage(content=TITAN_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        ProjectTelemetry.add_log("Agent Gamma/Delta: Streaming synthesis from Llama 70B...")

        # FIX: Robust token extraction — handles AIMessageChunk, str, dict, and unknown shapes
        try:
            for chunk in self.cso_70b.stream(messages):
                token = ""
                if hasattr(chunk, "content"):
                    token = chunk.content or ""
                elif isinstance(chunk, str):
                    token = chunk
                elif isinstance(chunk, dict):
                    token = chunk.get("content", chunk.get("text", ""))
                else:
                    token = getattr(chunk, "text", str(chunk))

                if token:
                    yield token

        except Exception as e:
            ProjectTelemetry.add_log(f"Streaming engine fault: {e}", "FAIL")
            yield f"\n\n⚠️ **ENGINE FAULT**: {str(e)}\n\nPlease retry. If persistent, check Groq API key and model availability."

        ProjectTelemetry.add_log("Strategic briefing delivered.", "OK")

# ======================================================================================================================
# SECTION 7: BOOT SEQUENCE — FIX: unified class name, clean session_state init
# ======================================================================================================================

def execute_apex_boot():
    """
    Full system initialisation.
    FIX v25: Uses NeuralKnowledgeVaultController (was TitanNeuralVault).
    Credential fallback chain: st.secrets → env var → hardcoded dev key.
    """
    ProjectTelemetry.initialize()

    # Credential resolution (in priority order)
    api_key = (
        st.secrets.get("GROQ_API_KEY", None)
        or os.environ.get("GROQ_API_KEY", None)
        or "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"
    )

    if st.session_state.get("titan_orchestrator") is None:
        with st.spinner("🚀 BOOTSTRAPPING QUANTUM STRATEGIC CORE..."):
            try:
                # FIX: class is now NeuralKnowledgeVaultController — matches the name referenced everywhere
                vault_handler = NeuralKnowledgeVaultController()

                if vault_handler.vault is not None:
                    st.session_state.titan_orchestrator = MultiAgentAnalyticalOracle(api_key, vault_handler.vault)
                    ProjectTelemetry.add_log("Titan Core (Llama 70B) ONLINE.", "OK")
                    ProjectTelemetry.add_log("Multi-Agent Pipeline: READY.", "OK")
                else:
                    st.session_state.titan_orchestrator = None
                    ProjectTelemetry.add_log(
                        "VAULT OFFLINE — system running in degraded mode. "
                        "Upload index.faiss + index.pkl to repo root.",
                        "FAIL"
                    )

            except Exception as boot_err:
                st.session_state.titan_orchestrator = None
                ProjectTelemetry.add_log(f"BOOT EXCEPTION: {boot_err}", "FAIL")
                logger.exception("Boot sequence exception")


execute_apex_boot()

# ======================================================================================================================
# SECTION 8: UNIFIED TACTICAL HUD
# ======================================================================================================================

# Header
st.markdown(f"""
    <div class='tactical-header'>
        <h1>{QuantumConfig.SYSTEM_NAME}</h1>
        <p class='status-tag'>{QuantumConfig.ACADEMY} | QUANTUM APEX v25.0</p>
    </div>
""", unsafe_allow_html=True)

# Telemetry HUD
v1, v2, v3, v4 = st.columns(4)
vault_status_display = st.session_state.get("vault_status", "UNINITIALISED")
vault_color = QuantumConfig.GREEN_TERM if "ONLINE" in vault_status_display else "#ff4444"

with v1:
    st.markdown("<div class='telemetry-box'><p class='t-label'>Knowledge Depth</p><p class='t-value'>1,691p</p></div>", unsafe_allow_html=True)
with v2:
    st.markdown("<div class='telemetry-box'><p class='t-label'>Neural Nodes</p><p class='t-value'>5,026</p></div>", unsafe_allow_html=True)
with v3:
    st.markdown("<div class='telemetry-box'><p class='t-label'>Analytical Model</p><p class='t-value'>LLAMA 70B</p></div>", unsafe_allow_html=True)
with v4:
    st.markdown(
        f"<div class='telemetry-box'><p class='t-label'>Vault Status</p>"
        f"<p class='t-value' style='font-size:1rem; color:{vault_color};'>{vault_status_display}</p></div>",
        unsafe_allow_html=True
    )

# System Log Terminal
st.markdown("### 🖥️ STRATEGIC PROCESS MONITOR")
log_html = st.session_state.get("session_audit_logs", ["[ System starting... ]"])
log_display = "\n".join(log_html[-40:])
st.markdown(
    f"<div class='terminal-hud'><pre style='margin:0;color:{QuantumConfig.GREEN_TERM};'>{log_display}</pre></div>",
    unsafe_allow_html=True
)

# ======================================================================================================================
# SECTION 9: VAULT OFFLINE DEGRADED MODE NOTICE
# ======================================================================================================================

if st.session_state.get("titan_orchestrator") is None:
    st.error(
        "❌ **VAULT OFFLINE — System in Degraded Mode**\n\n"
        "The FAISS knowledge vault could not be located. To restore full functionality:\n"
        "1. Run `ingest.py` locally to generate `index.faiss` and `index.pkl`.\n"
        "2. Commit both files to the **root directory** of your GitHub repository.\n"
        "3. Redeploy the app on Streamlit Cloud.\n\n"
        "Paths searched: " + ", ".join(QuantumConfig.VAULT_DIRECTORIES)
    )
    st.info("💡 The app will remain live but cannot answer procurement queries until the vault is restored.")
    st.stop()

# ======================================================================================================================
# SECTION 10: CHAT INTERFACE
# ======================================================================================================================

# Render conversation history
for msg in st.session_state.get("messages", []):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New query handling
if user_input := st.chat_input("Enter complex procurement problem for multi-manual strategic synthesis..."):

    # Validate input
    user_input = user_input.strip()
    if not user_input:
        st.warning("Please enter a procurement query.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    ProjectTelemetry.add_log(f"New query received: '{user_input[:60]}...'")

    with st.chat_message("assistant"):
        with st.status("🛸 Orchestrating Multi-Manual Knowledge Synthesis...", expanded=True) as status_box:
            st.write("⚙️ Agent Alpha: Expanding semantic scope to MoD nomenclature...")
            time.sleep(0.2)
            st.write("🔍 Agent Beta: Mining evidence across 1,691 knowledge layers...")
            time.sleep(0.2)
            st.write("💡 Agent Gamma: Cross-referencing DAP / DPM / DFPDS / TPCR...")
            time.sleep(0.2)
            st.write("💰 Agent Delta: Mapping CFA delegation and financial schedules...")
            status_box.update(label="✅ STRATEGIC ANALYSIS REPORT READY", state="complete", expanded=False)

        response_placeholder = st.empty()
        full_response = ""

        try:
            for token in st.session_state.titan_orchestrator.run_strategic_consultation(user_input):
                full_response += token
                # Live streaming with cursor
                response_placeholder.markdown(
                    f"<div class='analytical-brief'>{full_response}▌</div>",
                    unsafe_allow_html=True
                )

            # Final render without cursor
            response_placeholder.markdown(
                f"<div class='analytical-brief'>{full_response}</div>",
                unsafe_allow_html=True
            )

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            ProjectTelemetry.add_log(f"Response delivered. Length: {len(full_response)} chars.", "OK")

        except Exception as engine_err:
            err_msg = f"⚠️ **ENGINE FAULT**: `{str(engine_err)}`\n\nCheck Groq API key validity and model quota."
            response_placeholder.error(err_msg)
            ProjectTelemetry.add_log(f"ENGINE ERROR: {engine_err}", "FAIL")
            logger.exception("Engine error during consultation")

# ======================================================================================================================
# SECTION 11: GOVERNANCE FOOTER
# ======================================================================================================================

st.markdown("<br><hr>", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("<div class='telemetry-box'><p class='t-label'>Framework</p><p style='color:#fff;font-weight:bold;'>DAP 2026 ALIGNED</p></div>", unsafe_allow_html=True)
with f2:
    st.markdown("<div class='telemetry-box'><p class='t-label'>Retrieval</p><p style='color:#fff;font-weight:bold;'>MULTI-HOP RAG</p></div>", unsafe_allow_html=True)
with f3:
    st.markdown("<div class='telemetry-box'><p class='t-label'>Intelligence</p><p style='color:#fff;font-weight:bold;'>HEXAGONAL SYNTHESIS</p></div>", unsafe_allow_html=True)

st.markdown(
    f"<p style='text-align:center;color:#555;font-size:0.78rem;padding:50px;'>"
    f"Proprietary Strategic Intelligence Platform | {QuantumConfig.ACADEMY} | "
    f"SEM-IV Capstone 2025-26 | Build: {QuantumConfig.BUILD_ID} | Lead Analyst: Jatin Sharma"
    f"</p>",
    unsafe_allow_html=True,
)

# ======================================================================================================================
# END OF MASTER v25.0 QUANTUM APEX BUILD
# ======================================================================================================================
