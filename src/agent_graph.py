import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Load variables from .env file into environment
load_dotenv()

# Access the API key
gemini_key = os.getenv("GEMINI_API_KEY")
