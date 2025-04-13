import os
import google.generativeai as genai
import chainlit as cl
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

# Load environment variables from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

@cl.oauth_callback
def oauth_callback(
    provider_id : str,
    token : str,
    raw_user_data : Dict[str , str],
    default_user : cl.User,
) -> Optional[cl.User]:

    """
    Handle the pauth callback from github
    Return a user object if authenctication is successful, else none.
    """


    print(f"Provider: {provider_id}")
    print(f"User Data: {raw_user_data}")

    return default_user  # Return the default user object

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])   # Initialize chat history
    await cl.Message(content="Hello, How can I assist you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")  # Get chat history from session

    history.append(
        {"role": "user", "content": message.content}
    )  # Add user message to history

    # Format chat history for Gemini model
    formatted_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"  # Determine message role
        formatted_history.append(
            {"role": role, "parts": [{"text": msg["content"]}]}
        )  # Format message

    response = model.generate_content(formatted_history)  # Get response from Gemini

    response_text = (
        response.text if hasattr(response, "text") else ""
    )  # Extract response text safely

    history.append(
        {"role": "assistant", "content": response_text}
    )  # Add assistant response to history
    cl.user_session.set("history", history)  # Update session history

    await cl.Message(content=response_text).send()  # Send response to user