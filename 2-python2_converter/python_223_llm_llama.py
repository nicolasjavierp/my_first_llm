from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv("../.env")

DATA_LOCATION = f"{os.getenv('DATA_LOCATION')}"
BINARY_MODEL_LOCATION = f"{os.getenv('BINARY_MODEL_LOCATION')}"

# Initialize the LLM with CTransformers
llm = CTransformers(
    model="TheBloke/Llama-2-7B-Chat-GGML", 
    model_file=f'{BINARY_MODEL_LOCATION}llama-2-7b-chat.ggmlv3.q2_K.bin', 
    callbacks=[]
)

# Define the translation prompt with explicit instructions to avoid headers and footers
prompt_template = PromptTemplate.from_template("""
You are a Python code translator. Convert the following Python 2.7 code to valid Python 3.11 code while ensuring:
1. Use the `with` statement for file handling instead of manually opening and closing files.
2. Change print statements to print functions.
3. Maintain the original logic and structure of the code.
4. Ensure proper indentation and style according to PEP 8.
5. Replace any deprecated libraries or functions with their modern equivalents.
6. Handle exceptions using the `as` keyword.
7. Use list comprehensions or generator expressions or dictionary comprehensions instead of manual loops where applicable.
8. Do not include any additional comments, headers, or footers in your output.
Original Python 2.7 code:
{code}
""")

def count_tokens(code):
    """Estimate the number of tokens in the code."""
    # Use a simple approximation: each word and punctuation mark is treated as a token
    return len(code.split())

def chunk_code(code, max_tokens=512):
    """Split the code into chunks that do not exceed the max_tokens limit."""
    tokens = code.splitlines()
    chunks = []
    current_chunk = []

    for line in tokens:
        current_chunk.append(line)
        if count_tokens('\n'.join(current_chunk)) > max_tokens:
            chunks.append('\n'.join(current_chunk[:-1]))
            current_chunk = [current_chunk[-1]]

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

# Create the LLM chain
sequence = prompt_template | llm

def convert_file(file_path):
    # Read the content of the Python 2 file
    with open(file_path, 'r') as file:
        python2_code = file.read()
    
    # Chunk the Python 2 code
    code_chunks = chunk_code(python2_code)

    # Convert the Python 2 code to Python 3
    python3_code_parts = []
    for chunk in code_chunks:
        python3_code = sequence.invoke({"code": chunk})
        python3_code_parts.append(python3_code.strip())
    
    python3_code_combined = "\n".join(python3_code_parts)

    # Write the converted code to a new Python 3 file
    new_file_path = file_path.replace('.py', '_converted.py')
    with open(new_file_path, 'w') as new_file:
        new_file.write(python3_code_combined)
    
    print(f"Converted {file_path} to {new_file_path}")

def convert_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('test.py'):
                file_path = os.path.join(dirpath, filename)
                convert_file(file_path)

# Specify the root directory containing Python 2 files
root_directory = '/home/nicolas.pantazis/work/my_first_llm/2-python2_converter'
convert_directory(root_directory)