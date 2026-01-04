from src.llms.fromgroq import groqclient
from src.state.chainstage import orchastratorstate, workerstate,Sections
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_classic.output_parsers import PydanticOutputParser
from langgraph.types import Send
import re

class Orchestratorworker :
    def __init__(self, api_key:str, model_name:str):
        self.groq = groqclient(api_key)
        self.llm = self.groq.get_llm(model_name)
        self.parser = PydanticOutputParser(pydantic_object=Sections)

    def orchestratornode(self, state:orchastratorstate) :
        print(state)
        prompt = [
            SystemMessage(content=(
                "Generate a plan for the report given topic\n"
                "Respond with ONLY valid JSON.\n"
                "Return a JSON object that matches this structure exactly:\n"
                 "{\n"
                 '  "sections": [\n'
                 '    {\n'
                 '      "title": string,\n'
                 '      "description": string\n'
                 '    }\n'
                 '  ]\n'
                 "}\n\n"
     
                 "Rules:\n"
                 "- sections must be a non-empty list\n"
                 "- title must be short and clear\n"
                 "- description must be a brief overview of the section\n"
                 "- Do NOT add any extra keys\n"
                 "- Respond with ONLY valid JSON.\n"
            )),
            HumanMessage(content=(
                f"Here is the topic for the report : {state['topic']}"
            ))
        ]

        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        else:
            resultstr = fulltext.strip()
        print(resultstr)
        orchestrator = self.parser.parse(resultstr)

        return {"sections": orchestrator.sections}
    
    def workernode(self, state:workerstate):
        prompt = [
            SystemMessage(content= 
                "write a report section following the provider title and description.include no preamble for the each section. not more than 150 to 200 words"
            ),
            HumanMessage(content=
                f"here is the section name : {state['section'].title} and brief description of the name : {state['section'].description}"
            )
        ]
        result = self.llm.invoke(prompt)
        fulltext = result.content
        match = re.search(r"<think>\s*(.*?)\s*</think>", fulltext, flags=re.DOTALL | re.IGNORECASE)
        if match:
            think = match.group(1).strip()
            resultstr = fulltext[match.end():].strip()
        else:
            resultstr = fulltext.strip()

        return {"completed_section": [resultstr]}
    
    def assign_workers(self, state:orchastratorstate):
        return [ Send("worker", {'section': s}) for s in state["sections"]]
    
    def concludereport(self, state:orchastratorstate):
        print("concludereport")
        completed_sections = state["completed_section"]
        print(type(completed_sections))
        completed_sections_report = "\n\n------\n\n".join(completed_sections)
        return {"finalreport": completed_sections_report}

