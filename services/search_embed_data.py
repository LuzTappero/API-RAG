from typing import List, Optional
from pydantic import BaseModel
from models.embedd_model import SearchResult
from sklearn.metrics.pairwise import cosine_similarity
import chromadb
import cohere
import os

COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

chroma_client = chromadb.Client()
collection_name = "THE_STORY_API_RAG"
collection = chroma_client.get_or_create_collection(collection_name)


def search_documents(query: str) -> Optional[List[SearchResult]]:
    try:
        # Generar el embedding para la consulta
        response = co.embed(
            texts=[query],
            model= "embed-multilingual-v3.0",
            input_type="search_document",
            embedding_types=["float"],
        )
        print(f"response del cliente de Cohere al crear embed de query: {response}")
        query_embeddings= response.embeddings.float_[0]

        # Realizar la consulta a la colección en Chroma
        results= collection.query(
            query_embeddings=[query_embeddings],
            n_results=2,
            include=['documents', 'metadatas', 'distances']
        )

        print(f"results of the colecction: {results}")
        if results:
            document_id = results['ids'][0][0]
            document_content = results['documents'][0][0]
            distance = results['distances'][0][0]

            search_result = SearchResult(
                document_id=document_id,
                content_snippet=document_content,  # Fragmento del contenido relevante
                similarity_score=distance  # Puntuación de relevancia
            )
            print(f"ID del documento: {document_id}")
            print(f"Contenido del documento: {document_content}")
            print(f"Distancia: {distance}")
            return [search_result]
        else:
            return None

    except Exception as e:
        print(f"Error al buscar en ChromaDB: {e}")
        return None