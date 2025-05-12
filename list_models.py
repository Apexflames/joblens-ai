import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

models = openai.Model.list().data
for m in models:
    print(m.id)
