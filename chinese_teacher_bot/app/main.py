from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Initialize FastAPI app
app = FastAPI(
    title="Chinese Teacher AI API",
    description="A REST API for correcting Chinese sentences with TinyLlama (Ollama).",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url=None,  # Disable ReDoc
    openapi_url="/openapi.json"  # Still need OpenAPI for Swagger
)

# Ollama API endpoint
OLLAMA_API_URL = ""

# Request body model
class UserInput(BaseModel):
    sentence: str

# Function to send messages to Ollama (TinyLlama)
def query_ollama(prompt: str):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "tinyllama",  # or whatever model you use on Ollama
        "messages": [
            {"role": "system", "content": (
                "You are a helpful, patient Mandarin Chinese teacher. "
                "Correct grammar, suggest better phrasing, and explain corrections in English. "
                "Encourage the student when they do well!"
            )},
            {"role": "user", "content": prompt}
        ],
        "stream": False  # Make sure it's false to simplify handling
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()

        # Check for different formats based on Ollama version
        if "message" in result:
            return result["message"]["content"]
        elif "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return "Unexpected response format!"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# REST endpoint: POST /correct
@app.post("/correct")
def correct_sentence(user_input: UserInput):
    """Corrects a Chinese sentence and returns an explanation."""
    sentence = user_input.sentence
    corrected = query_ollama(sentence)
    return {"input": sentence, "correction": corrected}

