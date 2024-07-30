import openai
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.environ.get('OPEN_AI_KEY')
openai.api_key = openai_api_key
def get_embedding_function():
    embeddings = OpenAIEmbeddings()
    return embeddings