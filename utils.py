# Standard library imports
from typing import List, Tuple

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
    