import uuid
from fastapi import HTTPException
from langchain_community.embeddings import CohereEmbeddings
import cohere
from dotenv import load_dotenv
import os
import chromadb
from utils.text_utils import split_into_chunks
from services.upload_doc import upload_doc
# from services.save_embedding import save_embedding

load_dotenv()
chroma_client = chromadb.Client()

collection_name = "THE_STORY_API_RAG"
collection = chroma_client.get_or_create_collection(collection_name)

docs = upload_doc()

COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

def create_embedding(document_id: str) -> str:
    """
    Creates embeddings for a given document and saves them to ChromaDB.

    Args:
        document_id (str): The ID of the document to process.

    Returns:
        str: The ID of the document after saving the embeddings.
    """
    try:
        if document_id not in docs:
            raise HTTPException(status_code=404, detail="Document not found")

        document = docs[document_id]
        content = document.get('content')
        if not content or not content.strip():
            raise HTTPException(status_code=400, detail="Document content is empty or invalid.")

        text_chunks = split_into_chunks(content)
        if not text_chunks:
            raise HTTPException(status_code=400, detail="No valid chunks to process.")

        embedding_response = co.embed(
            texts=text_chunks,
            model="embed-multilingual-v3.0",
            input_type="search_document",
            embedding_types=["float"],
        )
        embeddings = embedding_response.embeddings.float_

        if not embeddings or len(embeddings) != len(text_chunks):
            raise HTTPException(status_code=500, detail="Failed to generate embeddings or mismatch with chunks.")

        document_title = document.get('title', 'Untitled')
        documents_with_title = [
            {
                "id": f"{document_id}_{i}",
                "title": document_title,
                "content": text_chunk
            }
            for i, text_chunk in enumerate(text_chunks)
        ]

        print("Documentos con título:", documents_with_title)  # Agrega este print aquí

        ids = [f"{document_id}_{uuid.uuid4()}" for _ in range(len(text_chunks))]
        collection.add(
            documents=[doc["content"] for doc in documents_with_title],
            embeddings=embeddings,
            ids=ids,
        )
        print(f"Embeddings generated and added to collection for document ID: {collection}")

        return ids[0]  # Return the first ID as the primary identifier
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing embeddings: {str(e)}")