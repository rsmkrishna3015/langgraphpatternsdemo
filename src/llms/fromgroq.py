from langchain_groq import ChatGroq
import os

class groqclient:
    def __init__(self, api_key: str):
        os.environ["GROQ_API_KEY"] = api_key

    def get_llm(self, model_name: str = "groq-llama2-70b-chat", temperature: float = 0.7):
        return ChatGroq(
            model_name=model_name,
            temperature=temperature
        )
