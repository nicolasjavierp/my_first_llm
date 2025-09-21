from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.document_loaders import PyPDFLoader

llm = CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML", model_file = './llama-2-7b-chat.ggmlv3.q2_K.bin', callbacks=[StreamingStdOutCallbackHandler()])

html_loader = CSVLoader("./starwars.csv")

html_data_csv = html_loader.load()

html_loader = BSHTMLLoader('view-source_https___www.starwars.com_databank_luke-skywalker.html')

data_html = html_loader.load()
 
breakpoint()

pdf_loader = PyPDFLoader('/home/nicolas.pantazis/work/LLM/my_first_llm/Star_Wars_ Dark_Forces-Guide_Walkthrough.pdf')

data_pages = pdf_loader.load()


