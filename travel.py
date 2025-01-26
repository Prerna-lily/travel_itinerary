import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# System prompts
SYSTEM_PROMPT = """
You are an AI travel assistant. Your task is to create highly personalized travel itineraries for users based on their inputs. 
Ask clarifying questions if their inputs are incomplete or vague.
"""

# Function to generate responses
def generate_response(user_input):
    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    # OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    return response['choices'][0]['message']['content']

# Streamlit app
def main():
    st.title("AI Travel Planner")
    st.write("Provide your basic travel preferences, and I'll create a personalized travel itinerary for you!")

    # User input
    user_input = st.text_area("Enter your travel preferences (e.g., destination, dates, activities):", height=100)

    if st.button("Generate Itinerary"):
        if user_input.strip():
            with st.spinner("Generating itinerary..."):
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

                # Display results
                st.subheader("Initial Response")
                st.write(initial_response)

                st.subheader("Suggested Clarifications")
                st.write(clarification_response)

                st.subheader("Generated Itinerary")
                st.write(itinerary_response)
        else:
            st.warning("Please enter your travel preferences to generate an itinerary.")

if __name__ == "__main__":
    main()
