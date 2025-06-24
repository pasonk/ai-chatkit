from langchain_core.documents import Document


# backend env root dir
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.ai.rag.chromaClient import hand_book_vector_store, client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader



# client.delete_collection("handbook")

client.get_or_create_collection("handbook")

# with open("./resource/EmployeeHandbook.pdf", "r", encoding="utf-8") as f:
#     text = f.read()

documents = []
loader = PyPDFLoader("./resource/EmployeeHandbook.pdf")
documents.extend(loader.load())


text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
# docs = text_splitter.create_documents([text])
docs = text_splitter.split_documents(documents)



hand_book_vector_store.add_documents(docs)

result = hand_book_vector_store.similarity_search("vacation", k=5)

print(result)