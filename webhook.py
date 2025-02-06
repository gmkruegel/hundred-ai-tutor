from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# ✅ Allow requests from anywhere (or specify LearnWorlds domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to LearnWorlds domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/learnworlds-webhook")
async def chatbot(request: Request):
    data = await request.json()
    question = data.get("question", "")

    if not question:
        return {"answer": "I couldn't process that."}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )
        answer = response["choices"][0]["message"]["content"]
        return {"answer": answer}

    except Exception as e:
        return {"answer": "Sorry, I couldn't process that."}
