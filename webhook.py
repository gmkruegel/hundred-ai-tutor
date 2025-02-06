from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from openai.error import OpenAIError  # ✅ Corrected import for OpenAI error handling

app = FastAPI()

# ✅ Allow LearnWorlds Requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("❌ ERROR: OPENAI_API_KEY is missing!")
else:
    print(f"✅ Loaded OpenAI API Key: {openai_api_key[:5]}**********")

openai.api_key = openai_api_key

@app.post("/learnworlds-webhook")
async def chatbot(request: Request):
    data = await request.json()
    question = data.get("question", "")

    if not question:
        print("❌ Error: No question received.")
        return {"answer": "Error: No question received."}

    try:
        print(f"✅ Received question: {question}")

        # ✅ Make OpenAI API Call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )

        # ✅ Debugging: Print Full OpenAI Response
        print(f"🔹 Full OpenAI Response: {response}")

        # ✅ Extract AI Response Properly
        answer = response["choices"][0]["message"]["content"]
        print(f"✅ AI Response: {answer}")
        
        return {"answer": answer}

    except OpenAIError as e:  # ✅ Corrected OpenAI Error Handling
        print(f"❌ OpenAI API Error: {str(e)}")
        return {"answer": f"OpenAI API Error: {str(e)}"}

    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return {"answer": f"Unexpected Error: {str(e)}"}
