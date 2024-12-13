from uuid import uuid4
from fastapi import HTTPException
import json
from typing import List, Dict
from models.input_models import UploadDocumentRequest, Document
from utils.split_into_chunks import split_into_chunks
import os

# Archivo para persistir documentos
DOCUMENTS_FILE = "documents.json"

def upload_doc() -> Dict:
    """Load documents from a JSON file to persist."""
    if not os.path.exists(DOCUMENTS_FILE):
        raise HTTPException(status_code=404, detail=f"The file {DOCUMENTS_FILE} does not exist.")
    try:
        with open(DOCUMENTS_FILE, "r") as file:
            data= json.load(file)
            if not isinstance(data, list):
                raise ValueError("The file does not contain a valid list of documents.")
            return data
    except json.JSONDecodeError:
        print("The file is empty or contains invalid JSON. Returning an empty list.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading documents: {str(e)}")
        return []


# Guardar documentos en un archivo local
def save_documents(documents: List[Document]):
    """Save documents from the request to a JSON file to persist."""
    # Input validation
    if not isinstance(documents, list):
        raise ValueError("Invalid document format. Expected an UploadDocumentRequest object.")
    for document in documents:
        if not isinstance(document, Document):
            raise ValueError("Invalid document format. Expected a list of Document objects.")
        if not document.title:
            raise ValueError("The document title cannot be empty.")
        if not document.content:
            raise ValueError("The document content cannot be empty.")

    try:
        # Split document into chunks before saving
        chunks=[]
        for document in documents:
            chunks.extend(split_into_chunks(document.content))

        if not chunks:
            raise ValueError("No chunks generated from the document content.")
        ids= []
        new_chunks=[]
        saved_chunks = upload_doc()

        if os.path.exists(DOCUMENTS_FILE):
            with open(DOCUMENTS_FILE, "r") as file:
                try:
                    saved_chunks = json.load(file)
                except json.JSONDecodeError:
                    saved_chunks = []
        else:
            saved_chunks = []
        for document in documents:
            for chunk in chunks:
                document_id = str(uuid4())
                chunk_document  = {
                    "document_id": document_id,
                    "title": document.title,
                    "content": chunk,
                }
            # Append the document to the list
            new_chunks.append(chunk_document)
            ids.append(document_id)
        saved_chunks.extend(new_chunks)
        # Save the updated list to the file
        with open(DOCUMENTS_FILE, "w") as file:
            json.dump(saved_chunks, file, indent=4)
        return {
            "message": "Document successfully uploaded",
            "document_id": ids[0],
        }
    except Exception as e:
        raise RuntimeError(f"An error occurred while saving the document: {str(e)}")
