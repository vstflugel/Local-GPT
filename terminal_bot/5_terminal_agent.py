from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the AI agent with the specified model
agent = Agent(
    #model=Groq(id="llama-3.3-70b-versatile")
    model=Groq(id="deepseek-r1-distill-qwen-32b")
)

def chat_with_agent():
    print("Welcome to your terminal-based AI assistant! Type your queries below.")
    print("Type 'exit' to quit.\n")
    
    while True:
        # Take user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Generate a response from the agent
        response = agent.print_response(user_input)
        #print(f"AI: {response}")

chat_with_agent()
