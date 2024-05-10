from pathlib import Path

from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def main():
    base_dir = Path(__file__).resolve().parent
    models_dir = base_dir / "models"
    model_path = models_dir / "llama-2-7b-chat.ggmlv3.q2_K.bin"

    llm = CTransformers(
        model="TheBloke/Llama-2-7B-Chat-GGML",
        model_file=model_path.as_posix(),
        callbacks=[StreamingStdOutCallbackHandler()]
    )

    template = """
    [INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Your answers are always brief.
    <</SYS>>
    {text}[/INST]
    """

    prompt = PromptTemplate(template=template, input_variables=["text"])
    sequence = prompt | llm
    response = sequence.invoke("What is the meaning of life ?")
    print(response)


if __name__ == "__main__":
    main()
