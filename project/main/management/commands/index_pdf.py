from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Index PDF for RAG'

    def handle(self, *args, **kwargs):
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_ollama import OllamaEmbeddings
        from langchain_community.vectorstores import FAISS

        pdf_path = os.path.join(settings.BASE_DIR, 'static', 'docs', 'ewu.pdf')
        index_path = os.path.join(settings.BASE_DIR, 'faiss_index')

        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f'PDF not found at {pdf_path}'))
            return

        self.stdout.write(f'Loading PDF from {pdf_path}...')
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        self.stdout.write(f'Loaded {len(documents)} pages.')

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        self.stdout.write(f'Created {len(chunks)} chunks. Embedding with llama3.2...')

        embeddings = OllamaEmbeddings(model="llama3.2")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(index_path)

        self.stdout.write(self.style.SUCCESS(f'Done! Index saved to {index_path}'))