import openai
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env en el directorio actual
load_dotenv()
# Configura el cliente de OpenAI con la clave de API
openai.api_key = os.getenv("OPENAI_API_KEY")
# Inicializa el cliente de OpenAI con la clave de API
client = openai.OpenAI(api_key=openai.api_key)

def get_OpenAI_suggestion(entry: str) -> str:
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
                "content": "You are a helpful assistant.",
            },
        ],
    )
    
    return chat_completion.choices[0].message.content