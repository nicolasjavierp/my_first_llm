import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM

pdf_path = "/home/nicolas.pantazis/work/LLM/my_first_llm/HSMB_A1_first_page.pdf"
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






# # Process each page and apply the prompt
# for doc in documents:
#     text = doc.page_content  # Extract text from the document
#     # Apply the prompt
#     modified_text = llm(prompt_template.render(exercise_text=text))
#     print("Modified Exercise:\n", modified_text)


# import pdf2image
# import pytesseract
# import re, os
# import pdfplumber
# #from langchain import Document#, OpenAI, LLMChain
# from langchain_ollama import OllamaEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS


# def extract_text_from_pdf(pdf_path):
#     extracted_texts = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             if text:
#                 extracted_texts.append(text)
#     return extracted_texts


# # Step 0: Extract the text from the pdf
# pdf_path = '/home/nicolas.pantazis/work/LLM/my_first_llm/HSMB_A1_SE_M01_T02_L01.pdf'
# extracted_texts = extract_text_from_pdf(pdf_path)

# breakpoint()

# # Step 1: Convert PDF to images and extract text
# images = pdf2image.convert_from_path(pdf_path)
# extracted_texts = []

# for image in images:
#     text = pytesseract.image_to_string(image)
#     extracted_texts.append(text)

# breakpoint()


# import pdfplumber
# import os
# from PIL import Image

# def extract_text_and_images_from_pdf(pdf_path, image_save_dir):
#     extracted_texts = []
#     extracted_images = []
    
#     with pdfplumber.open(pdf_path) as pdf:
#         for i, page in enumerate(pdf.pages):
#             # Extract text
#             text = page.extract_text()
#             if text:
#                 extracted_texts.append(text)
            
#             # Extract images
#             images = page.images
#             for img_index, img in enumerate(images):
#                 # Get the image object
#                 x0, top, x1, bottom = img['x0'], img['top'], img['x1'], img['bottom']

#                 # Ensure the bounding box is within the page bounds
#                 page_bbox = page.bbox
#                 x0 = max(x0, page_bbox[0])
#                 top = max(top, page_bbox[1])
#                 x1 = min(x1, page_bbox[2])
#                 bottom = min(bottom, page_bbox[3])

#                 # Check if the bounding box is valid
#                 if x0 < x1 and top < bottom:
#                     # Crop image and save
#                     image = page.within_bbox((x0, top, x1, bottom)).to_image()
#                     img_path = os.path.join(image_save_dir, f'page_{i+1}_img_{img_index+1}.png')
#                     image.save(img_path)
#                     extracted_images.append(img_path)
#                 else:
#                     print(f"Invalid bounding box for image on page {i+1}, index {img_index+1}")

#     return extracted_texts, extracted_images

# # Step 2: Parse exercises
# image_save_dir = '/home/nicolas.pantazis/work/LLM/my_first_llm/extracted_images'
# os.makedirs(image_save_dir, exist_ok=True)
# extracted_texts, extracted_images = extract_text_and_images_from_pdf(pdf_path, image_save_dir)
# breakpoint()


# # Step 2: Parse exercises
# exercises = []
# for page_text in extracted_texts:
#     found_exercises = re.findall(r'\d+\.\s*(.*?)\n', page_text, re.DOTALL)
#     exercises.extend(found_exercises)

# # Step 3: Create Langchain Document Store
# # documents = [Document(page_content=exercise) for exercise in exercises]

# # # Step 4: Use a Text Splitter if needed
# # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# # documents = text_splitter.split_documents(documents)

# # # Step 5: Create a Vector Store for Retrieval
# # vector_store = FAISS.from_documents(documents)

# # Step 6: Define the LLM for contextualization
# # llm = OpenAI(model="text-davinci-002")  # Choose the model as needed
# # context_chain = LLMChain(llm=llm, prompt="Explain the goal and relevant concepts of the exercise: {exercise}")

# # # Step 7: Generate context for each exercise
# # for exercise in exercises:
# #     context = context_chain.run({"exercise": exercise})
# #     print(f"Exercise: {exercise}\nContext: {context}\n")