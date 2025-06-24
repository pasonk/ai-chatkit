from langchain_core.documents import Document

 
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.ai.rag.chromaClient import hand_book_vector_store


result = hand_book_vector_store.similarity_search("welfare", k=5)

print(result)