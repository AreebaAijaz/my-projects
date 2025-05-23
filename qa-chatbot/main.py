import google.generativeai as genai
from dotenv import load_dotenv
import chainlit as cl
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= gemini_api_key)

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# chainlit decorator when a new session starts  
@cl.on_chat_start
async def start_chart():
    await cl.Message(content="Hello, How can I help you today?").send()  

@cl.on_message
async def handle_messsage(message:cl.Message):
    prompt = message.content
    response = model.generate_content(prompt)
    response_text = response.text if hasattr(response , 'text') else "Sorry, I couldn't generate a response."
    await cl.Message(content=response_text).send()