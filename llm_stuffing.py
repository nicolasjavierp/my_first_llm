from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.summarize import load_summarize_chain
import os
from langchain.docstore.document import Document
from transformers import GPT2Tokenizer

# Initialize the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
max_tokens = 512

# Function to chunk text into pieces that fit within the token limit
def chunk_text(text, max_tokens):
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokenizer.decode(tokens[i:i + max_tokens], clean_up_tokenization_spaces=True)
        chunks.append(chunk)
    return chunks

llm = CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML", model_file = './llama-2-7b-chat.ggmlv3.q2_K.bin', callbacks=[StreamingStdOutCallbackHandler()])
docs_file_list = [file for file in os.listdir() if file.startswith("star_wars_e") and file.endswith(".txt")]

docs = []
for file in docs_file_list:
    with open(file, 'r') as f:
        content = f.read()
    for chunk in chunk_text(content, max_tokens):
        doc = Document(chunk)
        docs.append(doc)

chain = load_summarize_chain(llm, chain_type="stuff")

summaries = []
for doc in docs:
    summary = chain.invoke([doc])
    summaries.append(summary)

breakpoint()