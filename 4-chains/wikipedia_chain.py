from langchain_community.document_loaders import WikipediaLoader
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_ollama.llms import OllamaLLM


def answer_question_about(person_name, question):
    """
    Use Wikipedia Documnet Loader to help answer questions about someone,
    insert it as additional helpful context.
    """
    # Load Document
    loader = WikipediaLoader(query=person_name, load_max_docs=1)
    context_text = loader.load()[0].page_content
    #Connect to Model
    model = OllamaLLM(model="gemma2:2b")
    #Promt & Format Question
    template = "Answer this question:\n{question}\n Here is some extra context:\n{document}"
    human_prompt = HumanMessagePromptTemplate.from_template(template)
    #Chat Prompt & get result

    chat_prompt = ChatPromptTemplate.from_messages([])
    return answer