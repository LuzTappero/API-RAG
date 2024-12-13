import chromadb
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from fastapi import FastAPI, Request
import uuid
from services.upload_doc import save_documents,upload_doc
from services.create_embedding import create_embedding
from services.create_query_embedding import create_query_embedding
from models.upload_model import UploadDocumentRequest
from models.embedd_model import EmbeddingRequest, QueryRequest, AskRequest
from services.search_embed_data import search_documents
import os
import cohere
from services.ask_request import generate_response

COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

router= APIRouter()

# Archivo para persistir documentos
DOCUMENTS_FILE = "documents.json"
docs = upload_doc()

@router.post("/upload_document")
def upload_document(request: UploadDocumentRequest):
    try:
        if not request.title or not request.content:
            raise HTTPException(status_code=400, detail="Title and content are required.")
        response = save_documents(request)
        return response
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/generate_embeddings")
def generate_embeddings(request: EmbeddingRequest):
    """
    API endpoint to generate embeddings for a specific document chunk.

    Args:
        request (EmbeddingRequest:str): The request containing the document chunk ID.

    Returns:
        dict: Message and document ID indicating successful embedding generation.
    """
    try:
        document_id = request.document_id
        matching_chunks = [doc for doc in docs if doc.get("document_id") == document_id]
        if not matching_chunks:
            raise HTTPException(status_code=404, detail="Document chunk not found")

        new_embedding_id = create_embedding(document_id)
        return {
            "message": "Embeddings generated successfully",
            "document_id": new_embedding_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")

@router.post("/search")
def search(query_request: QueryRequest):
    """
    Realiza una búsqueda en los documentos según la consulta recibida.
    """
    try:
        query = query_request.query
        if not query:
            raise HTTPException(status_code=400, detail="La consulta no puede estar vacía.")
        query_embedding = create_query_embedding(query)
        results = search_documents(query_embedding)
        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron resultados para la consulta.")
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al realizar la búsqueda: {str(e)}")

@router.post("/ask")
def ask(question_request: AskRequest):
    question_text = question_request.question
    question_embedding = create_query_embedding(question_text)
    search_results = search_documents(question_embedding)

    most_relevant_content = search_results[0]['content_snippet']

    system_prompt= """
        Tu trabajo es responder a las preguntas, con las siguientes características:
        - Responde de manera amigable y con tono entusiasta, como si le hablaras a un niño.
        - Responde en máximo 3 oraciones.
        - Agrega emojis a la respuesta.
        - Ante la misma pregunta debes responder lo más similar posible para cada interacción.
        - Responde siempre en español, sin importar en qué idioma se haga la pregunta.
        - Solo debes utilizar el contenido de las historias para responder sobre las preguntas del usuario.
        """

    response = generate_response(most_relevant_content, system_prompt,question_text)
    return {"answer": response}



