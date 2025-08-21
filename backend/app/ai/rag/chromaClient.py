import chromadb
from chromadb.config import Settings
from langchain_ollama import OllamaEmbeddings

from langchain_chroma import Chroma
from core.config import settings
from chromadb.api.shared_system_client import SharedSystemClient


client = chromadb.PersistentClient(path=settings.CHROMA_PATH,settings=Settings(anonymized_telemetry=False))
#
embeddings = OllamaEmbeddings(
    model=settings.EMBEDDING_MODEL,
)

# collection = client.get_or_create_collection(name="handbook")
      
hand_book_vector_store = Chroma(
    collection_name="handbook",
    persist_directory=settings.CHROMA_PATH,  # Where to save data locally, remove if not necessary
    embedding_function=embeddings,
    client=client,
    create_collection_if_not_exists=True,
)
