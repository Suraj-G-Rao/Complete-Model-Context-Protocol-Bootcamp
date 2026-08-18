import os 
from dotenv import load_dotenv
from openai import OpenAI 

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def get_diagnosis(symptoms: list[str]) -> str:
    prompt = f"Patient has symptoms: {', '.join(symptoms)}. Suggest possible medical diagnosis.suggest me a possible cure fro the same"

    response = client.chat.completions.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


