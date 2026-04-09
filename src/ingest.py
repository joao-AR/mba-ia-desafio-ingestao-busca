import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector 
from dotenv import load_dotenv
load_dotenv()

PDF_PATH =  os.getenv("PDF_PATH")

def ingest_pdf():
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    
    enriched = [
       Document(
            page_content=document.page_content,
            metadata={key : value for key, value in document.metadata.items() if value not in ("", None)}
        )
        for document in chunks
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        model=os.getenv("GOOGLE_EMBEDDING_MODEL")
    )
    
    store = PGVector(embeddings=embeddings, 
                 collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"), 
                 connection=os.getenv("DATABASE_URL"),
                 use_jsonb=True)
    
    store.add_documents(documents=enriched,ids=ids)
    return

if __name__ == "__main__":
    for k in ("GOOGLE_EMBEDDING_MODEL","GOOGLE_API_KEY","DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} not set")
        
    ingest_pdf()