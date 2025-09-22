from langchain_community.llms import CTransformers
from  langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from third_party.linkedin import scrape_linkedin_profile

llm = CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML", model_file = './llama-2-7b-chat.ggmlv3.q2_K.bin', callbacks=[StreamingStdOutCallbackHandler()])

template = """
given the Linkedin information {information} about a person I want you to create:
1. A Short Summary
2. Two interesting facts about tem
"""

prompt = PromptTemplate(template=template, input_variables=["text"])

sequence = prompt | llm

breakpoint()
linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/jonmoser/", mock=True)

response = sequence.invoke(input={"information": linkedin_data})

