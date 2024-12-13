from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cohere  # Asegúrate de instalar el paquete cohere
import os
import chromadb
from services.search_embed_data import search_documents
from services.create_query_embedding import create_query_embedding

COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

system_prompt = """
Tu trabajo es responder a las preguntas, con las siguientes características:
- Responde de manera amigable y con tono entusiasta, como si le hablaras a un niño.
- Responde en máximo 3 oraciones.
- Agrega emojis a la respuesta.
- Ante la misma pregunta debes responder lo más similar posible para cada interacción.
- Responde siempre en español, sin importar en qué idioma se haga la pregunta.
- Solo debes utilizar el contenido de las historias para responder sobre las preguntas del usuario.
"""

chroma_client = chromadb.Client()
collection_name = "THE_STORY_API_RAG"
collection = chroma_client.get_or_create_collection(collection_name)


def generate_response(most_relevant_content, system_prompt, question_text):
    """Genera la respuesta usando el modelo de lenguaje"""
    try:
        prompt_con_instrucciones = f"{system_prompt}\nTexto relevante: {most_relevant_content}\n\nPregunta: {question_text}"

        response = co.generate(
            model="command-r-plus-08-2024",
            prompt=prompt_con_instrucciones,
            max_tokens=100,
            temperature=0.2,
        )
        return response.generations[0].text.strip()
    except Exception as e:
            print(f"Error al generar la respuesta con Cohere: {e}")
            return "Hubo un problema al generar la respuesta. Por favor, intenta nuevamente."