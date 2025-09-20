from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import CSVLoader

ollama_emb = OllamaEmbeddings(
    model="deepseek-r1:1.5b",
)

loader = CSVLoader('./starwars.csv')

data = loader.load()

breakpoint()

embedded_docs = ollama_emb.embed_documents([row.page_content for row in data])

#embeddings = ollama_emb.embed_documents()


