import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_postgres import PGVector
from search import search_prompt

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

def getUserQuestion():
    return input("Qual sua pergunta? (escreva exit para sair)\n").strip()

def queryValidator(query):
    if not query:
        print("Pergunta não pode ser vazia")
        return False
    elif query.lower() == "exit":
        print("Saindo...")
        return False
 
    return True

def getQueryResults(query):
    documents = store.similarity_search_with_score(query, k=10)
    results = "\n".join([document.page_content for document, score in documents])  
    return results
 
def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    while True:
        query = getUserQuestion()
        isValidQuery = queryValidator(query)
        
        if not isValidQuery:
            return
    
        results = getQueryResults(query)
        
        
        
        result = chain.invoke({"contexto": results, "pergunta": query})
        print(result.content)

if __name__ == "__main__":
    main()