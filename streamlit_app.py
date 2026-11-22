import os

import streamlit as st
from dotenv import load_dotenv

from chatbot.bot import (
    SUPPORTED_MODELS,
    build_langchain_messages,
    get_groq_llm,
    stream_groq_response,
)

# 1. Load environment variables from .env file
load_dotenv()

# 2. Configure Streamlit Page
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Groq AI Chatbot with LangChain")
st.caption("Powered by Groq Cloud, LangChain, and Streamlit")

# 3. Sidebar Configuration & Credential handling
with st.sidebar:
    st.header("⚙️ Configuration")

    # Read credentials from .env first
    env_api_key = os.getenv("GROQ_API_KEY", "").strip()

    if env_api_key:
        st.success("✅ `GROQ_API_KEY` loaded from `.env`")
        api_key = env_api_key
    else:
        st.warning("⚠️ `GROQ_API_KEY` not found in `.env`")
        api_key = st.text_input(
            "Enter Groq API Key:",
            type="password",
            help="Get your key at https://console.groq.com/keys",
        ).strip()

    # Model selection
    selected_model = st.selectbox(
        "Choose Groq Model:",
        options=SUPPORTED_MODELS,
        index=0,
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature:",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Higher values make output more creative, lower values more deterministic.",
    )

    # Max output tokens (safeguards free tier limit)
    max_tokens = st.slider(
        "Max Output Tokens:",
        min_value=50,
        max_value=1000,
        value=500,
        step=50,
        help="Free tier OTPM limit is 1000 tokens per minute.",
    )

    # System Prompt customization
    system_prompt = st.text_area(
        "System Prompt:",
        value="You are a helpful, knowledgeable, and polite AI assistant.",
        height=100,
    )

    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. Initialize session state chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display existing conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Chat Input & Response Generation
if user_prompt := st.chat_input("Type your message here..."):
    if not api_key:
        st.error("❌ Please provide a valid Groq API Key in your `.env` file or sidebar to chat.")
    else:
        # Display user message immediately
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            try:
                llm = get_groq_llm(
                    api_key=api_key,
                    model_name=selected_model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                langchain_messages = build_langchain_messages(
                    chat_history=st.session_state.messages,
                    system_prompt=system_prompt,
                )

                # Stream response
                response_stream = stream_groq_response(llm, langchain_messages)
                full_response = st.write_stream(response_stream)

                # Save assistant response to state
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except (ValueError, RuntimeError) as err:
                st.error(f"Configuration Error: {err}")
            except Exception as err:  # noqa: BLE001
                st.error(f"Error calling Groq API: {err}")
