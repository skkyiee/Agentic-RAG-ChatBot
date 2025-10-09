from core.embeddings import get_embeddings
from core.vector_store import store_chunks, query_chunks
from core.mcp import MCPMessage

class RetrievalAgent:
    def __init__(self, send_fn):
        self.send_fn = send_fn

    def receive(self, message):
        if message.type == "DOC_PARSED":
            chunks = message.payload["chunks"]
            store_chunks(chunks)
        elif message.type == "QUERY":
            query = message.payload["query"]
            results = query_chunks(query)
            response = MCPMessage(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                type="RETRIEVED_CHUNKS",
                trace_id=message.trace_id,
                payload={"chunks": results, "query": query}
            )
            self.send_fn(response)