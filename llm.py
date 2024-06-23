# Standard library imports
from dotenv import load_dotenv
import os

# Third-party imports
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMCustom():
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0, api_key=os.getenv('API_KEY'))
    
    def get_llm_obj(self):
        return self.llm
