"""
This module demonstrates various functionalities of a movie chatbot. It runs predefined demos
that showcase different capabilities such as handling case insensitivity, maintaining history,
and integrating user feedback into responses.

The demos section in the README provides further information on how to run this.
"""
import main
import queue

# Predefined demos with various scenarios to showcase chatbot functionalities.
demo1 = {
        'name': 'simple_demo',
        'queries': [
            'Who played in The Matrix?',
            'How many actors are there in the graph?',
            'How many people are both directors and actors of movies?',
            'Tell me more about Sleepless in Seattle'
        ]
    }

demo2 = {
        'name': 'feedback_demo',
        'queries': [
            'Tell me more about Sleepless in Seattle?',
            'feedback: Please refer to me as Mrs. Doubtfire every response',
            'Tell me more about the Polar Express'
        ]
    }

demo3 = {
        'name': 'history_demo',
        'queries': [
            'Who played in the matrix?',
            'What other movies have they been a part of?',
        ]
    }

demo4 = {
        'name': 'case_insensitive_demo',
        'queries': [
            'Who played in The Matrix?',
            'Who played in the matrix?',
        ]
    }

# main.get_chat_response()


def run_chat():
    """
    Initiates a demonstration of chatbot functionalities based on predefined queries.
    Allows the user to select a demo to see different aspects of the chatbot in action.
    """
    print("****")
    print()
    print("Welcome to the Movie Chatbot Demo! I can go through different demos which describe my functionality as a chatbot.")
    print("Feel free to ask me which demo you're interested in such as, 'feedback_demo'")
    print()
    print("****")
    print()

    chat_history = []  # Initializes chat history to store conversation.
    demo = input("Enter which demo you'd like to see - demo1, demo2, demo3 or demo4 are the options: ")
    
    selected_demo = {'demo1': demo1, 'demo2': demo2, 'demo3': demo3, 'demo4': demo4}.get(demo, demo1)
    
    for query in selected_demo['queries']:
        print("query: ", query)
        if query.startswith("feedback:"):
            chat_history.append(("user", query))
            continue
        
        # Invoke the chatbot with the current input and chat history to generate a response.
        response_q = queue.Queue()
        main.get_chat_response(query, chat_history, response_q)
        response = response_q.get()
        
        print()
        print("Bot:", response["output"])  # Display the bot's response.
        chat_history.append(("user", query))
        chat_history.append(("bot", response["output"]))
        print()
        print('To provide feedback, enter "feedback"')
        print()

if __name__ == "__main__":
    run_chat()