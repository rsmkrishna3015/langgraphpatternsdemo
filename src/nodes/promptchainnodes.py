from src.state.chainstage import chainstage
from src.llms.fromgroq import groqclient
import re


class PromptChainNodes():
    def __init__(self, api_key: str, model_name: str = None):
        self.groq = groqclient(api_key)
        self.llm = self.groq.get_llm(model_name)

    def initial_story_node(self, state: chainstage) -> str:
        prompt = f"Write an engaging short story about the topic: {state["topic"]}"
        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
    
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        return {"initial_story": resultstr}

    def improved_story_node(self, state: chainstage) -> str:
        prompt = f"Improve the following story for better engagement:\n\n{state["initial_story"]}"
        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
    
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        return {"improved_story": resultstr}

    def summarization_node(self, state: chainstage) -> str:
        prompt = f"Summarize the following story in a concise manner:\n\n{state["improved_story"]}"
        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
    
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        return {"summary": resultstr}