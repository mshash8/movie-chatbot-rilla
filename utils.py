"""
This module provides utility functions to format chat histories and manage real-time output 
during asynchronous operations in applications that involve human-bot interactions. It is 
designed to improve user experience by structuring chat messages for better readability 
and providing visual feedback during processing delays.

Key Functions:
- `format_chat_history`: Converts a list of raw chat tuples into a formatted list of 
  HumanMessage and AIMessage objects, enhancing clarity and structure in the display of 
  chat interactions.
- `print_dots`: Provides real-time visual feedback by printing dots in the console as 
  a background thread processes tasks, useful for maintaining user engagement during 
  potentially long-running operations.

Usage:
- These functions can be integrated into chatbots or any interactive systems where users 
  engage in a dialogue with an AI, requiring clear communication and responsive feedback 
  mechanisms.
"""


# Standard library imports
from typing import List, Tuple
import time
# Third-party imports
from langchain_core.messages import AIMessage, HumanMessage


def format_chat_history(chat_history: List[Tuple[str, str]]):
    """
    Format the chat history to be more user-friendly.
    
    Parameters:
        chat_history (List[Tuple[str, str]]): The list of chat message tuples (user, bot).

    Returns:
        List[HumanMessage, AIMessage]: A list of formatted chat messages.
    """
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer
    
def print_dots(function_thread):
    # Print a dot every second while function_thread is still running
    while function_thread.is_alive():
        print(".", end="", flush=True)
        time.sleep(1)
