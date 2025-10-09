import json

class MCPMessage:
    def __init__(self, sender, receiver, type, trace_id, payload):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.trace_id = trace_id
        self.payload = payload

    def to_json(self):
        return json.dumps(self.__dict__)