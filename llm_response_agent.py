import openai
from core.mcp import MCPMessage

openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"


class LLMResponseAgent:
    def __init__(self, callback=None):
        self.callback = callback  # UI function to show response

    def receive(self, message):
        context = "\n".join(message.payload["chunks"])
        query = message.payload["query"]
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

        response = openai.ChatCompletion.create(
            model="gemma3",  # or "mistral", "phi3", etc.
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        answer = response["choices"][0]["message"]["content"]

        if self.callback:
            self.callback(answer)
        else:
            print("Answer:", answer)
