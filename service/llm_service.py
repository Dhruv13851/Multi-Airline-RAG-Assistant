from langchain_groq import ChatGroq
from config.settings import Settings


def get_llm(
    temperature: float = Settings.TEMPERATURE
):

    return ChatGroq(
        groq_api_key=Settings.GROQ_API_KEY,
        model=Settings.LLM_MODEL,
        temperature=temperature
    )