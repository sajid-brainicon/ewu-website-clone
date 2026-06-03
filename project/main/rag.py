import os
from django.conf import settings

_vectorstore = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        from langchain_ollama import OllamaEmbeddings
        from langchain_community.vectorstores import FAISS

        index_path = os.path.join(settings.BASE_DIR, 'faiss_index')

        if not os.path.exists(index_path):
            print(f"FAISS index not found at {index_path}")
            return None

        print(f"Loading FAISS index from {index_path}")
        embeddings = OllamaEmbeddings(model="llama3.2")
        _vectorstore = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("FAISS index loaded successfully")
    return _vectorstore


def get_relevant_context(question, k=4):
    try:
        vectorstore = get_vectorstore()
        if vectorstore is None:
            print("No vectorstore available")
            return ""
        docs = vectorstore.similarity_search(question, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        print(f"Found {len(docs)} relevant chunks")
        return context
    except Exception as e:
        print(f"RAG ERROR: {e}")
        return ""