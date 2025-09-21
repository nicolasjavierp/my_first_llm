from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import OllamaEmbeddings

ollama_emb = OllamaEmbeddings(
    model="deepseek-r1:1.5b",
)

with open('./star_wars_e_6.txt') as file:
    e6_text = file.read()

embeddings = ollama_emb.embed_documents(e6_text)

breakpoint()


