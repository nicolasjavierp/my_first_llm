from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import CSVLoader
import os
from dotenv import load_dotenv

load_dotenv("../.env")

DATA_LOCATION = f"{os.getenv('DATA_LOCATION')}"

ollama_emb = OllamaEmbeddings(
    model="deepseek-r1:1.5b",
)

loader = CSVLoader(f'{DATA_LOCATION}starwars.csv')

data = loader.load()

embedded_docs = ollama_emb.embed_documents([row.page_content for row in data])

print(embedded_docs)

