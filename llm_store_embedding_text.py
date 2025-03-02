from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import chromadb
from chromadb.config import Settings

ollama_emb = OllamaEmbeddings(
    model="deepseek-r1:1.5b",
)
#1_ Load Documnet
loader = TextLoader('./Script_E04.txt')
document_data = loader.load()
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=500)
docs = text_splitter.split_documents(document_data)

breakpoint()
#2_ Embedging --> EMbed Cunks --> Vectors
embedded_docs = ollama_emb.embed_documents([row.page_content for row in document_data])

#3_ Vector Chunks --> Save 2 Chroma
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

collection_name = "star_wars_scripts"
collection = client.create_collection(name=collection_name)

# 4. Save Embedded Documents to Chroma storeing both the embeddings and the original texts
for doc, embedding in zip(docs, embedded_docs):
    collection.add(
        documents=[doc.page_content],  # Original text
        embeddings=[embedding],        # Corresponding embedding
        metadatas=[{"source": "Script_E04.txt"}]  # Optional metadata
    )

print("Documents and embeddings saved to Chroma successfully.")

