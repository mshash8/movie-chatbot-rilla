"""
This module provides a simplified interface for accessing OpenAI's GPT models via the LangChain OpenAI library. It initializes a ChatOpenAI object with specific parameters to interact with OpenAI's language models, focusing on deterministic responses from GPT-4.

Key Components:
- LLMCustom: Manages the initialization and access to the GPT model using environment variables for secure API key configuration.

Functionality:
- Initializes the ChatOpenAI class with a zero temperature setting to ensure deterministic model responses and provides a method to retrieve the model object.

Usage:
- Designed for applications needing advanced NLP capabilities like chatbots or automated content generators, enabling easy integration of OpenAI’s language models.
"""

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
