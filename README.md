# Movie Chatbot Rilla

## Overview
Movie Chatbot Rilla is a chatbot powered by Python, LangChain, Neo4j, and the GPT model from OpenAI. It's designed to answer a variety of questions related to movies, including details about actors, directors, and producers. This solution leverages the graph database capabilities of Neo4j to store and retrieve complex relationships between entities like movies and persons, and integrates the conversational intelligence of GPT to provide engaging and informative responses.

## Project Structure
The project is organized as follows:
- `utils.py`: Contains helper functions that support various operations within the chatbot framework.
- `llm.py`: Defines a class that encapsulates the instantiation of the OpenAI GPT model.
- `graph_setup.py`: Contains a class for setting up and accessing the Neo4j graph database.
- `main.py`: The main executable script that runs the chatbot, orchestrating the flow of data and interactions.
- `.env`: A configuration file that stores sensitive credentials such as the Neo4j connection details and the GPT API key.
- `prompts.py`: Houses all necessary prompts, queries, and template configurations required for generating the chatbot's responses.
  
## Chatbot Architecture
### Core Components

1. **Neo4jGraph Connection**:
   - Establishes a connection to a `Neo4j` database with specific credentials. This is used to execute Cypher queries directly against your graph database.

2. **OpenAI Chat Model**:
   - Initializes an instance of `ChatOpenAI` configured to interact using OpenAI's gpt-4-0125-preview model, setting the model up with an API key and a zero temperature, ensuring deterministic outputs.

3. **FewShotPromptTemplate**:
   - Prepares a few-shot learning environment where you provide examples of how questions map to Cypher queries. This helps the model learn how to generate appropriate queries based on user input. It's especially useful for dynamically generating queries when predefined queries do not suffice.

4. **GraphCypherQAChain**:
   - A sophisticated mechanism that, upon failure of a direct database query, engages the GPT model to dynamically generate and execute a Cypher query based on user input. This is particularly helpful for handling complex queries that require an understanding beyond simple keyword matching.

5. **InformationTool**:
   - Defined as a part of your toolchain, this tool uses both the direct querying capabilities of Neo4j and the dynamic query generation of OpenAI's model to fetch information based on user queries.

6. **Agent**:
   - The Agent is essentially a configurable pipeline that processes user inputs and other relevant data to generate responses. The Agent is defined as a sequence of operations or transformations, which are applied to the state of a conversation. These transformations include extracting and formatting data, applying prompt templates, and integrating language models with other tools for advanced processing. The main purpose of the Agent is to define how the chatbot should interpret and respond to inputs based on predefined logic and dynamic data handling strategies.
  
7. **AgentExecutor**:
   - The AgentExecutor manages the lifecycle and execution of the Agent. It is responsible for invoking the Agent with the appropriate inputs and managing the interaction between the Agent and the tools it utilizes. 

### Handling Complex Queries

The `get_information` function within the chatbot is designed to manage database queries with a two-tiered approach. Initially, it tries to retrieve information using a predefined Cypher query that is specifically structured to inject recognized entities from the user's input directly into the Neo4j database. If this initial attempt returns no results, an `IndexError` is caught, triggering the function's fallback mechanism. During this fallback, the function dynamically generates a Cypher query by leveraging the `GraphCypherQAChain`. This approach is particularly effective for handling complex or abstract queries, such as "how many actors are present in the graph", which may not conform to predefined query formats. This dual approach ensures robustness and flexibility in the chatbot's ability to retrieve and provide data.


## Getting Started

### Prerequisites
To run Movie Chatbot Rilla, you will need Python 3.6 or higher. It is recommended to use a virtual environment to manage the dependencies.

### Installation

1. **Clone the Repository**
   Clone the project repository to your local machine using SSH or HTTPS:
   ```bash
   git clone <repository-url>
   ```
2. **Navigate to the Project Directory**
   ```bash
   cd movie-chatbot-rilla
   ```
3. **Install Virtualenv**
   ```bash
   pip3 install virtualenv
   ```
4. **Create a Virtual Environment**
   ```bash
   virtualenv chatbot
   ```
5. **Activate the Virtual Environment**
   
   On macOS and Linux:
   ```bash
     source chatbot/bin/activate
   ```
   
   On Windows:
   ```bash
     .\chatbot\Scripts\activate
   ```
6. **Install Dependencies**
   
   Install all required libraries using pip:
   ```bash
     pip3 install -r requirements.txt
   ```
7. **Set Up Environment Variables**
   
   Open the .env file and enter your GPT API key and Neo4j sandbox credentials:
   ``` plaintext
   API_KEY='your_openai_api_key'  
   NEO4J_URL='your_neo4j_sandbox_url'  
   NEO4J_USER='your_username'  
   NEO4J_PASSWORD='your_password'
   ```  
8. **Run the Chatbot**
   ```bash
      python main.py
   ```
9. **Deactivate the Environment**
   ```bash
   deactivate
   ```
### Usage
Once started, the chatbot will prompt you to ask questions regarding movies, actors, directors, or producers. Simply type your question to receive an informative response. The chatbot has basic memory capabilities and asks the user for feedback on the quality of the response. To exit from the chatbot, type 'quit' or 'exit'.    
Some examples of questions that can be asked include:
* Who played in the Matrix?
* How many directors are there in the database?
* Who are the actors in Sleepless in Seattle?
* Are there movies where the director is the actor of the movie?


## Limitations
- **Dynamic Query Handling**: The need to dynamically handle abstract queries provides excellent flexibility, but the solution can be brittle and inconsistent, sometimes generating imprecise Cypher statements.
- **Few-shot Prompting**: Adding several examples to the set of predefined queries (few-shot examples) can improve the robustness of the chatbot but comes at the cost of increased latency. A potential improvement could involve including only relevant examples to the query using a similarity search.
- **Error Handling and Logs**: Enhancing error handling and logging can assist in diagnosing why certain queries fail and in understanding the nature of the generated queries.
- **Performance Optimization**: Each fallback to the `GraphCypherQAChain` involves a network request to OpenAI's servers, which may introduce latency and encounter potential rate limits. Optimizing when and how often these fallbacks occur can significantly improve user experience.


## References
1. [How to best prompt for Graph-RAG](https://python.langchain.com/v0.2/docs/how_to/graph_prompting/)
2. [Semantic layer over graph database](https://python.langchain.com/v0.1/docs/use_cases/graph/semantic/)
3. [Efficient Few-Shot Prompting in LangChain: Response Caching, Prompt Templating and Prompt Serialization-Part 2](https://jayant017.medium.com/efficient-few-shot-prompting-in-langchain-part-2-265b0bc013c5)
4. [Building your own LLM RAG chatbot with Neo4j and Langchain](https://blog.futuresmart.ai/building-your-own-llm-rag-chatbot-with-neo4j-and-langchain)

## Contributing
Contributions to Movie Chatbot Rilla are welcome! Please feel free to fork the repository, make changes, and submit pull requests. You can also open issues to discuss potential modifications or report bugs.

## License
This project is open-source and follows the MIT License. You are free to use and modify the code according to the terms of the MIT License. 



   
   
