from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

# Send message
response = llm.invoke("CAN YOU EXPLAIN ABOUT THE KRISHNAVATHAR MOVIE")

# Print response
print("\nLLM Response:\n")
print(response.content)