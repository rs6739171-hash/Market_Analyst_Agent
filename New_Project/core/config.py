import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_llm(model_name: str = "gpt-3.5-turbo", temperature: float = 0.2):
    "Initializes and return the OpenAI Chat Model"
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the enviroment variable")
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=model_name,
        temperature=temperature)