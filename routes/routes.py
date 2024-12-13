from fastapi import APIRouter, HTTPException
from services.upload_doc import save_documents,upload_doc
from services.create_doc_embedding import create_doc_embedding
from services.create_query_embedding import create_query_embedding
from services.search_embed_data import search_documents
from services.generate_response_with_llm import generate_response
from models.input_models import EmbeddingRequest, QueryRequest, AskRequest,UploadDocumentRequest

router= APIRouter()

# File to persist documents
DOCUMENTS_FILE = "documents.json"
docs = upload_doc()

@router.post("/upload_document")
def upload_document(request: UploadDocumentRequest):
    """
    API endpoint to upload documents from a request.

    Args:
        request (request: UploadDocumentRequest):The request contains the document title and content.

    Returns:
        dict: Response indicating successful document upload and document ID.
    """
    try:
        # Input validation
        documents = request.documents if isinstance(request.documents, list) else [request.documents]
        print("Documentos recibidos:", documents)
        for doc in documents:
            if not doc.title or not doc.content:
                raise HTTPException(status_code=400, detail="Each document must have a title and content.")
        print("Documentos validados correctamente")
        response = save_documents(documents)
        print("Documentos guardados correctamente")
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
        #Find document by ID to generate embeddings
        document_id = request.document_id
        matching_chunks = [doc for doc in docs if doc.get("document_id") == document_id]
        if not matching_chunks:
            raise HTTPException(status_code=404, detail="Document chunk not found")

        new_embedding_id = create_doc_embedding(document_id, matching_chunks[0])
        return {
            "message": "Embeddings generated successfully",
            "document_id": new_embedding_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")

@router.post("/search")
def search(query_request: QueryRequest):
    """
    API endpoint to search data and return results based on a query.

    Args:
        request (QueryRequest:str): The request containing the query.

    Returns:
        dict: A dictionary containing the search results.
    """
    try:
        # Input validation
        query = query_request.query
        if not query:
            raise HTTPException(status_code=400, detail="The query cannot be empty.")
        #generate query embedding
        query_embedding = create_query_embedding(query)
        #search documents based on query embedding and return results
        results = search_documents(query_embedding)
        if not results:
            raise HTTPException(status_code=404, detail="No results were found for the query.")
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error when searching: {str(e)}")

@router.post("/ask")
def ask(question_request: AskRequest):
    """
    API endpoint to ask a question.

    Args:
        request (AskRequest:str): The request containing the question.

    Returns:
        dict: A dictionary containing the answer generated with LLM, based on the most relevant content related.
    """
    #get question from the request
    question_text = question_request.question
    #create query embedding
    question_embedding = create_query_embedding(question_text)
    #search documents
    search_results = search_documents(question_embedding)

    #get most relevant content
    most_relevant_content = search_results[0]['content_snippet']

    #generate response with LLM
    response = generate_response(most_relevant_content,question_text)
    return {"answer": response}



