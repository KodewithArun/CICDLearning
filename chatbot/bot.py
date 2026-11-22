from collections.abc import Generator

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

SUPPORTED_MODELS = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "allam-2-7b",
]


def get_groq_llm(
    api_key: str,
    model_name: str = "qwen/qwen3.8-27b",
    temperature: float = 0.7,
    max_tokens: int = 500,
) -> ChatGroq:
    """Initialize and return a LangChain ChatGroq instance with token bounds."""
    if not api_key or not api_key.strip():
        raise ValueError("GROQ_API_KEY must not be empty.")

    return ChatGroq(
        groq_api_key=api_key.strip(),
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def build_langchain_messages(
    chat_history: list[dict],
    system_prompt: str | None = None,
) -> list[BaseMessage]:
    """Convert raw message dicts into LangChain message objects."""
    messages: list[BaseMessage] = []

    if system_prompt and system_prompt.strip():
        messages.append(SystemMessage(content=system_prompt.strip()))

    for msg in chat_history:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    return messages


def stream_groq_response(
    llm: ChatGroq,
    messages: list[BaseMessage],
) -> Generator[str, None, None]:
    """Stream chunks from the Groq LangChain model."""
    for chunk in llm.stream(messages):
        if chunk.content:
            yield str(chunk.content)
