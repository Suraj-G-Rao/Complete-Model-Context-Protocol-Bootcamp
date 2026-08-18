import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following medical abstract:\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-4",  # Or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a medical research summarizer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()