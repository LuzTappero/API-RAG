from langchain_text_splitters import RecursiveCharacterTextSplitter
import cohere
from dotenv import load_dotenv
import os
from .extract_text_from_pdf import extract_text_from_pdf

load_dotenv()

COHERE_API_KEY = os.getenv("API_KEY")

co = cohere.ClientV2(COHERE_API_KEY)

def split_into_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
    # chunk_size=2000,  # Aproximadamente 2000 caracteres
    # chunk_overlap=50  # Superposición de 50 caracteres entre los chunks
    chunk_size=800,  # Aproximadamente 2000 caracteres
    chunk_overlap=30  # Superposición de 50 caracteres entre los chunks
    )
    # historia =text
    if not text.strip():
        print("The text is empty or doesn't contain important content to split.")
        return []  # Retornar una lista vacía si el texto no es válido

    chunks = text_splitter.split_text(text)
    print("Chunks:", chunks)

    # Imprimir los resultados (solo los primeros 3 chunks como ejemplo)
    print(f"Story splited in {len(chunks)} chunks:")
    print("Generated chunks:")
    for idx, chunk in enumerate(chunks):
        print(f"Chunk {idx + 1}: {chunk[:50]}...")  # Mostrar solo los primeros 250 caracteres
    return chunks