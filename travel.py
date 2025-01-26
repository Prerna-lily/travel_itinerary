from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# System prompts
SYSTEM_PROMPT = """
You are an AI travel assistant. Your task is to create highly personalized travel itineraries for users based on their inputs. 
Ask clarifying questions if their inputs are incomplete or vague.
"""

# Request body model
class TravelRequest(BaseModel):
    input_text: str

# Function to generate responses
def generate_response(user_input: str) -> str:
    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    try:
        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to generate travel itinerary
@app.post("/generate-itinerary/")
def travel_planner(request: TravelRequest):
    user_input = request.input_text

    # Initial User Input
    initial_response = generate_response(user_input)

    # Refined Input Prompt
    clarification_prompt = f"""
    Based on the following user input:
    "{user_input}"
    Generate a list of clarifying questions to understand the user's travel preferences better, 
    such as dietary preferences, walking tolerance, accommodation preferences, etc.
    """
    clarification_response = generate_response(clarification_prompt)

    # Itinerary Generation Prompt
    itinerary_prompt = f"""
    Using the user's refined inputs:
    "{user_input} {clarification_response}"
    Create a detailed, day-by-day travel itinerary including activity suggestions, timings, 
    and accommodations aligned with user preferences.
    """
    itinerary_response = generate_response(itinerary_prompt)

    # Combine the outputs
    final_output = {
        "initial_response": initial_response,
        "clarifications_suggested": clarification_response,
        "final_itinerary": itinerary_response,
    }
    return final_output

# Run the app (for local testing only)
# Use `uvicorn filename:app --reload` to run
