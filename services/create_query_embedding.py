import uuid
from fastapi import HTTPException
import cohere
from dotenv import load_dotenv
import os
import chromadb
from services.upload_doc import upload_doc

load_dotenv()
COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

chroma_client = chromadb.Client()
collection_name = "THE_STORY_API_RAG"
collection = chroma_client.get_or_create_collection(collection_name)

docs = upload_doc()

def create_query_embedding(query: str):
    """Create embeddings for a given query."""
    try:
        query_id = "query-" + str(uuid.uuid4())
        query_embedding = co.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query",
            embedding_types=["float"],
        ).embeddings.float_[0]

        if not query_embedding:
                raise HTTPException(status_code=400, detail="Error generating the embedding for the query.")

    #Add query embedding to ChromaDB
        collection.add(
            documents=[query],
            embeddings=[query_embedding],
            ids=[query_id]
            )
        return query_embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating the embedding for the query: {str(e)}")

