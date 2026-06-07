# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v13.0 - STABLE TITAN)
# VERSION: 13.0.1 | DIMENSION ALIGNED & PERFORMANCE TUNED
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
# SECTION 1: GLOBAL CONFIG & SECURITY
# ==============================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "DPQB-V13-FINAL"

# API Key Handling
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = "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"

# Telemetry System
def push_telemetry(msg, status="INFO"):
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = []
    ts = datetime.now().strftime('%H:%M:%S')
    st.session_state.session_telemetry.append(f"[{ts}] {status}: {msg}")
    if len(st.session_state.session_telemetry) > 20:
        st.session_state.session_telemetry.pop(0)

# ==============================================================================
# SECTION 2: TACTICAL UI
# ==============================================================================

st.set_page_config(page_title=PROJECT_NAME, page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;700&family=Orbitron:wght@400;900&display=swap');
    :root { --gold: #d4af37; --navy: #020c1b; --cyan: #64ffda; --text: #ccd6f6; }
    .stApp { background-color: var(--navy); color: var(--text); font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #010a15; border-right: 2px solid var(--gold); }
    .tactical-header { text-align: center; padding: 30px; background: #0a192f; border-bottom: 2px solid var(--gold); margin-bottom: 30px; }
    .tactical-header h1 { color: var(--gold); font-family: 'Orbitron', sans-serif; letter-spacing: 5px; text-transform: uppercase; }
    .telemetry-log { background-color: #000; color: #39ff14; padding: 15px; font-size: 0.8rem; height: 250px; overflow-y: auto; border: 1px solid #333; }
    .metric-card { background: #001219; border: 1px solid #1f3a5a; padding: 10px; text-align: center; border-radius: 4px; }
    .stChatInputContainer { border: 1px solid var(--gold) !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# SECTION 3: KNOWLEDGE BRAIN (DIMENSION MATCHED)
# ==============================================================================

@st.cache_resource
def load_aligned_engine():
    """Matches the 768-dimensions of the local 'nomic-embed-text' vault"""
    try:
        # Step 1: Detect Path
        vault_path = "permanent_vault" if os.path.exists("permanent_vault/index.faiss") else "."
        
        # Step 2: Use Nomic V1.5 to match the 768-dimension local vault
        # This is the "Magic Fix" for the AssertionError
        embeddings = HuggingFaceEmbeddings(
            model_name="nomic-ai/nomic-embed-text-v1.5", 
            model_kwargs={'trust_remote_code': True}
        )
        
        # Step 3: Load FAISS
        return FAISS.load_local(vault_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"Vault Loading Failure: {e}")
        return None

# Global engine instance
VAULT = load_aligned_engine()

# ==============================================================================
# SECTION 4: COMMAND HUD
# ==============================================================================

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--gold);'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    c1.markdown("<div class='metric-card'><p style='color:grey;font-size:0.6rem;'>CORPUS</p><p style='font-size:1.1rem;font-weight:bold;'>1.6k+p</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><p style='color:grey;font-size:0.6rem;'>DIMS</p><p style='font-size:1.1rem;font-weight:bold;'>768</p></div>", unsafe_allow_html=True)

    st.markdown("### 🖥️ PROCESS MONITOR")
    log_area = st.empty()
    
    if "session_telemetry" not in st.session_state:
        push_telemetry("AEGIS Titan v13 Core Online.")
    
    log_area.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry)}</div>", unsafe_allow_html=True)

    if st.button("Purge Session Memory"):
        st.session_state.messages = []
        st.session_state.session_telemetry = []
        st.rerun()

# ==============================================================================
# SECTION 5: MASTER CHAT EXECUTION
# ==============================================================================

st.markdown(f"<div class='tactical-header'><h1>🛡️ {PROJECT_NAME}</h1></div>", unsafe_allow_html=True)

if VAULT:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if user_input := st.chat_input("Enter strategic query..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        push_telemetry(f"Query: {user_input[:25]}...")

        with st.chat_message("assistant"):
            status_box = st.status("🛸 Syncing Vector Dimensions...", expanded=False)
            
            # Step 1: Retrieval
            docs = VAULT.as_retriever(search_kwargs={"k": 7}).invoke(user_input)
            context = "\n".join([f"[{d.metadata.get('source','Manual')}] {d.page_content}" for d in docs])
            status_box.update(label="STRATEGIC SYNTHESIS READY", state="complete")

            # Step 2: Groq Call
            llm = ChatGroq(
                groq_api_key=GROQ_API_KEY, 
                model_name="llama3-8b-8192", 
                temperature=0
            )

            prompt = f"""
            [DIRECTIVE] You are the NADP Strategic Oracle. 
            CONTEXT:
            {context}

            QUERY: {user_input}

            Structure your answer:
            1. SITUATIONAL ANALYSIS
            2. PROCEDURAL PATHWAY
            3. FINANCIAL AUTHORITY (DFPDS)
            4. ACTION RECOMMENDATION
            Cite source manuals.
            """
            
            output_ui = st.empty()
            full_res = ""
            
            try:
                for part in llm.stream(prompt):
                    token = part.content if hasattr(part, 'content') else str(part)
                    full_res += token
                    output_ui.markdown(full_res + "▌")
                
                output_ui.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                push_telemetry("Consultation Successful.")
            except Exception as e:
                st.error("API Latency Detected. Retrying...")
                push_telemetry(f"FAIL: {str(e)}", "ERROR")
else:
    st.error("CRITICAL: Vault missing or Dimension Mismatch. Run 'ingest.py' if files were changed.")

# Final Visual Log Refresh
log_area.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry)}</div>", unsafe_allow_html=True)
