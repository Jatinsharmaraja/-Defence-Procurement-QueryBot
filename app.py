# ======================================================================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# MENTORS: Dr. Indu Mazumdar (Internal) | Mr. S.K. Bhola, Ex-CGM/AVNL (Industrial)
# AUTHOR: Jatin Sharma (Roll No: 242602022)
# MODEL: Groq LPU + Llama 3.3 70B + HuggingFace Embeddings
# VERSION: 47.0.1
# ======================================================================================================================

import streamlit as st
import os
import time
import logging
from datetime import datetime
from typing import Optional, Generator

# ======================================================================================================================
# SECTION 1: DEPENDENCY IMPORTS
# ======================================================================================================================

try:
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_groq import ChatGroq
    from langchain_core.documents import Document
except ImportError as e:
    st.error(f"Missing dependency: {e}")
    st.stop()

# ======================================================================================================================
# SECTION 2: SYSTEM CONFIGURATION
# ======================================================================================================================

class Config:
    SYSTEM_NAME    = "Defence Procurement Query Bot"
    VERSION        = "v47.0.1"
    ACADEMY        = "National Academy of Defence Production (NADP), Nagpur"
    DEVELOPER      = "Jatin Sharma · Roll No. 242602022"
    CAPSTONE       = "SEM-IV Capstone 2025–2026"
    BUILD_ID       = "DPQB-TITAN-v47"

    CHIEF_MODEL    = "llama-3.3-70b-versatile"
    UTILITY_MODEL  = "llama-3.1-8b-instant"
    EMBED_MODEL    = "nomic-ai/nomic-embed-text-v1.5"

    API_KEY        = "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"

    VAULT_PATHS    = [
        ".",
        "permanent_vault",
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault"
    ]

    MINING_DEPTH   = 30
    TEMPERATURE    = 0.0

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("DPQB")

# ======================================================================================================================
# SECTION 3: UI CONFIGURATION & STYLING
# ======================================================================================================================

st.set_page_config(
    page_title="Defence Procurement Query Bot | NADP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Reset & Base ── */
        .stApp {
            background-color: #0d0f14;
            color: #e2e8f0;
            font-family: 'Inter', system-ui, sans-serif;
        }

        /* Hide Streamlit chrome */
        [data-testid="stSidebar"],
        [data-testid="stToolbar"],
        header, footer { display: none !important; }

        /* ── Page wrapper ── */
        .main .block-container {
            padding: 2rem 3rem 4rem 3rem;
            max-width: 1100px;
        }

        /* ── Header ── */
        .page-header {
            display: flex;
            align-items: center;
            gap: 1.25rem;
            padding: 2rem 0 1.5rem 0;
            border-bottom: 1px solid #1e2330;
            margin-bottom: 2rem;
        }
        .header-icon {
            width: 44px; height: 44px;
            background: linear-gradient(135deg, #1a4fa3 0%, #2563eb 100%);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; flex-shrink: 0;
        }
        .header-text h1 {
            font-size: 1.25rem; font-weight: 700;
            color: #f1f5f9; margin: 0; letter-spacing: -0.01em;
        }
        .header-text p {
            font-size: 0.8rem; color: #64748b;
            margin: 2px 0 0 0; font-family: 'JetBrains Mono', monospace;
        }
        .header-badge {
            margin-left: auto;
            background: #1e2330;
            border: 1px solid #2a3347;
            padding: 4px 12px; border-radius: 20px;
            font-size: 0.72rem; color: #4ade80;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.05em;
        }

        /* ── Stat strip ── */
        .stat-strip {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: #111520;
            border: 1px solid #1e2330;
            border-radius: 10px;
            padding: 1rem 1.25rem;
        }
        .stat-label {
            font-size: 0.7rem; font-weight: 600;
            text-transform: uppercase; letter-spacing: 0.08em;
            color: #4a5568; margin-bottom: 4px;
        }
        .stat-value {
            font-size: 1.1rem; font-weight: 700; color: #f1f5f9;
        }

        /* ── Process log ── */
        .log-panel {
            background: #080a0f;
            border: 1px solid #1e2330;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #4ade80;
            line-height: 1.7;
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 1.5rem;
        }

        /* ── Chat messages ── */
        .user-bubble {
            background: #1e2330;
            border: 1px solid #2a3347;
            border-radius: 12px;
            padding: 0.85rem 1.1rem;
            margin: 0.75rem 0;
            color: #e2e8f0;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* ── Response panel ── */
        .response-panel {
            background: #111520;
            border: 1px solid #1e2330;
            border-left: 3px solid #2563eb;
            border-radius: 10px;
            padding: 1.75rem 2rem;
            margin: 0.75rem 0 1.5rem 0;
            line-height: 1.9;
            font-size: 0.95rem;
            color: #cbd5e1;
        }
        .response-panel h2 {
            font-size: 0.8rem; font-weight: 700;
            letter-spacing: 0.1em; text-transform: uppercase;
            color: #2563eb; margin: 1.75rem 0 0.6rem 0;
            font-family: 'JetBrains Mono', monospace;
        }
        .response-panel h2:first-child { margin-top: 0; }
        .response-panel strong { color: #f1f5f9; }
        .response-panel em { color: #94a3b8; font-style: normal; }

        /* ── Source tag ── */
        .source-tag {
            display: inline-block;
            background: #0d1526;
            border: 1px solid #1e3a5f;
            color: #60a5fa;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 4px;
            margin: 2px 4px 2px 0;
        }

        /* ── Input area ── */
        .stChatInputContainer {
            background: #111520 !important;
            border: 1px solid #2a3347 !important;
            border-radius: 10px !important;
        }

        /* ── Expander ── */
        .streamlit-expanderHeader {
            background: #111520 !important;
            border: 1px solid #1e2330 !important;
            border-radius: 8px !important;
            color: #64748b !important;
            font-size: 0.8rem !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* ── Divider ── */
        hr { border-color: #1e2330 !important; margin: 2rem 0 !important; }

        /* ── Footer ── */
        .page-footer {
            text-align: center;
            color: #2d3748;
            font-size: 0.72rem;
            padding: 2rem 0 1rem 0;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.04em;
        }
        </style>
    """, unsafe_allow_html=True)

inject_styles()

# ======================================================================================================================
# SECTION 4: INTELLIGENCE SERVICES
# ======================================================================================================================

class LogService:
    @staticmethod
    def init():
        if "log" not in st.session_state:
            st.session_state.log = []
        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def push(msg: str, level: str = "info"):
        ts = datetime.now().strftime('%H:%M:%S')
        prefix = {"info": "·", "ok": "✓", "fail": "✗", "warn": "⚠"}.get(level, "·")
        st.session_state.log.append(f"[{ts}] {prefix} {msg}")
        if len(st.session_state.log) > 50:
            st.session_state.log.pop(0)

    @staticmethod
    def get() -> str:
        return "\n".join(st.session_state.log) if st.session_state.log else "System initialised. Ready for queries."


class VaultManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBED_MODEL,
            model_kwargs={'trust_remote_code': True}
        )
        self.vault = self._load()

    def _load(self) -> Optional[FAISS]:
        for path in Config.VAULT_PATHS:
            target = os.path.join(path, "index.faiss")
            if os.path.exists(target):
                try:
                    LogService.push(f"Knowledge vault found: {path}", "ok")
                    return FAISS.load_local(
                        folder_path=path,
                        embeddings=self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                except Exception as ex:
                    LogService.push(f"Vault load failed at {path}: {ex}", "fail")
        LogService.push("Knowledge vault not found in any configured path.", "fail")
        return None


class QueryOrchestrator:
    def __init__(self, api_key: str, vault: FAISS):
        self.vault = vault
        self.llm_70b = ChatGroq(groq_api_key=api_key, model_name=Config.CHIEF_MODEL, temperature=Config.TEMPERATURE)
        self.llm_8b  = ChatGroq(groq_api_key=api_key, model_name=Config.UTILITY_MODEL, temperature=0.1)

    def run(self, query: str) -> Generator:
        # Step 1: Query refinement
        LogService.push("Refining query and isolating key parameters...", "info")
        try:
            refined = self.llm_8b.invoke(
                f"Break this procurement query into: Category, Cost estimate, Urgency, and Technical specs. Query: '{query}'"
            ).content
        except Exception:
            refined = query

        # Step 2: Evidence retrieval
        LogService.push("Retrieving relevant sections from knowledge base...", "info")
        docs = self.vault.as_retriever(search_kwargs={"k": Config.MINING_DEPTH}).invoke(refined)

        context = ""
        sources = set()
        for i, doc in enumerate(docs):
            src = doc.metadata.get('source', 'Knowledge Base')
            sources.add(os.path.basename(src))
            context += f"\n[Section {i+1} | {src}]\n{doc.page_content}\n"

        LogService.push(f"Retrieved {len(docs)} sections from: {', '.join(sources)}", "ok")

        # Step 3: Strategic synthesis
        LogService.push("Generating structured procurement analysis...", "info")

        prompt = f"""You are a Senior Procurement Advisor at the National Academy of Defence Production (NADP), Nagpur.
Your task is to provide a clear, structured analysis based strictly on the Indian Defence procurement manuals provided.

KNOWLEDGE BASE:
{context}

QUERY ANALYSIS:
{refined}

Provide a comprehensive response covering these six areas. Use the exact headings below:

## POLICY CLASSIFICATION
Identify whether this is Capital (DAP 2020/2026) or Revenue (DPM) procurement. Define the applicable procurement category and mode. Cite the relevant manual and chapter.

## PROCEDURAL PATHWAY
Provide the step-by-step administrative process from Acceptance of Necessity (AoN) to contract signing. Reference specific annexures, proformas, and DPM volumes required.

## FINANCIAL AUTHORITY
Identify the Competent Financial Authority (CFA) using DFPDS 2026 delegation schedules. State the applicable financial limits and any approvals required above those limits.

## STRATEGIC CONTEXT
Explain how this procurement aligns with the Technology Perspective and Capability Roadmap (TPCR) and Atmanirbhar Bharat objectives. Reference any relevant Make in India provisions.

## RISK FACTORS
Highlight potential audit objections (C&AG), procedural conflicts between DAP and DPM, or tender irregularity risks. Be specific.

## RECOMMENDED NEXT STEPS
Provide three clear, actionable steps the administering officer should take immediately to advance this file.

Rules:
- Cite the specific manual (DAP, DPM Vol 1/2, DFPDS, TPCR, Handbook) for every factual claim.
- Be precise and direct. Avoid filler language.
- If information is not in the knowledge base, say so clearly rather than speculating.

Original query: {query}"""

        return self.llm_70b.stream(prompt)

# ======================================================================================================================
# SECTION 5: SYSTEM BOOTSTRAP
# ======================================================================================================================

def bootstrap():
    LogService.init()
    api_key = st.secrets.get("GROQ_API_KEY", Config.API_KEY)

    if not api_key:
        st.error("API key not configured. Add GROQ_API_KEY to Streamlit secrets.")
        st.stop()

    if "orchestrator" not in st.session_state:
        with st.spinner("Loading knowledge base..."):
            vault_mgr = VaultManager()
            if vault_mgr.vault:
                st.session_state.orchestrator = QueryOrchestrator(api_key=api_key, vault=vault_mgr.vault)
                LogService.push("System ready. Knowledge base loaded successfully.", "ok")
            else:
                st.session_state.orchestrator = None
                LogService.push("System offline. Knowledge vault unavailable.", "fail")

bootstrap()

# ======================================================================================================================
# SECTION 6: DASHBOARD UI
# ======================================================================================================================

# ── Header ──
vault_ok = st.session_state.get("orchestrator") is not None
status_text = "SYSTEM READY" if vault_ok else "VAULT OFFLINE"
status_color = "#4ade80" if vault_ok else "#f87171"

st.markdown(f"""
<div class="page-header">
    <div class="header-icon">🛡️</div>
    <div class="header-text">
        <h1>Defence Procurement Query Bot</h1>
        <p>National Academy of Defence Production (NADP), Nagpur · {Config.VERSION}</p>
    </div>
    <div class="header-badge" style="color: {status_color};">{status_text}</div>
</div>
""", unsafe_allow_html=True)

# ── Stats ──
st.markdown("""
<div class="stat-strip">
    <div class="stat-card">
        <div class="stat-label">Knowledge Base</div>
        <div class="stat-value">1,691 pages</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Indexed Chunks</div>
        <div class="stat-value">5,026</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Reasoning Model</div>
        <div class="stat-value">Llama 70B</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Manuals Covered</div>
        <div class="stat-value">DAP · DPM · DFPDS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Process log (collapsed by default) ──
with st.expander("Process log", expanded=False):
    st.markdown(f"<div class='log-panel'>{LogService.get()}</div>", unsafe_allow_html=True)

# ── Vault offline gate ──
if not vault_ok:
    st.error("Knowledge vault is offline. Ensure `index.faiss` exists in one of the configured vault paths.")
    st.stop()

# ── Chat history ──
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>**You:** {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='response-panel'>{msg['content']}</div>", unsafe_allow_html=True)

# ── Input ──
if user_input := st.chat_input("Describe your procurement scenario — category, estimated value, urgency..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-bubble'>**You:** {user_input}</div>", unsafe_allow_html=True)
    LogService.push(f"Query received: {user_input[:60]}...")

    response_slot = st.empty()
    full_text = ""

    try:
        for chunk in st.session_state.orchestrator.run(user_input):
            token = chunk.content if hasattr(chunk, 'content') else str(chunk)
            full_text += token
            response_slot.markdown(f"<div class='response-panel'>{full_text}▌</div>", unsafe_allow_html=True)

        response_slot.markdown(f"<div class='response-panel'>{full_text}</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": full_text})
        LogService.push("Response delivered.", "ok")

    except Exception as err:
        st.error(f"Inference error: {err}")
        LogService.push(f"Inference failed: {err}", "fail")

# ── Footer ──
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"""
<div class="page-footer">
    {Config.ACADEMY} · {Config.CAPSTONE} · {Config.DEVELOPER} · Build {Config.BUILD_ID}
</div>
""", unsafe_allow_html=True)

# ======================================================================================================================
# END OF FILE
# ======================================================================================================================
