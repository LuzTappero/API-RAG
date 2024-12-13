import uuid
from fastapi import HTTPException
from langchain_community.embeddings import CohereEmbeddings
import cohere
from dotenv import load_dotenv
import os
import chromadb
from services.upload_doc import upload_doc


load_dotenv()
chroma_client = chromadb.Client()

collection_name = "THE_STORY_API_RAG"
collection = chroma_client.get_or_create_collection(collection_name)

docs = upload_doc()

COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

def create_query_embedding(query: str):
    """Genera un embedding para la consulta de búsqueda."""
    try:
        query_id = "query-" + str(uuid.uuid4())
        query_embedding = co.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query",
            embedding_types=["float"],
        ).embeddings.float_[0]
        if not query_embedding:
                raise HTTPException(status_code=400, detail="Error al generar el embedding para la consulta.")

        collection.add(
            documents=[query],
            embeddings=[query_embedding],
            ids=[query_id]
            )
            # print(f"Embedding de consulta agregado con ID: {query_id}")
        return query_embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el embedding de la consulta: {str(e)}")

