import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_postgres import PGVector
from search import search_prompt
import sys

from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    model=os.getenv("GOOGLE_EMBEDDING_MODEL")
)

store = PGVector(embeddings=embeddings, 
                collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"), 
                connection=os.getenv("DATABASE_URL"),
                use_jsonb=True)


def main():
    
    query = input("Whats is your question?")

    # Verifica se não está vazia
    if query.strip():
        results = store.similarity_search_with_score(query, k=4)
    
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    result = chain.invoke({"contexto": results, "pergunta": query})
    
    print(result.content)

if __name__ == "__main__":
    main()