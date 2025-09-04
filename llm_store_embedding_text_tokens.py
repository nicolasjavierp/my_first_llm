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

def calculate_optimal_chunk_size(document):
    sentences = sent_tokenize(document)
    lengths = [len(sentence) for sentence in sentences]
    mean_length = sum(lengths) / len(lengths)
    std_dev = (sum((x - mean_length) ** 2 for x in lengths) / len(lengths)) ** 0.5
    optimal_chunk_size = int(mean_length + std_dev)
    return max(optimal_chunk_size, 100)

from nltk.tokenize import sent_tokenize
from langchain_core.documents import Document
import nltk
nltk.download('punkt_tab')
# Load Document
loader = TextLoader('./yoda_force.txt')
document_data = loader.load()
logging.info("Document loaded. Splitting text...")
all_sentences = []
for doc in document_data:
    sentences = sent_tokenize(doc.page_content)
    all_sentences.extend(sentences)

docs = [Document(page_content=sentence) for sentence in all_sentences]
logging.info(f"Split into {len(docs)} sentences.")

# Embedding --> Embed Chunks --> Vectors --> Vector Chunks --> Save to Chroma
logging.info("Initializing Chroma vector store...")
vector_store = Chroma(collection_name="yoda", embedding_function=ollama_emb, persist_directory="./yoda_db")
logging.info("Adding documents to Chroma...")
start_time = time.time()  # Record the start time
vector_store.add_documents(documents=docs, ids=[str(i) for i in range(len(docs))])
end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate elapsed time
print(f"Execution time of vector_store.add_documents: {elapsed_time:.4f} seconds")
logging.info("Documents added.")
previous_len = len(docs)
breakpoint()
retriever = vector_store.as_retriever()
#6_ Query the Chroma and get similarites
query = "What makes Yoda the greatest Jedi?"
#similar_docs = vector_store.similarity_search(query)
similar_docs = retriever.get_relevant_documents(query)
print(similar_docs[0].page_content)

#7_ Load New Big Documnet
loader = TextLoader('./yoda_fencing.txt')
document_data = loader.load()
logging.info("NEW Document loaded. Splitting text...")
all_sentences = []
for doc in document_data:
    sentences = sent_tokenize(doc.page_content)
    all_sentences.extend(sentences)

docs = [Document(page_content=sentence) for sentence in all_sentences]
logging.info(f"Split into {len(docs)} sentences.")
vector_store.add_documents(documents=docs, ids=[str(i) for i in range(previous_len+1,len(docs)+previous_len+1)])

#6_ Query the Chroma and get similarites
query = "What style of lightsaber combat does Yoda use?"
similar_docs = vector_store.similarity_search(query)
print(similar_docs[0].page_content)