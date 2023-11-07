import json
import autogen
from autogen import ChatCompletion
import openai

openai.api_key = "sk-xxxxxxx"

config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_base": "http://127.0.0.1:8080",
        "api_type": "open_ai",
        "api_version": None,
    }
]

# print(ChatCompletion.create(
#     config_list=config_list,
#     prompt="Hi",
# ))


def valid_json_filter(context, config, response):
    for text in autogen.Completion.extract_text(response):
        try:
            json.loads(text)
            return True
        except ValueError:
            pass
    return False


response = autogen.Completion.create(
    config_list=config_list,
    # config_list=[{"model": "text-ada-001"}, {"model": "gpt-3.5-turbo"}, {"model": "text-davinci-003"}],
    prompt="How to construct a json request to Bing API to search for 'latest AI news'? Return the JSON request",    
    filter_func=valid_json_filter,
)
