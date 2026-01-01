from src.state.chainstage import chainstage, Routerstate
from src.nodes.promptchainnodes import PromptChainNodes
from src.nodes.Routernodes import Routernodes
from langgraph.graph import StateGraph, START, END

class graphclient():
    def __init__(self):
        pass

    def create_promptchain_graph(self, api_key:str, model_name:str) -> StateGraph[chainstage]:
        graph = StateGraph(chainstage)

        promptchainnode = PromptChainNodes(api_key=api_key, model_name=model_name)

        graph.add_node("initialstory",promptchainnode.initial_story_node)
        graph.add_node("improvedstory",promptchainnode.improved_story_node)
        graph.add_node("summarization",promptchainnode.summarization_node)

        graph.add_edge(START, "initialstory",)
        graph.add_edge("initialstory", "improvedstory")
        graph.add_edge("improvedstory", "summarization")
        graph.add_edge("summarization", END)

        return graph.compile() 
    
    def create_routerpatter_graph(self, api_key:str, model_name:str) -> StateGraph[Routerstate] :
        graph = StateGraph(Routerstate)

        routernode = Routernodes(api_key, model_name)

        graph.add_node("llm_code", routernode.llm_code)
        graph.add_node("llm_explanation", routernode.llm_explanation)
        graph.add_node("llm_interview_question", routernode.llm_interview_question)
        graph.add_node("llm_router",routernode.llm_router)

        graph.add_edge(START, "llm_router")
        graph.add_conditional_edges("llm_router", 
                                    routernode.llm_router_conditon,
                                    {
                                        "llm_code":"llm_code",
                                        "llm_explanation":"llm_explanation",
                                        "llm_interview_question":"llm_interview_question"
                                    })
        graph.add_edge("llm_code", END)
        graph.add_edge("llm_explanation", END)
        graph.add_edge("llm_interview_question", END)

        return graph.compile()
    
