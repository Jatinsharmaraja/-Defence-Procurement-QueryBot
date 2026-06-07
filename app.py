# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v11.0 - STABLE TITAN)
# INSTITUTION: National Academy of Defence Production (NADP), Nagpur
# ENGINE: Groq LPU + Llama 3.1 70B (High-Stability Cloud Build)
# SECURITY: Local-Vault RAG + Secure Cloud Inference
# ==============================================================================

import streamlit as st
import os
import time
import logging
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# ==============================================================================
# SECTION 1: SYSTEM IDENTITY & FAIL-SAFE SECRETS (Lines 30-110)
# ==============================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "DPQB-V11-STABLE"
ACADEMY = "NADP Nagpur"

# Audit logging initialization
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TITAN_STABLE")

# Secure API Key Handling
try:
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    else:
        # Emergency backup for direct testing
        GROQ_API_KEY = "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"
except Exception:
    GROQ_API_KEY = "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"

# ==============================================================================
# SECTION 2: ROBUST TELEMETRY UTILITIES (Lines 111-220)
# ==============================================================================

def push_telemetry(msg, status="INFO"):
    """Maintains a real-time system event log in the user session."""
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = []
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] {status}: {msg}"
    st.session_state.session_telemetry.append(log_entry)
    
    # Keep only most recent logs for performance
    if len(st.session_state.session_telemetry) > 20:
        st.session_state.session_telemetry.pop(0)

def get_formatted_logs():
    return "\n".join(st.session_state.session_telemetry)

# ==============================================================================
# SECTION 3: TACTICAL HUD DESIGN (CSS) (Lines 221-450)
# ==============================================================================

st.set_page_config(page_title=PROJECT_NAME, page_icon="🛡️", layout="wide")

def apply_military_ui():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
        
        :root {
            --gold: #d4af37;
            --navy-deep: #020c1b;
            --tactical-blue: #0a192f;
            --cyan-glow: #64ffda;
            --text-silver: #ccd6f6;
        }

        .stApp { background-color: var(--navy-deep); color: var(--text-silver); font-family: 'JetBrains Mono', monospace; }
        
        [data-testid="stSidebar"] {
            background-color: #010a15;
            border-right: 2px solid var(--gold);
            box-shadow: 10px 0px 30px rgba(0,0,0,0.5);
        }

        .tactical-header {
            text-align: center; padding: 40px; background: #0a192f;
            border-bottom: 3px double var(--gold); margin-bottom: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
        .tactical-header h1 { color: var(--gold); font-family: 'Orbitron', sans-serif; letter-spacing: 8px; text-transform: uppercase; }

        .analysis-card {
            background-color: #112240; border: 1px solid var(--cyan-glow);
            padding: 25px; border-radius: 4px; border-left: 8px solid var(--gold);
            margin-bottom: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        }

        .telemetry-log {
            background-color: #000; color: #39ff14; padding: 15px;
            font-size: 0.82rem; height: 250px; overflow-y: auto;
            border: 1px solid #333; font-family: 'Courier New', monospace;
        }

        .metric-unit { background: #001219; border: 1px solid #1f3a5a; padding: 15px; text-align: center; border-radius: 3px; }
        .stChatInputContainer { border: 1px solid var(--gold) !important; }
        </style>
    """, unsafe_allow_html=True)

apply_military_ui()

# ==============================================================================
# SECTION 4: KNOWLEDGE CORE (Lines 451-680)
# ==============================================================================

class TitanIntelligenceEngine:
    """Orchestrates Optimized Strategic Retrieval and Inference."""
    
    def __init__(self, api_key):
        self.key = api_key
        # Memory-optimized Embedding model for Cloud
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Enhanced Path Detection
        if os.path.exists("permanent_vault/index.faiss"):
            self.vault_path = "permanent_vault"
        elif os.path.exists("index.faiss"):
            self.vault_path = "."
        else:
            self.vault_path = None
            
        self.vault = self._load_vault()

    def _load_vault(self):
        if not self.vault_path: return None
        try:
            return FAISS.load_local(
                self.vault_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            logger.error(f"VAULT_ERR: {e}")
            return None

    def synthesize_analysis(self, user_query):
        if not self.vault: return "ERROR: Vault files missing in GitHub."

        # RETRIEVAL (K=8 optimized for speed and token limits)
        retriever = self.vault.as_retriever(search_kwargs={"k": 8})
        docs = retriever.invoke(user_query)
        
        context_data = ""
        for i, d in enumerate(docs):
            src = d.metadata.get('source', 'Classified Manual')
            context_data += f"\n[LAYER {i+1} | ORIGIN: {src}]\n{d.page_content}\n"

        # SYSTEM PROMPT (Pointed Analytical Approach)
        directive = f"""
        YOU ARE THE 'DEFENCE PROCUREMENT QUERY BOT'.
        MISSION: Execute a 360-degree consultation on procurement.
        
        KNOWLEDGE EVIDENCE BASE:
        {context_data}

        PROTOCOL:
        1. 📋 SITUATIONAL ANALYSIS: Determine project category.
        2. ⚖️ PROCEDURAL PATHWAY: Steps from Manuals & Handbooks.
        3. 💰 FINANCIAL AUTHORITY: Identify CFA via DFPDS 2026.
        4. ✅ FINAL ACTION PLAN: 3 actionable steps.

        CITATIONS: Cite manuals for every rule.
        """

        llm = ChatGroq(
            groq_api_key=self.key, 
            model_name="llama-3.1-70b-versatile",
            temperature=0,
            max_tokens=1500
        )
        
        return llm.stream(directive + "\n\nUser Question: " + user_query)

# ==============================================================================
# SECTION 5: COMMAND SIDEBAR HUD (Lines 681-800)
# ==============================================================================

if not GROQ_API_KEY:
    st.error("FATAL: Security Key Missing.")
    st.stop()

# Cache engine to prevent repeated loading
if "engine" not in st.session_state:
    st.session_state.engine = TitanIntelligenceEngine(GROQ_API_KEY)

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--gold);'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.markdown("<div class='metric-unit'><p style='color:gold;font-size:0.7rem;'>CORPUS</p><p style='font-size:1.4rem;font-weight:bold;'>1.6k+p</p></div>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<div class='metric-unit'><p style='color:gold;font-size:0.7rem;'>ENGINE</p><p style='font-size:1.4rem;font-weight:bold;'>GROQ</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🖥️ PROCESS MONITOR LOG")
    log_box = st.empty()
    
    if "session_telemetry" not in st.session_state:
        push_telemetry("AEGIS Titan Stable Core Online.")
    
    log_box.markdown(f"<div class='telemetry-log'>{get_formatted_logs()}</div>", unsafe_allow_html=True)

    if st.button("🔴 PURGE SESSION"):
        st.session_state.messages = []
        st.session_state.session_telemetry = []
        st.rerun()

# ==============================================================================
# SECTION 6: ANALYTICAL DASHBOARD EXECUTION (Lines 801-950)
# ==============================================================================

st.markdown(f"<div class='tactical-header'><h1>🛡️ {PROJECT_NAME}</h1></div>", unsafe_allow_html=True)
st.caption(f"NADP Nagpur Strategic Dashboard | Build: {SYSTEM_CODE}")

if not st.session_state.engine.vault:
    st.error("SYSTEM ERROR: Permanent Vault files (index.faiss) not detected. Check GitHub.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if user_input := st.chat_input("Enter procurement query..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)

    push_telemetry(f"Input: {user_input[:35]}...")

    with st.chat_message("assistant"):
        with st.status("🛸 Accessing Defence Knowledge Layers...", expanded=False):
            st.write("Synthesizing context...")
            time.sleep(0.3)
        
        output_surface = st.empty()
        full_analysis = ""
        
        try:
            # ROBUST STREAM PARSING to prevent 'str' object attribute error
            for part in st.session_state.engine.synthesize_analysis(user_input):
                # FIXED ATTRIBUTE LOGIC
                if hasattr(part, 'content'):
                    token = part.content
                elif isinstance(part, str):
                    token = part
                else:
                    token = getattr(part, 'text', str(part))
                
                full_analysis += token
                output_surface.markdown(full_analysis + "▌")
            
            output_surface.markdown(full_analysis)
            push_telemetry("Report Delivered.")
            st.session_state.messages.append({"role": "assistant", "content": full_analysis})
        
        except Exception as e:
            st.error(f"ENGINE TIMEOUT: {str(e)}")
            push_telemetry(f"ERROR: {str(e)}", status="FAIL")

# Update visual logs
log_box.markdown(f"<div class='telemetry-log'>{get_formatted_logs()}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #555; font-size: 0.75rem;'>Proprietary Tool | NADP Nagpur | Capstone 2025-26</p>", unsafe_allow_html=True)
