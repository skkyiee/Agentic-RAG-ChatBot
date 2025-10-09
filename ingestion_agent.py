import os
from core.document_parser import parse_document
from core.mcp import MCPMessage

class IngestionAgent:
    def __init__(self, send_fn):
        self.send_fn = send_fn

    def ingest(self, filepath):
        chunks = parse_document(filepath)
        message = MCPMessage(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            type="DOC_PARSED",
            trace_id="trace-001",
            payload={"chunks": chunks, "filename": os.path.basename(filepath)}
        )
        self.send_fn(message)