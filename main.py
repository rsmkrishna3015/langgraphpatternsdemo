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
                        for k, v in value.items():
                          with st.chat_message("assistant"):
                            st.markdown(v)

            if usecase == "ROUTER":
                events = graph.create_routerpatter_graph(user_input.get("GROQ_API_KEY"), user_input.get("select_groq_model"))
                for event in events.stream({"input": user_message}):
                    for key, value in event.items():
                        for k, v in value.items():
                          with st.chat_message("assistant"):
                            st.markdown(v)

            if usecase == "ORCHESTRATOR-WORKER":
                events = graph.create_orchestertorworker_graph(user_input.get("GROQ_API_KEY"), user_input.get("select_groq_model"))
                for event in events.stream({"topic": user_message}):
                    if "finalreport" in event:
                        final_state = event["finalreport"]

                        if "finalreport" in final_state:
                            with st.chat_message("assistant"):
                                st.markdown(final_state["finalreport"])


        except Exception as e:
            st.error(e)

if __name__ == "__main__":
    load_langgraph_agenticai_app()