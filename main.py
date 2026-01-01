import streamlit as st

from src.ui.streamlit.loadui import loadStreamlitUi
from src.graphs.graphclients import graphclient

def load_langgraph_agenticai_app() :
    """
    Loads the streamlit app ui components
    """
    ui = loadStreamlitUi()
    user_input = ui.load_streamlit_ui()

    if not user_input :
        st.error("Failed to load user input component")
        return

    user_message = st.chat_input("Enter your message here.")

    if user_message :
        try:
            graph = graphclient()

            usecase = user_input.get("select_usecase")

            if not usecase:
                st.error("No usecase matched.")

            if usecase == "PROMPT CHAIN":
                events = graph.create_promptchain_graph(user_input.get("GROQ_API_KEY"), user_input.get("select_groq_model"))
                for event in events.stream({"topic": user_message}):
                    for key, value in event.items():
                        with st.chat_message("assistant"):
                            st.markdown(value)

            if usecase == "ROUTER":
                events = graph.create_routerpatter_graph(user_input.get("GROQ_API_KEY"), user_input.get("select_groq_model"))
                for event in events.stream({"input": user_message}):
                    for key, value in event.items():
                        with st.chat_message("assistant"):
                            st.markdown(value)


        except Exception as e:
            st.error(e)

if __name__ == "__main__":
    load_langgraph_agenticai_app()

#
#
#if __name__ == "__main__":
#    graph = graphclient()
#
#   # print(graph.create_promptchain_graph(
#   #     api_key="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",
#   #     model_name="qwen/qwen3-32b"
#   # ).invoke({"topic": "bad boy and a dog"}))
#
#    print(graph.create_routerpatter_graph(
#        api_key="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",
#        model_name="qwen/qwen3-32b"
#    ).invoke({"input": "get me sample code for java hashmap"}))