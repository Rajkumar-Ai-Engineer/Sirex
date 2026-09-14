from src.utils.config_loader import load_config
import os
from dotenv import load_dotenv
from langchain_sarvam import ChatSarvam

class API_KEY_Manager:
    def __init__(self):
        try:
            load_dotenv()
            self.sarvam_api_key = os.getenv("SARVAM_API_KEY")
        except Exception as e:
            raise ValueError(f"Error loading API keys: {e}")
    
class ModelLoader:
    def __init__(self):
        try:
            self.config = load_config()
            self.api_manager = API_KEY_Manager()
            self.sarvam_api_key = self.api_manager.sarvam_api_key
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")
    def load_llm(self):
        try:
            base = self.config["llm"]["sarvam"]
            llm = ChatSarvam(api_key=self.sarvam_api_key,model=base["model"],temperature=base["temperature"],max_tokens=base["max_tokens"])
            return llm
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")
