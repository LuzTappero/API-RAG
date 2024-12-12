from fastapi import APIRouter, HTTPException
from typing import List, Dict
from fastapi import FastAPI, Request
import uuid
from services.upload_doc import save_documents,upload_doc
from services.create_embedding import create_embedding
from models.upload_model import UploadDocumentRequest
from models.embedd_model import EmbeddingRequest, SearchResult, QueryRequest, AskRequest
from services.search_embed_data import search_documents
import os
import cohere

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
        doc_id = str(uuid.uuid4())
        docs[doc_id] = {"title": request.title, "content": request.content}
        save_documents(docs)
        return {"message": "Document uploaded successfully", "document_id": doc_id}
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")

@router.post("/generate_embeddings")
def generate_embeddings(request: EmbeddingRequest):
    try:
        document_id = request.document_id
        if document_id not in docs:
            raise HTTPException(status_code=404, detail="Document not found")
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
    Busca documentos relevantes en la base de datos utilizando el embedding del query proporcionado.
    Parámetros:
    - query (str): La consulta en lenguaje natural que el usuario quiere buscar.
    Retorna:
    - results (List[SearchResult]): Una lista de documentos relevantes con su ID, título, fragmento de contenido y puntuación de similitud.
    """
    try:
        print ("entrando a search")
        query = query_request.query
        results = search_documents(query)

        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron resultados para la consulta.")

        search_results = [
            SearchResult(
                document_id=result.document_id,
                # title=result.title,
                content_snippet=result.content_snippet,
                similarity_score=result.similarity_score
            )
            for result in results
        ]

        return {"results": search_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al realizar la búsqueda: {str(e)}")



@router.post("/ask")
def ask(request: AskRequest):
    question_text = request.question

    search_results = search_documents(question_text)
    print("Resultados retornados por search_documents:", search_results)

    
    if "documents" in search_results:
        documents = search_results["documents"]
        if documents and isinstance(documents[0], list):
            relevant_doc = documents[0][0]  # Primer documento relevante
        else:
            raise ValueError("La estructura de 'documents' no es válida o está vacía")
    else:
        raise KeyError("'documents' no encontrado en los resultados")
    # Usar el contenido del documento para procesar la respuesta
    print("Documento relevante:", relevant_doc)

    instruction_prompt = """
    Tu trabajo es responder a las preguntas, con las siguientes características:
    - Responde de manera amigable y con tono entusiasta, como si le hablaras a un niño.
    - Responde en máximo 3 oraciones.
    - Agrega emojis a la respuesta.
    - Ante la misma pregunta debes responder lo más similar posible para cada interacción.
    - Responde siempre en español, sin importar en qué idioma se haga la pregunta.
    - Solo debes utilizar el contenido de las historias para responder sobre las preguntas del usuario.
    """

    formatted_prompt = f"{instruction_prompt}\nTexto relevante: {relevant_doc}\n\nPregunta: {question_text}"

    response = co.generate(
        model="command-r-plus-08-2024",
        prompt=formatted_prompt,
        max_tokens=100,
        temperature=0.2
    )
    return {"respuesta": response.generations[0].text.strip()}