import json
import random
import string
import time

import tiktoken
from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema.output import LLMResult
from sam.core.config.vector_config import VectorDBConfig

from sam.core.llm_models.base import LLmInputInterface
from sam.core.llm_models.llm_model_factory import LLMFactory
from sam.core.config import LLMConfig, PromptConfig
from sam.core.utils import logger
from sam.core.vector_store.vector_factory import VectorFactory


app = Flask(__name__)
CORS(app)

llamacpp_server = None


@app.route("/")
def index():
    return "interference api"


@app.route("/hello/<name>")
def hello(name):
    return f"Hello {name}"

@app.route("/chat/completions", methods=["POST"])
def chat_completions():
    try:
        model = request.get_json().get("model", "gpt-3.5-turbo")
        stream = request.get_json().get("stream", False)
        api_key = request.get_json().get("api_key")
        messages = request.get_json().get("messages")
        functions = request.get_json().get("functions")
        n_gpu_layers= request.get_json().get("n_gpu_layers", 99)
        temperature= request.get_json().get("temperature", 0.4)
        max_tokens= request.get_json().get("max_tokens", 1000)
        top_p= request.get_json().get("top_p", 1)
        cache= request.get_json().get("cache", False)
        n_ctx= request.get_json().get("n_ctx", 8196)

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
            streaming=stream,
            n_gpu_layers=n_gpu_layers,
            temperature=temperature,
            max_tokens=max_tokens,     
            top_p=top_p,   
            cache=cache,
            n_ctx=n_ctx,
        )

        prompts = [message['content'] for message in messages]
        if avaialable_functions is True:
            configs = PromptConfig()
            prompts[-1] = configs.prompt_template().format(prompt=prompts[-1], functions=functions)

            chat_input.grammer_path = "D:/AI/SamoCoder/test/json.gbnf"
            chat_input.f16_kv=True

        chatProvider = LLMFactory.get_model(input=chat_input, provider_name=provider.provider)
        response = chatProvider.compelete(
            prompts=prompts)

        completion_id = "".join(random.choices(
            string.ascii_letters + string.digits, k=28))
        completion_timestamp = int(time.time())
        response_str = llm_result_to_str(response)
        inp_token = num_tokens_from_string("".join(prompts))
        out_token = num_tokens_from_string(response_str)
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route("/embeddings", methods=["POST"])
def embeddings():
    try: 
        input_text_list = request.get_json().get("input")
        model = request.get_json().get("model", "bge-small")
        api_key = request.get_json().get("api_key", None)

        configs = VectorDBConfig(with_envs=False)
        provider = configs.get_embeddings(model)

        logger.info(provider)

        embeddingProvider = VectorFactory.get_embeddings(type=provider, model=model, api_key=api_key)
        inp_token = num_tokens_from_string("".join(input_text_list))
        
        resp = []
        if isinstance(input_text_list, str):            
            resp.append(embeddingProvider.get_embedding(input_text_list))
        else:
            for text in input_text_list:
                resp.append(embeddingProvider.get_embedding(text))

        logger.info(resp) 
        return {
            "data": resp,
            "model": model,
            "object": "list",
            "usage": {"prompt_tokens": inp_token, "total_tokens": inp_token},
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/vectordb/embed", methods=["POST"])
def vectordb_text():
    try: 
        input_text_list = request.get_json().get("input")
        model = request.get_json().get("model", "bge-small")
        db = request.get_json().get("db", "lancedb")
        index_name = request.get_json().get("index_name")
        embeddings_api_key = request.get_json().get("embeddings_api_key", None)
        db_api_key = request.get_json().get("db_api_key", None)

        configs = VectorDBConfig(with_envs=False)
        embeddings = configs.get_embeddings(model)
        vectordb = configs.get_vectordb(db)

        logger.info(embeddings)

        embeddingProvider = VectorFactory.get_embeddings(type=embeddings, model=model, api_key=embeddings_api_key)
        vectordbProvider = VectorFactory.get_vector_storage(type=vectordb, api_key=db_api_key, embedding_model=embeddingProvider, index_name=index_name)

        inp_token = num_tokens_from_string("".join(input_text_list))
        
        resp = []
        if isinstance(input_text_list, str):            
            resp.append(vectordbProvider.add_texts([input_text_list]))
        else:
            resp.append(vectordbProvider.add_texts(input_text_list))

        logger.info(resp) 
        return {
            "data": resp,
            "model": model,
            "db": vectordb,
            "object": "list",
            "usage": {"prompt_tokens": inp_token, "total_tokens": inp_token},
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route("/vectordb/search", methods=["POST"])
def vectordb_search():
    try: 
        input_text = request.get_json().get("input")
        model = request.get_json().get("model", "bge-small")
        db = request.get_json().get("db", "lancedb")
        index_name = request.get_json().get("index_name")
        top_k = request.get_json().get("top_k", 5)
        relevance_score = request.get_json().get("relevance_score", 0.8)
        embeddings_api_key = request.get_json().get("embeddings_api_key", None)
        db_api_key = request.get_json().get("db_api_key", None)

        configs = VectorDBConfig(with_envs=False)
        embeddings = configs.get_embeddings(model)
        vectordb = configs.get_vectordb(db)

        logger.info(embeddings)

        embeddingProvider = VectorFactory.get_embeddings(type=embeddings, model=model, api_key=embeddings_api_key)
        vectordbProvider = VectorFactory.get_vector_storage(type=vectordb, api_key=db_api_key, embedding_model=embeddingProvider, index_name=index_name)

        inp_token = num_tokens_from_string("".join(input_text))
    
        res = vectordbProvider.similarity_search(query=input_text, top_k=top_k)
        resp = list(map(lambda x: {"text": x.page_content, "id": x.metadata.get("id"), "distance": x.metadata.get("_distance") }, res))

        logger.info(res) 
        return {
            "data": resp,
            "model": model,
            "db": vectordb,
            "object": "list",
            "usage": {"prompt_tokens": inp_token, "total_tokens": inp_token},
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/chat/completions", methods=["GET"])
def get_chat_models():
    try:
        configs = LLMConfig()
        return configs.providers
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/vectordb", methods=["GET"])
def get_vector_dbs():
    try:
        configs = VectorDBConfig()
        return configs.vectordbs
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/embeddings", methods=["GET"])
def get_embeddings_models():
    try:
        configs = VectorDBConfig()
        return configs.embeddings
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/prompts", methods=["GET"])
def get_prompts():
    try:
        full = request.args.get("full", 'false')

        configs = PromptConfig()
        if full == 'true':
            configs.add_prompt_to_config()
        prompts = configs.prompts
        
        return prompts
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/prompts/<name>", methods=["GET"])
def get_prompt(name: str):
    try:
        configs = PromptConfig()
        return { "content": configs.prompt_template(type=name) }
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
