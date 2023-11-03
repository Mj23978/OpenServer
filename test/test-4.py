from langchain.llms.llamacpp import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from sam.core.utils.utils import run_with_time

template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="D:/AI/llama.cpp/models/dolphin-2.1-mistral-7b.Q5_K_M.gguf",
    model_kwargs={
        "chat_format": "mistral",
    },
    n_gpu_layers=99,
    temperature=0.4,
    max_tokens=2000,
    top_p=0.95,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)  # type: ignore

prompt = """
Question: A rap battle between Stephen Colbert and John Oliver
"""

def run():
    print(llm(prompt))

run_with_time(run)
