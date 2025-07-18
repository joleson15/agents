from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv("../.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def has_model_starting_with(prefix="computer"):
    models = client.models.list().data
    return any(model.id.startswith(prefix) for model in models)

print(has_model_starting_with())