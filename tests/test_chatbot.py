import os

import os

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import pytest

from chatbot.bot import (
    SUPPORTED_MODELS,
    build_langchain_messages,
    get_groq_llm,
)


def test_supported_models():
    assert "qwen/qwen3.8-27b" in SUPPORTED_MODELS
    assert len(SUPPORTED_MODELS) >= 3


def test_build_langchain_messages_with_system_prompt():
    raw_history = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help?"},
        {"role": "user", "content": "What is Python?"},
    ]
    system_prompt = "You are a Python expert."

    messages = build_langchain_messages(raw_history, system_prompt=system_prompt)

    assert len(messages) == 4
    assert isinstance(messages[0], SystemMessage)
    assert messages[0].content == "You are a Python expert."
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == "Hello!"
    assert isinstance(messages[2], AIMessage)
    assert messages[2].content == "Hi there! How can I help?"
    assert isinstance(messages[3], HumanMessage)
    assert messages[3].content == "What is Python?"


def test_build_langchain_messages_empty_history():
    messages = build_langchain_messages([], system_prompt=None)
    assert messages == []


def test_get_groq_llm_empty_key():
    with pytest.raises(ValueError, match="GROQ_API_KEY must not be empty"):
        get_groq_llm(api_key="")


def test_get_groq_llm_valid_instance():
    llm = get_groq_llm(
        api_key="gsk_test_fake_api_key_12345",
        model_name="qwen/qwen3.8-27b",
        temperature=0.7,
        max_tokens=250,
    )
    assert llm.model_name == "qwen/qwen3.8-27b"
    assert llm.temperature == 0.7
    assert llm.max_tokens == 250


@pytest.mark.skipif(not os.getenv("GROQ_API_KEY"), reason="GROQ_API_KEY not set")
def test_groq_api_live_smoke():
    """Live smoke test that runs in CI when secrets.GROQ_API_KEY is provided."""
    api_key = os.getenv("GROQ_API_KEY")
    llm = get_groq_llm(
        api_key=api_key,
        model_name="qwen/qwen3.8-27b",
        max_tokens=100,
    )
    messages = build_langchain_messages([{"role": "user", "content": "Ping"}])
    response = llm.invoke(messages)
    assert response.content is not None
    assert len(str(response.content)) > 0
