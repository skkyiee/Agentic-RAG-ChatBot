import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from core.mcp import MCPMessage


st.title("📚 Multi-Format Agentic RAG Chatbot (with Ollama)")


# Callback to update Streamlit UI with model response
def display_answer(answer):
    st.chat_message("assistant").markdown(answer)
    st.session_state.history[-1]["bot"] = answer


# Init agents
response_agent = LLMResponseAgent(callback=display_answer)
retriever = RetrievalAgent(lambda msg: response_agent.receive(msg))
ingester = IngestionAgent(lambda msg: retriever.receive(msg))

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Render chat messages
for msg in st.session_state.history:
    st.chat_message("user").markdown(msg["user"])
    st.chat_message("assistant").markdown(msg["bot"])

# File uploader
uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, PPTX, CSV, TXT, MD)",
    type=["pdf", "docx", "pptx", "csv", "txt", "md"],
)
if uploaded_file:
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    ingester.ingest(file_path)

# Chat input
query = st.chat_input("Ask a question")
if query:
    st.session_state.history.append({"user": query, "bot": "Thinking..."})
    message = MCPMessage(
        sender="UI",
        receiver="RetrievalAgent",
        type="QUERY",
        trace_id="trace-002",
        payload={"query": query},
    )
    retriever.receive(message)
