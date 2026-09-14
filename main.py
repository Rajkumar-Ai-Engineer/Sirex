from dotenv import load_dotenv
from langchain_sarvam import ChatSarvam
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatSarvam()
parser = StrOutputParser()

SYSTEM_PROMPT = "You are a helpful medical assistant."

def helper(user_message: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]
    return (llm | parser).invoke(messages)
