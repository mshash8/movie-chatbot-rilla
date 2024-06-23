# Movie Chatbot Rilla

## Overview
Movie Chatbot Rilla is a sophisticated chatbot powered by Python, LangChain, Neo4j, and the GPT model from OpenAI. It's designed to answer a variety of questions related to movies, including details about actors, directors, and producers. This solution leverages the graph database capabilities of Neo4j to store and retrieve complex relationships between entities in the film industry, and integrates the conversational intelligence of GPT to provide engaging and informative responses.

## Project Structure
The project is organized as follows:
- `utils.py`: Contains helper functions that support various operations within the chatbot framework.
- `llm.py`: Defines a class that encapsulates the instantiation of the OpenAI GPT model.
- `graph_setup.py`: Contains a class for setting up and accessing the Neo4j graph database.
- `main.py`: The main executable script that runs the chatbot, orchestrating the flow of data and interactions.
- `.env`: A configuration file that stores sensitive credentials such as the Neo4j connection details and the GPT API key.
- `prompts.py`: Houses all necessary prompts, queries, and template configurations required for generating the chatbot's responses.

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
3. **Create a Virtual Environment**
   ```bash
   virtualenv chatbot
   ```
4. **Activate the Virtual Environment**
   On macOS and Linux:
  ```bash
  source chatbot/bin/activate
  ```
  On Windows:
  ```bash
  .\chatbot\Scripts\activate
  ```
5. **Install Dependencies**
  Install all required libraries using pip:
  ```bash
  pip3 install -r requirements.txt
  ```
6. **Set Up Environment Variables**
  Open the .env file and enter your GPT API key and Neo4j sandbox credentials:
  API_KEY='your_openai_api_key'
  NEO4J_URI='your_neo4j_sandbox_uri'
  NEO4J_USER='your_username'
  NEO4J_PASSWORD='your_password'
7. **Run the Chatbot**
   ```bash
   python main.py
   ```
### Usage
Once started, the chatbot will prompt you to ask questions regarding movies, actors, directors, or producers. Simply type your question to receive an informative response.

### Contributing
Contributions to Movie Chatbot Rilla are welcome! Please feel free to fork the repository, make changes, and submit pull requests. You can also open issues to discuss potential modifications or report bugs.

### License
Specify your project license here, which dictates how others can use and contribute to your code.



   
   
