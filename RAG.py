from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
import argparse
from langchain_core.prompts import ChatPromptTemplate
Chroma_path = "chroma"

def main():
    #Creates CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    #Gets the database we created earlier
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=Chroma_path, embedding_function=embedding_function)
    #Gets the top 5 chunks that offer the closest answer to the question
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results) == 0: #Include, or results[0][1] < 0.6, if you want the best possible answer
        print(f"Unable to find matching results.")
        return
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:
    {context}
    
    ---
    
    Answer the question based on the above context: {question}
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOllama(model="llama3.2") 
    
    #Passes in the 5 chunks into the llama llm to give a contextual answer.
    response = model.invoke(prompt)
    response_text = response.content 

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)

if __name__ == "__main__":
    main()