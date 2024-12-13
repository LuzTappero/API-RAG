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

docs= upload_doc()

def create_embedding(document_id: str) -> str:
    """
    Creates embeddings for a given document and saves them to ChromaDB.

    Args:
        document_id (str): The ID of the document to process.

    Returns:
        str: The ID of the document after saving the embeddings.
    """
    try:
        matching_chunks = [doc for doc in docs if doc["document_id"] == document_id]
        if not matching_chunks:
            raise HTTPException(status_code=404, detail="Document chunk not found")

        document = matching_chunks[0]
        content = document.get("content")
        if not content or not content.strip():
            raise HTTPException(status_code=400, detail="Document chunk content is empty or invalid.")

        embedding_response = co.embed(
            texts=[content],
            model="embed-multilingual-v3.0",
            input_type="search_document",
            embedding_types=["float"],
        )
        embeddings = embedding_response.embeddings.float_

        if not embeddings or len(embeddings) != 1:
            raise HTTPException(status_code=500, detail="Failed to generate embeddings for the document chunk.")

        collection.add(
            documents=[content],
            embeddings=embeddings,
            ids=[document_id]
        )
        print(f"Embedding generated and added to collection for document chunk ID: {document_id}")

        return document_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing embeddings: {str(e)}")