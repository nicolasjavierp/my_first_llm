from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv

load_dotenv("../.env")

DATA_LOCATION = f"{os.getenv('DATA_LOCATION')}"
BINARY_MODEL_LOCATION = f"{os.getenv('BINARY_MODEL_LOCATION')}"

llm = CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML", model_file = f'{BINARY_MODEL_LOCATION}llama-2-7b-chat.ggmlv3.q2_K.bin', callbacks=[StreamingStdOutCallbackHandler()])

template = """
[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Your answers are always brief.
<</SYS>>
{text}[/INST]
"""

prompt = PromptTemplate(template=template, input_variables=["text"])

sequence = prompt | llm

response = sequence.invoke("What is the meaning of life ?")

