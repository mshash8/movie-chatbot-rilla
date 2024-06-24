"""
This module provides a custom class for establishing and managing connections with a Neo4j graph database. It leverages the LangChain Community library to facilitate interactions with Neo4j, aiming to abstract and simplify the connection process for other components or services within an application.

The module uses environment variables to securely configure the database connection, ensuring that sensitive credentials are not hardcoded into the source code. This approach enhances security and allows for greater flexibility across different deployment environments.

Key Components:
- Neo4jCustomGraph: A class that encapsulates the logic required to connect to and interact with a Neo4j graph database. It handles connection errors gracefully and provides a method to retrieve the graph object for further operations.

Functionality:
- The module reads database connection details from environment variables, establishes a connection to a Neo4j database, and provides a method to access the connected graph instance. This setup is intended for use in applications that require graph database interactions, particularly those dealing with complex data relationships and queries.

Usage:
- This module is designed to be imported and utilized by other parts of an application that require direct interactions with a Neo4j database, offering a simplified and centralized way to manage such interactions.
"""

# Standard library imports
from dotenv import load_dotenv
import os

# Third-party imports
from langchain_community.graphs import Neo4jGraph

load_dotenv()

class Neo4jCustomGraph():
    def __init__(self):
        url = os.getenv('NEO4J_URL')
        username = os.getenv('NEO4J_USERNAME')
        password = os.getenv('NEO4J_PASSWORD')
        try:
            self.graph = Neo4jGraph(url=url, username=username, password=password)
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")

    def get_graph_object(self):
        return self.graph
