from src.state.chainstage import Routerstate, Router
from src.llms.fromgroq import groqclient
from langchain_core.messages import SystemMessage, HumanMessage
import re

class Routernodes():
    def __init__(self, api_key:str, model_name:str):
        self.groq = groqclient(api_key)
        self.llm = self.groq.get_llm(model_name)
        self.routellm = self.llm.with_structured_output(Router)

    def llm_code(self, state:Routerstate) :
        print(f"llm_code : {state}")
        prompt = f"write code for given topic: {state["input"]}"
        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
    
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        return {"output": resultstr}

    def llm_explanation(self, state:Routerstate) :
        print(f"llm_explanation : {state}")
        prompt = f"generate explanation for given topic: {state["input"]}"
        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
    
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        return {"output": resultstr}
    
    def llm_interview_question(self, state:Routerstate) :
        print(f"llm_interview_question : {state}")
        prompt = f"generate interview question for given topic: {state["input"]}"
        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
    
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        return {"output": resultstr}
    
    def llm_router(self, state:Routerstate) :
        print(f"llm_router : {state}")
        prompt = [
            SystemMessage(content="Route to code, explanation, interviewquestion based on users input"),
            HumanMessage(content=state["input"])
        ]

        result = self.routellm.invoke(prompt)
        print(f"llm_router after llm call : {result}")
        #fulltext = result.content
        #match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
    #
        #if match:
        #    think = match.group(1).strip()
        #    resultstr = fulltext[match.end():].strip()
        return {"decision": result.step}
    
    def llm_router_conditon(self, state:Routerstate):
        if state["decision"] == "code" :
            return "llm_code"
        if state["decision"] == "explanation" :
            return "llm_explanation"
        if state["decision"] == "interview_question" :
            return "llm_interview_question"
        