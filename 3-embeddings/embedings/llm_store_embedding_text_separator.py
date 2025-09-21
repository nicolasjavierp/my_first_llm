from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
import logging
import time
from nltk.tokenize import sent_tokenize

my_model = "deepseek-r1:1.5b"
max_token_length = 256

logging.basicConfig(level=logging.INFO)
ollama_emb = OllamaEmbeddings(model=my_model)

# Load Document
loader = TextLoader('./yoda_force.txt')
document_data = loader.load()
logging.info("Document loaded. Splitting text...")

text_splitter = CharacterTextSplitter(separator='.')
docs = text_splitter.split_documents(document_data)
logging.info(f"Split into {len(docs)}.")

# Embedding --> Embed Chunks --> Vectors --> Vector Chunks --> Save to Chroma
logging.info("Initializing Chroma vector store...")
vector_store = Chroma(collection_name="yoda_collection", embedding_function=ollama_emb, persist_directory="./yoda_db")
logging.info("Adding documents to Chroma...")
start_time = time.time()
vector_store.add_documents(documents=docs, ids=[str(i) for i in range(len(docs))])
end_time = time.time()
elapsed_time = end_time - start_time  # Calculate elapsed time
print(f"Execution time of vector_store.add_documents: {elapsed_time:.4f} seconds")
logging.info("Documents added.")

breakpoint()
# 4_ Save Embedded Documents to Chroma storeing both the embeddings and the original texts
# vector_store.persist()
# print("Documents and embeddings saved to Chroma successfully.")

#5_ Load embeddings from persistance we need to specify the embedding function VERY Important
db_load = Chroma(persist_directory="./yoda_db", embedding_function=ollama_emb)

#6_ Query the Chroma and get similarites
query = "What does this say of Quinlan Vos?" #Quinlan Vos
similar_docs = db_load.similarity_search(query)
print(similar_docs[0].page_content)

#7_ Load New Big Documnet
loader = TextLoader('./yoda_fencing.txt')
document_data = loader.load()
# Reuse text splitter
docs = text_splitter.split_documents(document_data)
#create new connection
new_db_conn = Chroma.from_documents(docs, embedding_function=ollama_emb, persist_directory="./yoda_db")

