from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
import os
import shutil
Data_path = "Books"

def main():
    generate_storage()

#Loads documents and chunks them
def generate_storage():
    documents = load_documents()
    chunks = chunkDocuments(documents)
    chromaDatabase(chunks)

#Loads documents
def load_documents():
    loader = DirectoryLoader(Data_path, glob="*.md")
    documents = loader.load()
    return documents
#Chunks document
def chunkDocuments(documents: list[Document]):
    documents = load_documents()
    text_chunker = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=250,
        length_function=len,
        add_start_index = True,
    )
    chunks = text_chunker.split_documents(documents)

    print(f"Split {len(documents)} document into {len(chunks)} chunks")

    #Tests that chunks actually were split
    # for i in chunks:
    #     print(i, "\n\n")

#Adds the chunked document into a chroma vector database
def chromaDatabase(chunks: list[Document]):
    Chroma_path = "chroma"

    if os.path.exists(Chroma_path):
        shutil.rmtree(Chroma_path)

    db = Chroma.from_documents(
        chunks, OllamaEmbeddings(model="nomic-embed-text"), persist_directory=Chroma_path
    )

    db.persist()
    print(f"Saved {len(chunks)} chunks to Chroma path: {Chroma_path}")

if __name__ == "__main__":
    main()

