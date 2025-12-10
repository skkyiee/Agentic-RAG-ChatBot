# Agentic RAG Chatbot with Multi-Format Support (MCP-based)

This project is an **agent-based Retrieval-Augmented Generation (RAG) chatbot** that allows users to upload documents of various formats and ask questions about their content. The architecture follows an agentic design and uses a **Model Context Protocol (MCP)** for message-based communication between agents.

## 🔗 Links

* [Architecture Diagram PDF](https://github.com/ashittis/AgenticRAGChatbot/blob/main/architrcturepdf.pdf)

## Features

* Upload documents in multiple formats: **PDF, DOCX, PPTX, TXT, CSV, MD**
* Semantic chunking and vector storage using **FAISS**
* Embedding via **HuggingFace Sentence Transformers** (`all-MiniLM-L6-v2`)
* Offline, free language model responses using **Ollama** (Gemma, Mistral, etc.)
* Modular architecture with three core agents:

  * `IngestionAgent`
  * `RetrievalAgent`
  * `LLMResponseAgent`
* Communication between agents via structured **MCP messages**
* **Streamlit-based interactive UI**

## Architecture Overview

```
User → UI (Streamlit)
        ↓
IngestionAgent → parses & chunks uploaded files
        ↓
RetrievalAgent → embeds chunks & stores in FAISS
        ↓
LLMResponseAgent → builds prompt + sends to Ollama LLM
        ↓
Streamlit → Displays response
```

### MCP Message Example

```json
{
  "type": "RETRIEVAL_RESULT",
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "trace_id": "rag-457",
  "payload": {
    "retrieved_context": ["slide 3: revenue up", "doc: Q1 summary..."],
    "query": "What KPIs were tracked in Q1?"
  }
}
```

## Tech Stack

| Component      | Tool/Library                              |
| -------------- | ----------------------------------------- |
| Language Model | Ollama (e.g., Gemma, Mistral)             |
| Embeddings     | HuggingFace Sentence Transformers         |
| Vector DB      | FAISS                                     |
| UI             | Streamlit                                 |
| File Parsing   | PyMuPDF, python-docx, python-pptx, pandas |
| Communication  | Custom MCP (Model Context Protocol)       |
| LLM Access     | OpenAI-compatible API via Ollama          |

## Installation

### Prerequisites

* Python 3.10+
* Ollama installed and running locally
* A model pulled via Ollama, for example:

  ```bash
  ollama run gemma
  ```

### Install Python Dependencies

```bash
git clone https://github.com/ashittis/AgenticRAGChatbot.git
cd AgenticRAGChatbot
python -m venv rag_env
# For Windows
rag_env\Scripts\activate
# For macOS/Linux
source rag_env/bin/activate
pip install -r requirements.txt
```

## Running the Application

Start your Ollama model:

```bash
ollama run gemma
```

Then launch the chatbot UI:

```bash
cd ui
streamlit run app.py
```

## Usage

* Upload one or more documents in supported formats.
* Wait for the system to parse and process the content.
* Ask questions about the documents.
* The answer will appear in the chat window, with **"Thinking..."** replaced upon response.

## Folder Structure

```
agentic-rag-chatbot/
├── agents/
│   ├── ingestion_agent.py
│   ├── retrieval_agent.py
│   └── llm_response_agent.py
├── core/
│   ├── mcp.py
│   └── embeddings.py
├── ui/
│   └── app.py
├── data/
├── README.md
```

## Challenges Faced

* Ensuring asynchronous behavior in Streamlit UI while maintaining stateful responses
* Handling multi-format document parsing reliably
* Maintaining model compatibility with Ollama’s local inference API
* Ensuring UI updates dynamically (e.g., replacing “Thinking…” in real-time)

## Improvements & Suggestions

* Add support for multiple concurrent documents and chunk source attribution
* Stream results live using streaming APIs from Ollama-compatible backends
* Add a `CoordinatorAgent` for managing trace and logging
* Extend to support **LangChain** or **LlamaIndex** integration in future versions

---

