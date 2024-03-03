import openai
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env en el directorio actual
load_dotenv()
# Configura el cliente de OpenAI con la clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")
# Inicializa el cliente de OpenAI con la clave de API
client = openai.OpenAI(api_key=openai.api_key)

# Suponiendo que RecommendationType es una enumeración o similar
# Puedes ajustar los valores según lo que realmente contenga RecommendationType
recommendation_type_mapping = {
    "main_dish": "a main dish",
    "drink": "a drink",
    "dessert": "a dessert",
}

def get_OpenAI_suggestion(meal, recommendation_of) -> str:
    # Construye la parte de la entrada relacionada con las recomendaciones
    recommendations = ', '.join([recommendation_type_mapping[rec] for rec in recommendation_of])

    # Construye la parte de la entrada relacionada con la comida, incluyendo solo los componentes presentes
    meal_components = []
    if meal.main_dish:
        meal_components.append(f"main dish {meal.main_dish}")
    if meal.drink:
        meal_components.append(f"drink {meal.drink}")
    if meal.dessert:
        meal_components.append(f"dessert {meal.dessert}")

    meal_description = ', '.join(meal_components)

    # Crea la entrada combinando las recomendaciones con los detalles de la comida
    entry = f"I want a recommendation of {recommendations} that goes with {meal_description}"
    print("entry: ", entry)

    # Realiza la solicitud de completion de chat
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": entry,
            },
            {
                "role": "system",
                "content": "You are an intelligent assistant that gives general main course, "
                           "drink and dessert recommendations that go with the user inputed food, "
                           "drink or dessert. Only give the user a recommendation of what they "
                           "asked to be recommended. give the answer in this format: "
                           "main_dish: result, drink: result, dessert: result. if the user does NOT "
                           "ask for a certain type of recommendation, return None for that particular "
                           "recommendation that was not asked. NEVER reccomend something that is not "
                            " part of what the user wants to be recommended (instead return None for that category) " 
                            "keep the format that i mentioned ALWAYS. "
                           "if a request is out of this scope, return "
                           "None for each category."},
        ],
    )
    
    response_content = chat_completion.choices[0].message.content

    print(response_content)
    # Aquí necesitas procesar la respuesta para extraer main_dish, drink y dessert
    # Esto es un ejemplo de cómo podrías hacerlo:
    response = {
        "main_dish": None,
        "drink": None,
        "dessert": None
    }
    # Supongamos que la respuesta sigue el formato "main_dish: result, drink: result, dessert: result"
    for line in response_content.split(', '):
        if ': ' in line:
            key, value = line.split(': ')
            if key.strip() in response:  # Asegura que la clave es válida
                response[key.strip()] = value.strip() if value.strip() != "None" else ""
        else:
            print(f"Skipping invalid line: {line}")
    return response
