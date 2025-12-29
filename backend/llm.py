from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# Chat history to maintain memory (in-session)
chat_history = []

# System prompt template with emotion context
system_prompt = (
    "You are a friendly, emotionally intelligent assistant. "
    "The user is feeling {emotion}. Keep that in mind while answering.\n"
)

# ChatPromptTemplate is defined but not used here — optional unless you use LangChain Chains
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# Function to get chatbot's response
def get_chatbot_response(user_input: str, emotion: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt.format(emotion=emotion)},
        *chat_history,
        {"role": "user", "content": user_input}
    ]

    # Invoke Gemini model with message history
    response = llm.invoke(messages)

    # Update chat history
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response.content))

    return response.content
