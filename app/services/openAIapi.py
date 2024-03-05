import openai
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables from a .env file in the current directory
load_dotenv()
# Set up the OpenAI client with the API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI client with the API key
client = openai.OpenAI(api_key=openai.api_key)

recommendation_type_mapping = {
    "main_dish": "a main dish",
    "drink": "a drink",
    "dessert": "a dessert",
}

def get_OpenAI_suggestion(meal, recommendation_of) -> str:
    recommendations = ', and '.join([recommendation_type_mapping[rec] for rec in recommendation_of])
    meal_components = []
    if meal.main_dish:
        meal_components.append(f"main dish {meal.main_dish}")
    if meal.drink:
        meal_components.append(f"drink {meal.drink}")
    if meal.dessert:
        meal_components.append(f"dessert {meal.dessert}")
    meal_description = ', '.join(meal_components)
    entry = f"I want a recommendation of {recommendations} that goes with {meal_description}"
    print("entry: ", entry)

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": entry,
            },
            {
                "role": "system",
                "content": "You are an intelligent assistant that provides specific recommendations for main courses, "
                           "drinks, and desserts. Always respond with a recommendation for each requested category in the format: "
                           "'main_dish: result, drink: result, dessert: result'. If a recommendation cannot be made, provide a relevant alternative instead of 'None'. "
                           "Maintain the format and ensure that all recommendations are relevant to the user's input."
            },
        ],
    )

    response_content = chat_completion.choices[0].message.content
    print(response_content)

    default_values = {
        "main_dish": meal.main_dish or "pizza",
        "drink": meal.drink or "coke",
        "dessert": meal.dessert or "chocolate cake",
    }

    response = {
        "main_dish": None,
        "drink": None,
        "dessert": None
    }

    try:
        parts = response_content.split(', ')
        for part in parts:
            if ': ' in part:
                key, value = part.split(': ', 1)
                key = key.strip()
                value = value.strip()
                if key in response:
                    response[key] = value if value.lower() != "none" else default_values[key]
            else:
                raise ValueError("Invalid format in response content")
    except ValueError as e:
        raise HTTPException(status_code=502, detail="Invalid format in response content.") from e

    return response
