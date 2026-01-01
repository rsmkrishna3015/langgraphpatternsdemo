from configparser import ConfigParser

class Config:
    def __init__(self, configfile="./src/ui/uiconfigfile.ini"):
        self.config = ConfigParser()
        self.config.read(configfile)

    def get_ui_pagetitle(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    
    def get_ui_usecase(self):
        return self.config["DEFAULT"].get("USECASE").split(", ")
    
    def get_ui_groqmodel(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_NAME").split(", ")