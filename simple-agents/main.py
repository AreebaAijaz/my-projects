import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionsModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI provider with Gemini API settings
povider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Configure the language model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash" , openai_client=povider)

# Create an greeting agent with instructions and model
agent = Agent(
    name= "Greeting Agent",
    instructions="You are a Greeting Agent, Your task is to greet the user with a friendly message, when someone says hi you've reply back with salam from areeba aijaz, if someone says bye then say allah hafiz from areeba aijaz, when someone asks other than greeting then say Areeba is here just for greeting, I can't answer anything else, sorry.",
    model = model,
)


# Define user input
user_input = input("Enter your question please!")
# Run the agent with user_input and see results.
result = Runner.run_sync(agent, user_input)
print(result.final_output)