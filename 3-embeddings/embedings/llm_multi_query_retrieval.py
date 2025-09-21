from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.document_loaders import WikipediaLoader
from langchain_ollama.llms import OllamaLLM
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import logging, time
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.chat_models import ChatOllama

model_name = "deepseek-r1:1.5b"
my_model = OllamaLLM(model=model_name)
max_token_length = 256

logging.basicConfig(level=logging.INFO)
ollama_emb = OllamaEmbeddings(model=model_name)


loader = WikipediaLoader(query="MKUltra")
documents = loader.load()

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=500)
splitted_docs = text_splitter.split_documents(documents)

logging.info("Initializing Chroma vector store...")
db_vector_store = Chroma(collection_name="mkultra", embedding_function=ollama_emb, persist_directory="./mkultra")
logging.info("Adding documents to Chroma...")
start_time = time.time()
db_vector_store.add_documents(documents=splitted_docs, ids=[str(i) for i in range(len(splitted_docs))])
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time of db_vector_store.add_documents: {elapsed_time:.4f} seconds")
logging.info("Documents added.")

breakpoint()

# We will use the LLM to create the multiqueries so temperature should be 0 for repeatability
my_chat_model = ChatOllama(model=model_name, temperature=0)
question = "When was this declasified?"
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=db_vector_store.as_retriever(), llm=my_model)
logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

n_relevant_docs = retriever_from_llm.get_relevant_documents(query=question)
print(n_relevant_docs[0].page_content)