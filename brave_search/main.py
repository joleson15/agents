from langchain_community.tools import BraveSearch
# from langchain_community.chat_models import ChatGoogle
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

os.getenv("GOOGLE_API_KEY")
tool = BraveSearch()
# print(tool.run("What is the capital of France?"))

API_KEY = "AIzaSyDWX4Kz60IreY_z47ChwNFoRBOmlZFfqxU"
SYSTEM_PROMPT = """
            You are a web-search expert that can curate a list of results based on a text query.
            Take the context given to you and return a list of relevant URLs, along with a brief description of each result.
            Use the following format for your response:

            [
                {url: "https://example.com", description: "Brief description"},
                {url: "htttps://example2.com", description: "Another brief description}
                ...
            ]

            The appropriate url will be found in the output after the "link:" key, meanwhile you can provie a brief description 
            based on the content of the search result found in the "snippet:" key. The content will be found hereafter:

"""

model = 'gemini-2.5-flash'

content = SYSTEM_PROMPT + tool.run("What are the top 5 AI topics right now?")
# print((tool.run("What are the top 5 AI topics right now?")))
# llm = ChatGoogleGenerativeAI(model = model)
# result = llm.invoke("What are the top 5 AI topics right now?")
# print(content)

client = genai.Client(api_key = os.getenv("GOOGLE_GEMINI_API_KEY"))
response = client.models.generate_content(model=model, contents=content)
print(response.text)