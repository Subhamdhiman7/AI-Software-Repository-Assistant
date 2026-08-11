from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config import GOOGLE_API_KEY


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY
    )

def ask_llm(question):
    llm = get_llm()

    response = llm.invoke(question)

    # Gemini may return content as structured blocks
    if isinstance(response.content, list):
        return "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return response.content