"""
This module integrates advanced Natural Language Processing (NLP) capabilities to interface with a Neo4j graph database, enabling the execution of structured Cypher queries and free-form natural language queries about movies and related entities. Utilizing the LangChain library, the module sets up a chatbot that handles various types of user inputs to provide detailed, context-aware information.

Components:
- Neo4jCustomGraph: Manages connections and interactions with a Neo4j graph database, ensuring efficient data retrieval and management.
- LLMCustom: A custom language model that processes and understands complex language queries, enhancing the chatbot's ability to generate accurate and relevant responses.
- InformationTool: A specific tool built on LangChain's framework that allows querying detailed information about entities like movies or actors through both structured queries and natural language inputs.
- AgentExecutor: Orchestrates the flow of data through different processing layers, from input reception to response generation, leveraging multiple custom and built-in LangChain tools.

The module demonstrates how to bind a language model with specific functionalities (tools) that enhance its capabilities, making it more suitable for specialized tasks such as answering queries about movies. It includes example setups for prompt templates and agent configurations that are tailored to improve interaction quality and reliability.
"""


# Standard library imports
from typing import Type
import threading
import queue
# Third-party imports
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chains import GraphCypherQAChain
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
# from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (ChatPromptTemplate, FewShotPromptTemplate,
                                     MessagesPlaceholder, PromptTemplate)
from langchain_core.utils.function_calling import convert_to_openai_function

# Application-specific imports
import prompts
from graph_setup import Neo4jCustomGraph
from llm import LLMCustom
import utils


# Establish a connection with the Neo4j graph
graph = Neo4jCustomGraph().get_graph_object()

# Initialize the custom language model
llm = LLMCustom().get_llm_obj()

# Define prompt templates for generating and formatting messages
example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

# Create a few-shot prompt with predefined examples for structured learning
few_shot_prompt = FewShotPromptTemplate(
    examples=prompts.examples,
    example_prompt=example_prompt,
    prefix=prompts.prefix,
    suffix=prompts.suffix,
    input_variables=["question", "schema"],
)

# Construct a chat prompt template incorporating messages and placeholders
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompts.agent_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Initialize the QA chain for handling Cypher queries using a natural language input
chain = GraphCypherQAChain.from_llm(
            graph=graph, llm=llm, cypher_prompt=few_shot_prompt, validate_cypher=True
        )

def get_information(entity: str, user_input: str) -> str:
    """
    Attempt to retrieve information about an entity using a Cypher query.
    If unsuccessful, falls back to using the QA chain to process natural language inputs.

    Parameters:
        entity (str): The entity to query information about.
        user_input (str): The natural language input from a user.

    Returns:
        str: The context information about the entity or the response from the QA chain.
    """
    try:
        data = graph.query(prompts.description_query, params={"candidate": entity})
        return data[0]["context"]
    except IndexError:
        try:
            response = chain.invoke(user_input)
        except ValueError:
            response = "I don't know the answer"
        return response

class InformationInput(BaseModel):
    """
    Data model for capturing the inputs required by the InformationTool.
    Uses Pydantic for data validation and settings management.

    Attributes:
        entity (str): The entity concerned, like a movie or person.
        user_input (str): Direct user input in natural language.
    """
    entity: str = Field(
        description="The specific entity in question, such as a 'movie' or 'person'. This field accepts both lowercase and uppercase text. The value should clearly identify a single, distinct entity to ensure accurate processing and classification."
    )
    user_input: str = Field(description="Direct user input in natural language.")

class InformationTool(BaseTool):
    """
    A tool for querying information about entities from a graph database.

    Attributes:
        name (str): Name of the tool.
        description (str): Description of the tool's functionality.
        args_schema (Type[BaseModel]): The schema for arguments this tool accepts.
    """
    name = "Information"
    description = "Tool to query information about entities like movies or people."
    args_schema: Type[BaseModel] = InformationInput

    def _run(self, entity: str, user_input: str) -> str:
        """Execute the information retrieval tool."""
        return get_information(entity, user_input=user_input)

tools = [InformationTool()]

llm_with_tools = llm.bind(functions=[convert_to_openai_function(t) for t in tools])

# Define the agent with a dictionary that transforms and processes input data
agent = (
    {
        "user_input": lambda x: x["input"],
        "input": lambda x: x["input"],
        # Processes the 'chat_history' if it exists, otherwise initializes an empty list
        "chat_history": lambda x: utils.format_chat_history(x.get("chat_history", [])),
        # Formats function call intermediate steps to be compatible with OpenAI's message format
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt  # Chains the prompt to the input processing for generating structured input
    | llm_with_tools  # Integrates language model with additional tools for processing
    | OpenAIFunctionsAgentOutputParser()  # Parses output from the language model to a usable format
)

# The executor manages the lifecycle of the agent and handles interactions with tools
agent_executor = AgentExecutor(agent=agent, tools=tools)

def get_chat_response(user_input, chat_history, response_q):
    data = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
    response_q.put(data)
    
def run_chat():
    """
    Runs the chat loop, processing user inputs and displaying responses.
    Collects feedback on the responses for improvement.
    """
    print("****")
    print()
    print("Welcome to the Movie Chatbot! I can provide information about movies and actors from my database.")
    print("Feel free to ask me questions such as, 'Who starred in Sleepless in Seattle?'")
    print()
    print("****")
    print()
    chat_history = []  # Initializes chat history to store conversation
    while True:
        user_input = input("You: ")  # Takes input from the user
        # Exit loop if user types "quit" or "exit"
        if user_input.lower() in ["quit", "exit"]:
            break
        elif user_input == "feedback":
            # Request feedback on the bot's response
            feedback = input("Was the response helpful? (yes/no): ").strip().lower()
            if feedback == "no":
                # If feedback is negative, request more details and thank the user for the feedback
                additional_feedback = input("What was wrong with the response? ")
                print("Thank you for your feedback! We will try to improve.")
                chat_history.append(("user", f"Feedback: {additional_feedback}"))
            elif feedback == "yes":
                # Positive feedback acknowledgement
                print("Glad to hear that!")
            continue
        # Invoke the agent with the current input and chat history to generate a response
        response_q = queue.Queue()
        ai_thread = threading.Thread(target=get_chat_response, args=(user_input, chat_history, response_q))
        ai_thread.start()
        
        utils.print_dots(ai_thread)
        
        ai_thread.join()
        
        response = response_q.get()
        print()
        print("Bot:", response["output"])  # Display the bot's response
        # Record user and bot messages in the chat history
        chat_history.append(("user", user_input))
        chat_history.append(("bot", response["output"]))
        print()
        print('To provide feedback, enter "feedback"')
        print()

if __name__ == "__main__":
    run_chat()
