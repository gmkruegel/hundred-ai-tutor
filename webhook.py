from fastapi import FastAPI, Request
import openai
import uvicorn

app = FastAPI()

# Set your OpenAI API key here
openai.api_key = "your-openai-api-key"

@app.post("/learnworlds-webhook")
async def learnworlds_webhook(request: Request):
    data = await request.json()
    
    # Extract student question
    student_question = data.get("question", "No question provided.")

    # Send question to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are The Hundred % AI Tutor. Keep responses concise, insightful, and motivating. Align with The Hundred % brand identity."},
            {"role": "user", "content": student_question}
        ]
    )

    ai_response = response["choices"][0]["message"]["content"]

    # Return the AI-generated answer
    return {"answer": ai_response}

# Run the API server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
