import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv

load_dotenv("../.env")

DATA_LOCATION = f"{os.getenv('DATA_LOCATION')}"

pdf_path = f"{DATA_LOCATION}HSMB_A1_first_page.pdf"
print(pdf_path)
loader = PyPDFLoader(pdf_path)

documents = loader.load()

model = OllamaLLM(model="deepseek-r1:1.5b")
for doc in documents:
    exercise_text = doc.page_content

    prompt_template = PromptTemplate(
        input_variables=["exercise_text"],
        template=(
            "I have a page of a children's exercise book containing images and text. Extract the text of the exercise."
            " I would like to modify the exercise to use the metric system instead of the imperial system. Here’s the original text:\n\n"
            "{exercise_text}\n\n"
            "Please convert the distances and adjust the language accordingly, while keeping the structure and intent of the exercise the same."
        )
    )
    chain = prompt_template | model
    modified_exercise = chain.invoke({"exercise_text": exercise_text})
    print("Modified Exercise:\n", modified_exercise)
