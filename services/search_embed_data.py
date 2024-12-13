from typing import List
from fastapi import HTTPException
import chromadb
import cohere
import os

COHERE_API_KEY = os.getenv("API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

chroma_client = chromadb.Client()
collection_name = "THE_STORY_API_RAG"
collection = chroma_client.get_or_create_collection(collection_name)

def search_documents(query_embeddings: List[float], top_n: int = 2):
    """Find relevant documents based on query embeddings."""
    try:
        # Realizar la consulta a la colección en Chroma
        results= collection.query(
            query_embeddings=[query_embeddings],
            n_results=top_n,
            include=['documents', 'distances']
        )

        if not results.get('documents'):
            raise HTTPException(status_code=404, detail="No results were found for the query.")

        search_results = []
    # Iterate over the results and extract relevant information
        for i in range(len(results['documents'])):
            document = results['documents'][i]
            distance = results['distances'][i]
            content_snippet = document[:200]
        # Append the search result to the list
            search_results.append({
                "document_id":  results['ids'][i],
                "content_snippet": content_snippet,
                "similarity_score": distance[1]
            })
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")