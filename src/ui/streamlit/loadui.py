import streamlit as st
import os

from src.ui.uiconfigfile import Config

class loadStreamlitUi():
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_ui_pagetitle(), layout="wide")
        st.header(self.config.get_ui_pagetitle())

        with st.sidebar:
            usecase = self.config.get_ui_usecase()
            model = self.config.get_ui_groqmodel()

            self.user_controls["select_usecase"] = st.selectbox("selected usecase", usecase)
            self.user_controls["select_groq_model"] = st.selectbox("select groq model", model)
            self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("Groq API Key", type="password")

            if not self.user_controls["GROQ_API_KEY"]:
                st.warning("Please enter groq api key.")

        return self.user_controls
