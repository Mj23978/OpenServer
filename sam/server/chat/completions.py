import json
import random
import string
import time
from typing import Any, Dict, List

from flask import jsonify, request
from langchain.schema import BaseMessage
from sam.server.app import app

from sam.core.llm_models.base import LLmInputInterface
from sam.core.llm_models.llm_model_factory import LLMFactory
from sam.core.config import LLMConfig, PromptConfig
from sam.core.utils import logger
from sam.server.utils import llm_result_to_str, num_tokens_from_string


class ChatCompletionsRequest:
    def __init__(self, request):
        try:
            self.model: str = request.get_json().get("model", "gpt-3.5-turbo")
            self.stream: bool = request.get_json().get("stream", False)
            self.api_key: str = request.get_json().get("api_key")
            self.messages: List[Dict[str, Any]
                                ] = request.get_json().get("messages")
            self.functions = request.get_json().get("functions")
            self.n_gpu_layers: int = request.get_json().get("n_gpu_layers", 99)
            self.temperature: float = request.get_json().get("temperature", 0.4)
            self.max_tokens: int = request.get_json().get("max_tokens", 1000)
            self.top_p: int = request.get_json().get("top_p", 1)
            self.cache: bool = request.get_json().get("cache", False)
            self.n_ctx: int = request.get_json().get("n_ctx", 8196)
        except Exception as e:
            return jsonify({'reason': "request data error", 'error': str(e)}), 500


@app.route("/chat/completions", methods=["POST"])
def chat_completions():
    try:
        request_data = ChatCompletionsRequest(request)

        avaialable_functions = False

        if "functions" in request.get_json():
            avaialable_functions = True

        configs = LLMConfig(with_envs=True)
        provider = configs.get_chat_providers(
            request_data.model, avaialable_functions)

        logger.info(provider)

        chat_input = LLmInputInterface(
            api_key=request_data.api_key,
            model=provider.model if provider.modelPath is None else provider.modelPath,
            model_kwargs={
                "chat_format": "mistral",
            },
            streaming=request_data.stream,
            n_gpu_layers=request_data.n_gpu_layers,
            temperature=request_data.temperature,
            max_tokens=request_data.max_tokens,
            top_p=request_data.top_p,
            cache=request_data.cache,
            n_ctx=request_data.n_ctx,
        )

        messages = [BaseMessage(
            type=message["role"], content=message["content"]) for message in request_data.messages]

        if avaialable_functions is True:
            configs = PromptConfig()
            new_messages = configs.extract_text(configs.prompt_template(
            ), prompt=messages[-1].content, functions=request_data.functions)
            messages.pop()
            messages = messages + new_messages

            chat_input.grammer_path = "D:/AI/SamoCoder/test/json.gbnf"
            chat_input.f16_kv = True

        chatProvider = LLMFactory.get_chat_model(
            input=chat_input, provider_name=provider.provider)
        response = chatProvider.compelete(
            prompts=[messages])
        response_str = llm_result_to_str(response)

        completion_id = "".join(random.choices(
            string.ascii_letters + string.digits, k=28))
        completion_timestamp = int(time.time())

        if not request_data.stream:
            inp_token = num_tokens_from_string(
                "".join([message.content for message in messages]))
            out_token = num_tokens_from_string(response_str)
            function_out = None

            if avaialable_functions is True:
                from langchain.output_parsers.json import SimpleJsonOutputParser

                function_out = SimpleJsonOutputParser().parse(response_str)

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
            if function_out is not None or function_out != "":
                res["choices"][0]["message"]["content"] = None
                res["choices"][0]["message"]["function_call"] = function_out
                res["choices"][0]["message"]["content"] = None
                res["choices"][0]["finish_reason"] = "function_call"
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
                "model": provider.model,
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


@app.route("/chat/completions", methods=["GET"])
def get_chat_models():
    try:
        configs = LLMConfig()
        return configs.chat_providers
    except Exception as e:
        return jsonify({'error': str(e)}), 500
