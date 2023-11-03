import json
import os
import random
import string
import time
import tiktoken

from flask import Flask, request
from flask_cors import CORS
from langchain.schema.output import LLMResult
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from sam.core.llm_models.base import LLmInputInterface
from sam.core.llm_models.llm_model_factory import build_model_factory
from sam.core.config import LLMConfig, PromptConfig
from sam.core.utils import logger


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "interference api"


@app.route("/chat/completions", methods=["POST"])
def chat_completions():
    model = request.get_json().get("model", "gpt-3.5-turbo")
    stream = request.get_json().get("stream", False)
    api_key = request.get_json().get("api_key")
    messages = request.get_json().get("messages")
    functions = request.get_json().get("functions")
    avaialable_functions = False

    if "functions" in request.get_json():
        avaialable_functions = True

    configs = LLMConfig(with_envs=True)
    provider = configs.get_providers_for_model(model, avaialable_functions)

    logger.info(provider)

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    chat_input = LLmInputInterface(
        api_key=api_key,
        model=provider.model if provider.modelPath is None else provider.modelPath,
        model_kwargs={
            "chat_format": "mistral",
        },
        n_gpu_layers=99,
        temperature=0.4,
        max_tokens=2000,
        streaming=stream,
        cache=False,
        n_ctx=8196,
    )

    prompts = [message['content'] for message in messages]
    if avaialable_functions is True:
        configs = PromptConfig()
        prompts[-1] = configs.wrap_prompt_template(prompt=prompts[-1], functions=functions)

        chat_input.grammer_path = "D:/AI/SamoCoder/test/json.gbnf"
        # chat_input.f16_kv=True

    chatProvider = build_model_factory(input=chat_input, provider_name=provider.provider)

    response = chatProvider.compelete(
        prompts=prompts)

    completion_id = "".join(random.choices(
        string.ascii_letters + string.digits, k=28))
    completion_timestamp = int(time.time())
    response_str = llm_result_to_str(response)
    inp_token = sum([num_tokens_from_string(message["content"])
                    for message in messages])
    out_token = sum([num_tokens_from_string(response_str)])
    functtion_out = None

    if avaialable_functions is True:
        from langchain.output_parsers.json import SimpleJsonOutputParser

        functtion_out = SimpleJsonOutputParser().parse(response_str)
        response_str = None


    if not stream:

        res = {
            "id": f"chatcmpl-{completion_id}",
            "object": "chat.completion",
            "created": completion_timestamp,
            "model": provider.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_str,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": inp_token,
                "completion_tokens": out_token,
                "total_tokens": inp_token + out_token,
            },
        }
        if functtion_out is not None:
            res["choices"][0]["message"]["function_call"] = functtion_out
        return res

    def streaming():
        for chunk in response:
            completion_data = {
                "id": f"chatcmpl-{completion_id}",
                "object": "chat.completion.chunk",
                "created": completion_timestamp,
                "model": provider.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "content": chunk,
                        },
                        "finish_reason": None,
                    }
                ],
            }

            content = json.dumps(completion_data, separators=(",", ":"))
            yield f"data: {content}"

            time.sleep(0.1)

        end_completion_data = {
            "id": f"chatcmpl-{completion_id}",
            "object": "chat.completion.chunk",
            "created": completion_timestamp,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop",
                }
            ],
        }
        content = json.dumps(end_completion_data, separators=(",", ":"))
        yield f"data: {content}"

    return app.response_class(streaming(), mimetype="text/event-stream")


# Get the embedding from huggingface
# def get_embedding(input_text, token):
#     huggingface_token = token
#     embedding_model = "sentence-transformers/all-mpnet-base-v2"
#     max_token_length = 500

#     # Load the tokenizer for the 'all-mpnet-base-v2' model
#     tokenizer = AutoTokenizer.from_pretrained(embedding_model)
#     # Tokenize the text and split the tokens into chunks of 500 tokens each
#     tokens = tokenizer.tokenize(input_text)
#     token_chunks = [
#         tokens[i : i + max_token_length]
#         for i in range(0, len(tokens), max_token_length)
#     ]

#     # Initialize an empty list
#     embeddings = []

#     # Create embeddings for each chunk
#     for chunk in token_chunks:
#         # Convert the chunk tokens back to text
#         chunk_text = tokenizer.convert_tokens_to_string(chunk)

#         # Use the Hugging Face API to get embeddings for the chunk
#         api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{embedding_model}"
#         headers = {"Authorization": f"Bearer {huggingface_token}"}
#         chunk_text = chunk_text.replace("
# ", " ")

#         # Make a POST request to get the chunk's embedding
#         response = requests.post(
#             api_url,
#             headers=headers,
#             json={"inputs": chunk_text, "options": {"wait_for_model": True}},
#         )

#         # Parse the response and extract the embedding
#         chunk_embedding = response.json()
#         # Append the embedding to the list
#         embeddings.append(chunk_embedding)

#     # averaging all the embeddings
#     # this isn't very effective
#     # someone a better idea?
#     num_embeddings = len(embeddings)
#     average_embedding = [sum(x) / num_embeddings for x in zip(*embeddings)]
#     embedding = average_embedding
#     return embedding


# @app.route("/embeddings", methods=["POST"])
# def embeddings():
#     input_text_list = request.get_json().get("input")
#     input_text = " ".join(map(str, input_text_list))
#     token = request.headers.get("Authorization").replace("Bearer ", "")
#     embedding = get_embedding(input_text, token)

#     return {
#         "data": [{"embedding": embedding, "index": 0, "object": "embedding"}],
#         "model": "text-embedding-ada-002",
#         "object": "list",
#         "usage": {"prompt_tokens": None, "total_tokens": None},
#     }

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def llm_result_to_str(response: LLMResult):
    final_result = ""

    for generation in response.generations:
        for item in generation:
            final_result += item.text
    return final_result


def run_api():
    app.run(host="127.0.0.1", port=8080)


run_api()
