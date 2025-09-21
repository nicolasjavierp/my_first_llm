from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama.llms import OllamaLLM
import logging
from langchain.prompts.chat import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda

logging.basicConfig(level=logging.INFO)
my_logger = logging.getLogger(__name__)

model_name = "deepseek-r1:1.5b"
my_model = OllamaLLM(model=model_name)

my_chat_model = ChatOllama(model=model_name, temperature=0)

# Select a topic of a blogpost ---> [Write the outline ---> Create blogpost from Outline] ---> Get Blogpost text

template_one = "Give me a simple bulletpoint outline for a blog post on {topic}"
prompt_one = ChatPromptTemplate.from_template(template_one)
chain_one = prompt_one | my_chat_model
# response_one = chain_one.invoke({"topic": "Star Wars"})
# my_outline = "".join([part for part in response_one.content.split('\n\n') if "**" in part])

template_two = "Write a blog post using this outline {outline}"
prompt_two = ChatPromptTemplate.from_template(template_two)
# chain_two = prompt_two | my_chat_model
# response_two = chain_two.invoke({"outline": my_outline})

def log_step1_input(x):
    my_logger.info("\n=== STEP 1: Creating outline for topic ===")
    my_logger.info(f"Topic: {x['topic']}")
    my_logger.info("Generating outline (streaming):")
    return x

def log_step1_output(x):
    my_logger.info("\n=== STEP 1 COMPLETED ===")
    my_logger.info("Outline generated successfully!")
    return x

def log_step2_input(x):
    my_logger.info("\n=== STEP 2: Writing blog post ===")
    my_logger.info("Creating blog post from outline (streaming):")
    return x

def log_step2_output(x):
    my_logger.info("\n=== STEP 2 COMPLETED ===")
    my_logger.info("Blog post generated successfully!")
    return x

full_chain = (
    RunnableLambda(log_step1_input)
    | prompt_one 
    | my_chat_model 
    | RunnableLambda(log_step1_output)
    | (lambda outline: {"outline": "".join([part for part in outline.content.split('\n\n') if "**" in part])})
    | RunnableLambda(log_step2_input)
    | prompt_two 
    | my_chat_model
    | RunnableLambda(log_step2_output)
)

streaming_handler = StreamingStdOutCallbackHandler()

response_chain = full_chain.invoke(
    {"topic": "Star Wars"}, 
    config={"callbacks": [streaming_handler]}
)