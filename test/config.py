import autogen
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
import openai


openai.api_key = "sk-***"
openai.api_base = "http://localhost:1337"

config_list = [
    {
        "model": "gpt-3.5-turbo",
        'api_key': '<your OpenAI API key here>',
    }
]

def generate_llm_config(tool: BaseTool):
    function_schema = {
        "name": tool.name.lower().replace(" ", "_"),
        "description": tool.description,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        }
    }

    if tool.args is not None:
        function_schema["parameters"]["properties"] = tool.args

    return function_schema

autogen.ChatCompletion.start_logging()

# llm_config = {
#     "functions": [
#         generate_llm_config(read_file_tool),
#         generate_llm_config(circle_tool)
#     ],
#     "config_list": config_list,
#     "request_timeout": 120,
# }
