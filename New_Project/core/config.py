import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_llm(model_name: str | None = None, temperature: float = 0.2):
    "Initializes and return the OpenAI Chat Model"
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the enviroment variable")
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=model_name or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        temperature=temperature,
        timeout=60,
        max_retries=2)
