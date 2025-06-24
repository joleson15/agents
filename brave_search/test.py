from google import genai
from dotenv import load_dotenv
from langchain_community.tools import BraveSearch

# load_dotenv()



API_KEY = "AIzaSyDWX4Kz60IreY_z47ChwNFoRBOmlZFfqxU"

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
            You are a web-search expert that can curate a list of results based on a text query.
            Take the output from the BraveSearch tool and return a list of relevant URLs, along with a brief description of each result.
            Use the following format for your response:

            [
                {url: "https://example.com", description: "Brief description"},
                {url: "htttps://example2.com", description: "Another brief description}
                ...
            ]

            The appropriate url will be found in the output after the "link:" key, meanwhile you can provie a brief description 
            based on the content of the search result found in the "snippet:" key.
"""

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=SYSTEM_PROMPT
)
print(response.text)