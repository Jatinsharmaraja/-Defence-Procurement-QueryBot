# ==============================================================================
# PROJECT: DEFENCE PROCUREMENT QUERY BOT (v12.0 - ULTRA-STABLE)
# VERSION: 12.0.2 | SPEED OPTIMIZED FOR CLOUD DEPLOYMENT
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
# SECTION 1: GLOBAL CONFIG & FAIL-SAFES
# ==============================================================================

PROJECT_NAME = "Defence Procurement Query Bot"
SYSTEM_CODE = "DPQB-V12-LIGHT"

# API Key handling
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = "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"

# Telemetry function
def push_telemetry(msg, status="INFO"):
    if "session_telemetry" not in st.session_state:
        st.session_state.session_telemetry = []
    ts = datetime.now().strftime('%H:%M:%S')
    st.session_state.session_telemetry.append(f"[{ts}] {status}: {msg}")
    if len(st.session_state.session_telemetry) > 15:
        st.session_state.session_telemetry.pop(0)

# ==============================================================================
# SECTION 2: UI DESIGN
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
    .telemetry-log { background-color: #000; color: #39ff14; padding: 15px; font-size: 0.8rem; height: 220px; overflow-y: auto; border: 1px solid #333; }
    .metric-card { background: #001219; border: 1px solid #1f3a5a; padding: 10px; text-align: center; border-radius: 4px; }
    .stChatInputContainer { border: 1px solid var(--gold) !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# SECTION 3: KNOWLEDGE BRAIN (CLOUD OPTIMIZED)
# ==============================================================================

@st.cache_resource
def load_optimized_engine():
    """Loads the vault once and keeps it in memory for instant responses"""
    try:
        # Step 1: Detect Path
        vault_path = "permanent_vault" if os.path.exists("permanent_vault/index.faiss") else "."
        
        # Step 2: Initialize Embeddings (Light version)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Step 3: Load FAISS
        return FAISS.load_local(vault_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"Vault Loading Failure: {e}")
        return None

# Global engine instance
VAULT = load_optimized_engine()

# ==============================================================================
# SECTION 4: SIDEBAR HUD
# ==============================================================================

with st.sidebar:
    st.markdown(f"<h2 style='color:var(--gold);'>🛡️ COMMAND HUD</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    c1.markdown("<div class='metric-card'><p style='color:grey;font-size:0.6rem;'>CORPUS</p><p style='font-size:1.1rem;font-weight:bold;'>1.6k+p</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><p style='color:grey;font-size:0.6rem;'>SPEED</p><p style='font-size:1.1rem;font-weight:bold;'>TURBO</p></div>", unsafe_allow_html=True)

    st.markdown("### 🖥️ PROCESS MONITOR")
    log_area = st.empty()
    
    if "session_telemetry" not in st.session_state:
        push_telemetry("AEGIS Optimized Core Online.")
    
    log_area.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry)}</div>", unsafe_allow_html=True)

    if st.button("Purge Memory"):
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

    if user_input := st.chat_input("Enter procurement query..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.markdown(user_input)
        
        push_telemetry(f"Query: {user_input[:25]}...")

        with st.chat_message("assistant"):
            status_box = st.status("🛸 Searching Defence Layers...", expanded=False)
            
            # Step 1: Retrieval
            docs = VAULT.as_retriever(search_kwargs={"k": 6}).invoke(user_input)
            context = "\n".join([f"[{d.metadata.get('source','Manual')}] {d.page_content}" for d in docs])
            status_box.update(label="STRATEGIC SYNTHESIS READY", state="complete")

            # Step 2: Groq Call (Using Faster 8B model for reliability)
            llm = ChatGroq(
                groq_api_key=GROQ_API_KEY, 
                model_name="llama3-8b-8192", # CHANGED to 8B for 10x faster response
                temperature=0
            )

            prompt = f"CONTEXT:\n{context}\n\nQUERY: {user_input}\n\nStructure: 1. ANALYSIS | 2. PROCEDURE | 3. AUTHORITY | 4. SOLUTION. Cite manuals."
            
            output_ui = st.empty()
            full_res = ""
            
            try:
                # Step 3: Stream with Fail-Safe Parser
                for part in llm.stream(prompt):
                    # Handle both object and string responses
                    token = part.content if hasattr(part, 'content') else str(part)
                    full_res += token
                    output_ui.markdown(full_res + "▌")
                
                output_ui.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                push_telemetry("Report Delivered.")
            except Exception as e:
                st.error("Engine saturation. Retrying...")
                push_telemetry(f"FAIL: {str(e)}", "ERROR")
else:
    st.error("CRITICAL: Vault missing. Ensure 'index.faiss' is in GitHub root.")

# Visual log update
log_area.markdown(f"<div class='telemetry-log'>{chr(10).join(st.session_state.session_telemetry)}</div>", unsafe_allow_html=True)
