
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
