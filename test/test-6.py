# from langchain.tools.ddg_search import DuckDuckGoSearchRun
# from langchain import LLMMathChain
# from langchain.agents import initialize_agent, Tool
# from langchain.agents import AgentType
# from langchain.chat_models import google_palm

# llm = google_palm.ChatGooglePalm(google_api_key='AIzaSyBhSFGRe7cfas_cMqDWvvYHsx0NDJy9zn4')
# search = DuckDuckGoSearchRun()
# llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
# tools = [
#     Tool(
#         name = "Search",
#         func=search.run,
#         description="useful for when you need to answer questions about current events. You should ask targeted questions"
#     ),
#     Tool(
#         name="Calculator",
#         func=llm_math_chain.run,
#         description="useful for when you need to answer questions about math"
#     )
# ]

# mrkl = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

import time
from langchain.llms.llamacpp import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from sam.core.utils.utils import run_with_time

template = """Your objective is to create input in JSON format based on the provided functions schema.

Create a JSON array containing only the inputs for the functions only, name and arguments.

example output:
{{
  "name": "get_current_weather",
  "arguments": "{{ \"location\": \"Boston, MA\"}}"
}}

functions : {functions}

Only answer with the specified JSON format, no other text

{prompt}
"""

prompt_template = PromptTemplate(template=template, input_variables=["prompt", "functions"])

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="D:/AI/llama.cpp/models/openchat_3.5.Q5_K_M.gguf",
    model_kwargs={
        "chat_format": "mistral",
    },
    n_gpu_layers=99,
    grammar_path="D:/AI/SamoCoder/test/json_arr.gbnf",
    temperature=0.4,
    f16_kv=True,
    max_tokens=1000,
    n_ctx=8196,    
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)  # type: ignore

prompt = """
David Nguyen is a sophomore majoring in computer science at Stanford University. He is Asian American and has a 3.8 GPA. David is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after graduating.
"""

functions = """
[
    {
        "name": "extract_student_info",
        "description": "Get the student information from the body of the input text",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the person"
                },
                "major": {
                    "type": "string",
                    "description": "Major subject."
                },
                "school": {
                    "type": "string",
                    "description": "The university name."
                },
                "grades": {
                    "type": "integer",
                    "description": "GPA of the student."
                },
                "club": {
                    "type": "string",
                    "description": "School club for extracurricular activities. "
                }                
            }
        }
    }
]
"""


def run():
    print(llm(prompt_template.format(prompt=prompt, functions=functions)))

run_with_time(run)


time.sleep(20)

prompt = """
David Nguyen is a sophomore majoring in computer science at Stanford University. He is Asian American and has a 3.8 GPA. David is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after graduating.
"""

functions = """
[
    {
        "name": "extract_student_info",
        "description": "Get the student information from the body of the input text",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the person"
                },
                "major": {
                    "type": "string",
                    "description": "Major subject."
                },
                "school": {
                    "type": "string",
                    "description": "The university name."
                },
                "grades": {
                    "type": "integer",
                    "description": "GPA of the student."
                },
                "club": {
                    "type": "string",
                    "description": "School club for extracurricular activities. "
                }                
            }
        }
    }
]
"""

def run():
    print(llm(prompt_template.format(prompt=prompt, functions=functions)))

run_with_time(run)
