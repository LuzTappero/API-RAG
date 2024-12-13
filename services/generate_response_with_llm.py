import cohere
import os

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
        - Si no tienes información sobre algun contenido, di 'Lo siento, no tengo información sobre eso.'
        """

def generate_response(most_relevant_content, question_text):
    """Generate the response using the language model"""
    try:
        prompt_con_instrucciones = f"{system_prompt}\nRelevant text: {most_relevant_content}\n\Question: {question_text}"

        response = co.generate(
            model="command-r-plus-08-2024",
            prompt=prompt_con_instrucciones,
            max_tokens=100,
            temperature=0.2,
        )
        return response.generations[0].text.strip()
    except Exception as e:
            print(f"Error generating response with Cohere: {e}")
            return "There was a problem generating the response. Please try again."