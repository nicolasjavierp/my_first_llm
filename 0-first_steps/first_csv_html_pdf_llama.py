from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.document_loaders import PyPDFLoader
import pprint, os
from dotenv import load_dotenv

load_dotenv("../.env")

DATA_LOCATION = f"{os.getenv('DATA_LOCATION')}"
BINARY_MODEL_LOCATION = f"{os.getenv('BINARY_MODEL_LOCATION')}"

if not os.path.exists(f'{BINARY_MODEL_LOCATION}llama-2-7b-chat.ggmlv3.q2_K.bin'):
    print(f"Error: The model file was not found at {f'{BINARY_MODEL_LOCATION}llama-2-7b-chat.ggmlv3.q2_K.bin'}.")
    print("Please make sure the file exists before running the script. You can download it here https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML")
    exit()

llm = CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML", model_file = f'{BINARY_MODEL_LOCATION}llama-2-7b-chat.ggmlv3.q2_K.bin', callbacks=[StreamingStdOutCallbackHandler()])

csv_loader = CSVLoader(f"{DATA_LOCATION}starwars.csv")

csv_data = csv_loader.load()

html_loader = BSHTMLLoader(f'{DATA_LOCATION}view-source_https___www.starwars.com_databank_luke-skywalker.html')

data_html = html_loader.load()

pdf_loader = PyPDFLoader(f'{DATA_LOCATION}Star_Wars_ Dark_Forces-Guide_Walkthrough.pdf')

data_pages = pdf_loader.load()

print("--- CSV Data ---")
for doc in csv_data[:1]:
    pprint.pprint(doc.page_content)

print("\n--- HTML Data ---")
for doc in data_html[:1]:
    pprint.pprint(doc.page_content)

print("\n--- PDF Data ---")
for doc in data_pages[:1]:
    pprint.pprint(doc.page_content)