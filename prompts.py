"""
This module defines the setup for interacting with a Neo4j graph database by providing 
predefined Cypher query templates and examples, designed for use with a language model 
that generates responses based on structured prompts. It encapsulates configurations 
for generating precise, schema-aware Cypher queries in response to natural language questions.

Key Components:
- `description_query`: A comprehensive Cypher query template for retrieving detailed 
  context about movies or persons within the graph, including their related entities.
- `prefix`, `suffix`, `examples`: These elements define the structure and examples for 
  constructing few-shot learning prompts that guide the language model to generate 
  syntactically correct and contextually appropriate Cypher queries.
- `agent_system_prompt`: Provides a detailed directive for the language model, ensuring 
  responses are consistently derived from the database and adhere to specific user queries.

Functionality:
- These configurations facilitate the creation of a knowledgeable assistant capable of 
  transforming user queries into actionable Cypher statements, and ensuring all interactions 
  are grounded in the database content.

Usage:
- The setup is ideal for applications requiring dynamic and accurate access to a graph database 
  through natural language interfaces, such as chatbots or interactive data exploration tools.
"""


description_query = """
MATCH (m:Movie|Person)
WHERE m.title CONTAINS $candidate OR m.name CONTAINS $candidate
MATCH (m)-[r:ACTED_IN|WROTE|DIRECTED|REVIEWED|PRODUCED|FOLLOWS]-(t)
WITH m, type(r) as type, collect(coalesce(t.name, t.title)) as names
WITH m, type+": "+reduce(s="", n IN names | s + n + ", ") as types
WITH m, collect(types) as contexts
WITH m, "type:" + labels(m)[0] + "\ntitle: "+ coalesce(m.title, m.name) 
       + "\nyear: "+coalesce(m.released,"") +"\n" +
       reduce(s="", c in contexts | s + substring(c, 0, size(c)-2) +"\n") as context
RETURN context LIMIT 1
"""
prefix = """
You are a Neo4j expert. Given an input question, create a syntactically correct 
Cypher query to run.\n\nHere is the schema information {schema}. Use only the provided 
relationship types and properties in the schema. Note: Do not include any explanations 
or apologies in your responses. Do not respond to any questions that might ask anything 
else than for you to construct a Cypher statement. Do not include any text except the 
generated Cypher statement. Do not use any other relationship types or properties that 
are not provided.\n\nBelow are a number of examples of questions and their corresponding 
Cypher queries.
"""

suffix = "User input: {question}\nCypher query: "

examples = [
    {
        "question": "How many artists are there?",
        "query": "MATCH (a:Person)-[:ACTED_IN]->(:Movie) RETURN count(DISTINCT a)",
    },
    {
        "question": "Which actors played in the movie Casino?",
        "query": "MATCH (m:Movie {{title: 'Casino'}})<-[:ACTED_IN]-(a) RETURN a.name",
    },
    {
        "question": "How many movies has Tom Hanks acted in?",
        "query": "MATCH (a:Person {{name: 'Tom Hanks'}})-[:ACTED_IN]->(m:Movie) RETURN count(m)",
    },
    {
        "question": "How many directors are there in the graph?",
        "query": "MATCH (a:Person)-[:DIRECTED]->(:Movie) RETURN count(DISTINCT a)",
    },
    {
        "question": "Which directors have made movies with at least three different actors named 'John'?",
        "query": "MATCH (d:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(a:Person) WHERE a.name STARTS WITH 'John' WITH d, COUNT(DISTINCT a) AS JohnsCount WHERE JohnsCount >= 3 RETURN d.name",
    },
    {
        "question": "Identify movies where directors also played a role in the film.",
        "query": "MATCH (p:Person)-[:DIRECTED]->(m:Movie), (p)-[:ACTED_IN]->(m) RETURN m.title, p.name",
    },
    {
        "question": "Find the actor with the highest number of movies in the database.",
        "query": "MATCH (a:Actor)-[:ACTED_IN]->(m:Movie) RETURN a.name, COUNT(m) AS movieCount ORDER BY movieCount DESC LIMIT 1",
    },
]

agent_system_prompt = "You are a helpful assistant that finds information about movies, actors, directors, etc., from the graph database. \
             Each user input must be processed by querying the graph database using the InformationTool. \
             Ensure each response is directly derived from the database query results. \
             Before finalizing any response, confirm a query to the database has been logged and validated. \
             If a user input does not trigger a database query, reprocess the input to include such a query. \
             Ask for clarification and provide options for further specification if tools require follow-up questions to refine the user’s request. \
             Act only on the user's specific requests and ensure compliance with the database query requirements. \
             If the specified information is not present in the database, respond with an 'I don't know because this information isn't there in the database'."
             