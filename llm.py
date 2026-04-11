import groq
import os
from dotenv import load_dotenv
from typer import prompt

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
class LLM:
    def __init__(self):
        self.Groq_client = groq.Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def generate_response(self, prompt):
        resonse = self.Groq_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return resonse.choices[0].message.content
