# ======================================================================================================================
# DEFENCE PROCUREMENT QUERY BOT — TITAN v26.0
# National Academy of Defence Production (NADP), Nagpur
# Academic Mentor: Dr. Indu Mazumdar | Industrial Mentor: Mr. S.K. Bhola (Ex-CGM/AVNL)
# Version: 26.0.0 — Clean UI Rebuild + API Key input + All v25 fixes retained
# ======================================================================================================================

import streamlit as st
import os
import time
import logging
from datetime import datetime
from typing import Optional, Generator

# ─── Dependency Imports ──────────────────────────────────────────────────────

try:
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_groq import ChatGroq
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError as e:
    st.error(f"Missing dependency: {e}. Please check requirements.txt.")
    st.stop()

# ─── Configuration ────────────────────────────────────────────────────────────

class Config:
    VERSION        = "26.0.0"
    ACADEMY        = "National Academy of Defence Production (NADP), Nagpur"
    CHIEF_MODEL    = "llama-3.1-70b-versatile"
    UTILITY_MODEL  = "llama-3.1-8b-instant"
    EMBED_MODEL    = "nomic-ai/nomic-embed-text-v1.5"

    VAULT_PATHS = [
        ".",
        "permanent_vault",
        "./permanent_vault",
        "/mount/src/-defence-procurement-querybot",
        "/mount/src/-defence-procurement-querybot/permanent_vault",
    ]

    SOURCE_PRIORITY = {
        "DFPDS": 1.0,
        "TPCR":  0.9,
        "DAP":   0.8,
        "DPM":   0.7,
        "HANDBOOK": 0.5,
    }

    # Design tokens — minimal monochrome + single amber accent
    BG          = "#0d0d0d"
    SURFACE     = "#141414"
    SURFACE2    = "#1a1a1a"
    BORDER      = "#2a2a2a"
    AMBER       = "#c8933a"
    AMBER_DIM   = "#7a5520"
    TEXT        = "#e8e8e8"
    TEXT_MUTED  = "#888888"
    TEXT_DIM    = "#555555"
    GREEN       = "#3dba6f"
    RED         = "#c0392b"


logging.basicConfig(level=logging.INFO, format="%(asctime)s | TITAN | %(message)s")
logger = logging.getLogger("TITAN")

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Defence Procurement Query Bot | NADP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset & Base */
*, *::before, *::after {{ box-sizing: border-box; }}

.stApp {{
    background-color: {Config.BG};
    color: {Config.TEXT};
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 15px;
    line-height: 1.6;
}}

/* Hide Streamlit chrome */
[data-testid="stSidebar"],
[data-testid="stToolbar"],
header, footer {{ display: none !important; }}

/* Main content width */
.main .block-container {{
    max-width: 900px;
    margin: 0 auto;
    padding: 0 24px 80px 24px;
}}

/* ── Header ── */
.app-header {{
    padding: 48px 0 36px 0;
    border-bottom: 1px solid {Config.BORDER};
    margin-bottom: 40px;
}}
.app-header-eyebrow {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: {Config.AMBER};
    margin-bottom: 10px;
    font-family: 'JetBrains Mono', monospace;
}}
.app-header h1 {{
    font-size: 26px;
    font-weight: 600;
    color: {Config.TEXT};
    margin: 0 0 6px 0;
    letter-spacing: -0.3px;
}}
.app-header-sub {{
    font-size: 13px;
    color: {Config.TEXT_MUTED};
}}

/* ── Status Bar ── */
.status-bar {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 12px 16px;
    background: {Config.SURFACE};
    border: 1px solid {Config.BORDER};
    border-radius: 6px;
    margin-bottom: 32px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}}
.status-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    flex-shrink: 0;
}}
.dot-green  {{ background: {Config.GREEN}; box-shadow: 0 0 6px {Config.GREEN}88; }}
.dot-amber  {{ background: {Config.AMBER}; box-shadow: 0 0 6px {Config.AMBER}88; }}
.dot-red    {{ background: {Config.RED};   box-shadow: 0 0 6px {Config.RED}88; }}
.status-item {{ color: {Config.TEXT_MUTED}; white-space: nowrap; }}
.status-item span {{ color: {Config.TEXT}; font-weight: 500; }}
.status-divider {{ width: 1px; height: 16px; background: {Config.BORDER}; }}

/* ── API Key Input ── */
.api-key-section {{
    background: {Config.SURFACE};
    border: 1px solid {Config.BORDER};
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 28px;
}}
.api-key-label {{
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {Config.TEXT_MUTED};
    margin-bottom: 10px;
    font-family: 'JetBrains Mono', monospace;
}}
.api-key-hint {{
    font-size: 12px;
    color: {Config.TEXT_DIM};
    margin-top: 8px;
}}
.api-key-hint a {{ color: {Config.AMBER}; text-decoration: none; }}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}}

/* User message bubble */
[data-testid="stChatMessage"][data-testid*="user"] .stMarkdown,
.user-msg {{
    background: {Config.SURFACE};
    border: 1px solid {Config.BORDER};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 6px 0;
    font-size: 14px;
}}

/* Assistant response */
.response-card {{
    border-left: 3px solid {Config.AMBER};
    padding: 28px 28px 28px 32px;
    margin: 8px 0 24px 0;
    background: {Config.SURFACE};
    border-radius: 0 8px 8px 0;
    font-size: 14px;
    line-height: 1.8;
}}
.response-card h2, .response-card h3 {{
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: {Config.AMBER};
    margin: 24px 0 10px 0;
    font-family: 'JetBrains Mono', monospace;
}}
.response-card h2:first-child, .response-card h3:first-child {{
    margin-top: 0;
}}
.response-card p {{ margin: 0 0 10px 0; color: {Config.TEXT}; }}
.response-card strong {{ color: #fff; font-weight: 600; }}
.response-card hr {{
    border: none;
    border-top: 1px solid {Config.BORDER};
    margin: 20px 0;
}}
.response-card code {{
    background: {Config.SURFACE2};
    padding: 1px 6px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: {Config.AMBER};
}}

/* ── Log terminal ── */
.log-panel {{
    background: {Config.SURFACE};
    border: 1px solid {Config.BORDER};
    border-radius: 6px;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    color: {Config.TEXT_DIM};
    max-height: 160px;
    overflow-y: auto;
    margin-bottom: 28px;
    line-height: 1.6;
}}
.log-panel .log-ok   {{ color: {Config.GREEN}; }}
.log-panel .log-fail {{ color: {Config.RED}; }}
.log-panel .log-warn {{ color: {Config.AMBER}; }}

/* ── Error / info banners ── */
.banner {{
    padding: 14px 18px;
    border-radius: 6px;
    font-size: 13px;
    margin-bottom: 20px;
    line-height: 1.6;
}}
.banner-error {{
    background: rgba(192,57,43,0.12);
    border: 1px solid rgba(192,57,43,0.4);
    color: #e88;
}}
.banner-info {{
    background: rgba(200,147,58,0.08);
    border: 1px solid {Config.AMBER_DIM};
    color: {Config.TEXT_MUTED};
}}
.banner-success {{
    background: rgba(61,186,111,0.08);
    border: 1px solid rgba(61,186,111,0.3);
    color: {Config.TEXT_MUTED};
}}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {{
    background: {Config.SURFACE} !important;
    border: 1px solid {Config.BORDER} !important;
    border-radius: 8px !important;
    color: {Config.TEXT} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 14px 16px !important;
    transition: border-color 0.15s;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color: {Config.AMBER} !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(200,147,58,0.08) !important;
}}

/* ── Section labels ── */
.section-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: {Config.TEXT_DIM};
    margin: 28px 0 12px 0;
    font-family: 'JetBrains Mono', monospace;
}}

/* ── Footer ── */
.app-footer {{
    border-top: 1px solid {Config.BORDER};
    padding: 24px 0;
    margin-top: 48px;
    font-size: 12px;
    color: {Config.TEXT_DIM};
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
}}

/* Streamlit widget overrides */
.stTextInput input, .stPasswordInput input {{
    background: {Config.BG} !important;
    border: 1px solid {Config.BORDER} !important;
    color: {Config.TEXT} !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}}
.stTextInput input:focus, .stPasswordInput input:focus {{
    border-color: {Config.AMBER} !important;
    box-shadow: 0 0 0 3px rgba(200,147,58,0.1) !important;
}}
div[data-testid="stForm"] {{ border: none !important; background: transparent !important; }}

/* Streamlit button */
.stButton button {{
    background: {Config.AMBER} !important;
    color: #000 !important;
    border: none !important;
    border-radius: 5px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
    cursor: pointer !important;
    transition: opacity 0.15s !important;
}}
.stButton button:hover {{ opacity: 0.85 !important; }}

/* Spinner */
.stSpinner {{ color: {Config.AMBER} !important; }}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ───────────────────────────────────────────────────────

def init_state():
    defaults = {
        "messages":    [],
        "logs":        [],
        "orchestrator": None,
        "vault_status": "uninitialised",
        "api_key":     "",
        "boot_done":   False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Telemetry ────────────────────────────────────────────────────────────────

def log(msg: str, level: str = "sys"):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append((ts, level, msg))
    logger.info(f"[{level.upper()}] {msg}")
    if len(st.session_state.logs) > 100:
        st.session_state.logs.pop(0)

def render_logs():
    if not st.session_state.logs:
        return "<div class='log-panel'>Waiting for activity…</div>"
    lines = []
    for ts, level, msg in st.session_state.logs[-30:]:
        cls = {"ok": "log-ok", "fail": "log-fail", "warn": "log-warn"}.get(level, "")
        cls_attr = f" class='{cls}'" if cls else ""
        lines.append(f"<span{cls_attr}>[{ts}] {msg}</span>")
    body = "<br>".join(lines)
    return f"<div class='log-panel'>{body}</div>"

# ─── System Prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are the TITAN Strategic Oracle — Chief Procurement Advisor at the National Academy of Defence Production (NADP), Nagpur.

Your role is to provide authoritative, Ministry-grade procurement intelligence strictly grounded in official manuals: DAP 2020/2026, DPM Vol I & II, DFPDS 2026, TPCR, and the Handbook on DPP.

RULES:
- Every factual claim MUST cite the exact Manual, Chapter, Para, or Appendix (e.g. "DAP 2020, Chapter II, Para 6" or "DFPDS 2026, Schedule IV").
- Never fabricate rule numbers, CFA limits, or procedural steps.
- If the knowledge base lacks a clear answer, say so explicitly and indicate which manual section would normally govern.
- Tone: authoritative, precise, Ministry-appropriate.

RESPONSE FORMAT — use this structure every time:

## POLICY CLASSIFICATION
[Capital vs Revenue. Procurement category: Buy (Indian-IDDM / Indian / Global), Make, or Lease. Cite DAP/DPM chapter.]

## PROCEDURAL PATHWAY
[Step-by-step process. Reference specific Appendices, Schedules, Forms. Include the full AON → RFPI/RFP → CoNC → SQR → TOEC → CNC → Contract sequence where applicable.]

## FINANCIAL POWER AUDIT
[Exact CFA tier for the stated value — Secretary (Defence), RM, DPB, AHQ, etc. Cite DFPDS 2026 Schedule number and ceiling. Flag if SFC/DAC/CCS approval is required.]

## STRATEGIC & TPCR ALIGNMENT
[TPCR technology domain. Make in India / iDEX / SRIJAN relevance. ToT or indigenisation potential.]

## RISK AUDIT
[Single-vendor risk and PAC justification; SQR framing risks; offset obligation triggers; integrity pact requirements; L1 price negotiation constraints; time-overrun risks.]

## ACTIONABLE ROADMAP
Step 1 — [Immediate administrative action and responsible authority]
Step 2 — [Key approval or committee action required]
Step 3 — [Contract finalisation or next milestone trigger]

## SOURCES
[List all manuals and document layers consulted.]
"""

# ─── Neural Vault ─────────────────────────────────────────────────────────────

class NeuralKnowledgeVaultController:
    def __init__(self):
        self.vault: Optional[FAISS] = None
        self.embeddings = None
        self._load_embeddings()
        self._mount_vault()

    def _load_embeddings(self):
        try:
            log("Loading embedding model…")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=Config.EMBED_MODEL,
                model_kwargs={"trust_remote_code": True},
            )
            log("Embedding model ready.", "ok")
        except Exception as e:
            log(f"Embedding model failed: {e}", "fail")

    def _mount_vault(self):
        if not self.embeddings:
            log("Vault mount skipped — no embeddings.", "fail")
            return
        for path in Config.VAULT_PATHS:
            if os.path.exists(os.path.join(path, "index.faiss")) and \
               os.path.exists(os.path.join(path, "index.pkl")):
                try:
                    log(f"Mounting vault: {path}")
                    self.vault = FAISS.load_local(
                        folder_path=path,
                        embeddings=self.embeddings,
                        allow_dangerous_deserialization=True,
                    )
                    log(f"Vault online — {path}", "ok")
                    st.session_state.vault_status = "online"
                    return
                except Exception as e:
                    log(f"Vault error at {path}: {e}", "fail")
        log("No vault found. Upload index.faiss + index.pkl to repo root.", "fail")
        st.session_state.vault_status = "offline"

# ─── Orchestrator ─────────────────────────────────────────────────────────────

class TitanOrchestrator:
    def __init__(self, api_key: str, vault: FAISS):
        self.vault = vault
        self.llm_70b = ChatGroq(groq_api_key=api_key, model_name=Config.CHIEF_MODEL,   temperature=0)
        self.llm_8b  = ChatGroq(groq_api_key=api_key, model_name=Config.UTILITY_MODEL, temperature=0.1)

    def _expand_query(self, query: str) -> str:
        try:
            prompt = (
                f"Rewrite this query using precise MoD procurement terminology "
                f"(DAP 2020, DPM, DFPDS 2026, TPCR). Return ONLY the rewritten query.\n\nQuery: {query}"
            )
            result = self.llm_8b.invoke(prompt)
            expanded = result.content.strip()
            log(f"Query expanded: {expanded[:70]}…")
            return expanded
        except Exception as e:
            log(f"Query expansion failed: {e}", "warn")
            return query

    def _retrieve_evidence(self, query: str) -> tuple[str, list[str]]:
        try:
            docs = self.vault.as_retriever(search_kwargs={"k": 20}).invoke(query)
        except Exception as e:
            log(f"Retrieval error: {e}", "fail")
            return "", []

        seen, ranked, sources = set(), [], set()
        for doc in docs:
            h = hash(doc.page_content[:200])
            if h in seen:
                continue
            seen.add(h)
            src = doc.metadata.get("source", "Manual Repository")
            key = next((k for k in Config.SOURCE_PRIORITY if k.upper() in src.upper()), "HANDBOOK")
            ranked.append((Config.SOURCE_PRIORITY[key], src, doc.page_content))
            sources.add(src)

        ranked.sort(reverse=True)
        ctx = ""
        for i, (p, src, content) in enumerate(ranked[:18], 1):
            ctx += f"\n[Layer {i:02d} | {src} | priority {p}]\n{content.strip()}\n{'─'*50}\n"

        log(f"Retrieved {len(ranked)} chunks from {len(sources)} source(s).", "ok")
        return ctx, sorted(sources)

    def stream(self, query: str) -> Generator:
        log("Pipeline started.")
        expanded = self._expand_query(query)
        evidence, sources = self._retrieve_evidence(expanded)

        if not evidence:
            evidence = "[No evidence retrieved — vault may be offline.]"

        user_msg = (
            f"EVIDENCE BASE:\n{evidence}\n\n"
            f"QUERY:\n{query}\n\n"
            f"Sources available: {', '.join(sources) if sources else 'None'}"
        )

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_msg),
        ]

        log("Streaming from Llama 3.1-70B…")
        try:
            for chunk in self.llm_70b.stream(messages):
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
            log("Response complete.", "ok")
        except Exception as e:
            log(f"Streaming error: {e}", "fail")
            yield f"\n\n**Error:** {str(e)}"

# ─── Boot ─────────────────────────────────────────────────────────────────────

def boot(api_key: str):
    if st.session_state.boot_done:
        return
    log("System starting…")
    with st.spinner("Initialising knowledge vault…"):
        try:
            vault_handler = NeuralKnowledgeVaultController()
            if vault_handler.vault:
                st.session_state.orchestrator = TitanOrchestrator(api_key, vault_handler.vault)
                log("System ready.", "ok")
            else:
                st.session_state.orchestrator = None
        except Exception as e:
            log(f"Boot error: {e}", "fail")
            st.session_state.orchestrator = None
    st.session_state.boot_done = True

# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="app-header">
    <div class="app-header-eyebrow">NADP · SEM-IV CAPSTONE 2025–26</div>
    <h1>Defence Procurement Query Bot</h1>
    <div class="app-header-sub">
        Analytical intelligence across DAP 2026 · DPM Vol I &amp; II · DFPDS 2026 · TPCR · Handbook on DPP
    </div>
</div>
""", unsafe_allow_html=True)

# ─── API Key Input ─────────────────────────────────────────────────────────────

# Resolve key: secrets → env → user input
resolved_key = (
    st.secrets.get("GROQ_API_KEY", None)
    or os.environ.get("GROQ_API_KEY", None)
    or st.session_state.api_key
)

if not resolved_key:
    st.markdown(f"""
    <div class="banner banner-error">
        <strong>Groq API key required.</strong><br>
        The hardcoded key has expired. Add your key below, or set <code>GROQ_API_KEY</code> 
        in Streamlit Secrets (Manage app → Secrets).
    </div>
    """, unsafe_allow_html=True)

    with st.form("key_form", clear_on_submit=False):
        st.markdown("<div class='api-key-label'>Groq API Key</div>", unsafe_allow_html=True)
        entered_key = st.text_input(
            label="Groq API Key",
            type="password",
            placeholder="gsk_…",
            label_visibility="collapsed",
        )
        st.markdown(
            "<div class='api-key-hint'>Get a free key at "
            "<a href='https://console.groq.com/keys' target='_blank'>console.groq.com/keys</a>. "
            "For persistent use, add to Streamlit Secrets.</div>",
            unsafe_allow_html=True
        )
        submitted = st.form_submit_button("Connect")
        if submitted and entered_key.strip():
            st.session_state.api_key = entered_key.strip()
            st.session_state.boot_done = False  # re-boot with new key
            st.rerun()
    st.stop()
else:
    # Boot with resolved key
    boot(resolved_key)

# ─── Status Bar ──────────────────────────────────────────────────────────────

vault_st   = st.session_state.vault_status
vault_dot  = "dot-green" if vault_st == "online" else "dot-red"
vault_label = "Online" if vault_st == "online" else "Offline"
orch_dot   = "dot-green" if st.session_state.orchestrator else "dot-red"
orch_label = "Ready" if st.session_state.orchestrator else "Unavailable"

st.markdown(f"""
<div class="status-bar">
    <span class="status-item">
        <span class="status-dot {vault_dot}"></span>
        Knowledge Vault <span>{vault_label}</span>
    </span>
    <div class="status-divider"></div>
    <span class="status-item">
        <span class="status-dot {orch_dot}"></span>
        Engine <span>{orch_label}</span>
    </span>
    <div class="status-divider"></div>
    <span class="status-item">Model <span>Llama 3.1-70B</span></span>
    <div class="status-divider"></div>
    <span class="status-item">Sources <span>1,691 pages · 5,026 nodes</span></span>
</div>
""", unsafe_allow_html=True)

# ─── Activity Log (collapsed) ────────────────────────────────────────────────

with st.expander("System log", expanded=False):
    st.markdown(render_logs(), unsafe_allow_html=True)

# ─── Vault offline notice ─────────────────────────────────────────────────────

if st.session_state.orchestrator is None:
    st.markdown(f"""
    <div class="banner banner-error">
        <strong>Knowledge vault is offline.</strong><br>
        Run <code>ingest.py</code> to generate <code>index.faiss</code> and <code>index.pkl</code>, 
        then commit both files to the root of your GitHub repository and redeploy.<br><br>
        Paths searched: {', '.join(f'<code>{p}</code>' for p in Config.VAULT_PATHS)}
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Chat history ─────────────────────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(
                f"<div class='response-card'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(msg["content"])

# ─── New query ────────────────────────────────────────────────────────────────

if prompt := st.chat_input("Describe your procurement problem…"):
    prompt = prompt.strip()
    if not prompt:
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    log(f"Query: {prompt[:60]}…")

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        with st.spinner("Analysing across manuals…"):
            try:
                for token in st.session_state.orchestrator.stream(prompt):
                    full_text += token
                    placeholder.markdown(
                        f"<div class='response-card'>{full_text}▌</div>",
                        unsafe_allow_html=True
                    )
                placeholder.markdown(
                    f"<div class='response-card'>{full_text}</div>",
                    unsafe_allow_html=True
                )
                st.session_state.messages.append({"role": "assistant", "content": full_text})

            except Exception as e:
                err = f"**Query failed:** {str(e)}"
                placeholder.markdown(
                    f"<div class='banner banner-error'>{err}</div>",
                    unsafe_allow_html=True
                )
                log(f"Engine error: {e}", "fail")

# ─── Footer ──────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="app-footer">
    <span>{Config.ACADEMY}</span>
    <span>v{Config.VERSION} · Lead: Jatin Sharma</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# END TITAN v26.0
# ══════════════════════════════════════════════════════════════════════════════
