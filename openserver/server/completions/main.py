import json
import random
import string
import time
from typing import List

from flask import jsonify, request

from openserver.core.llm_models.base import LLmInputInterface
from openserver.core.llm_models.llm_model_factory import LLMFactory
from openserver.core.config import CompletionConfig
from openserver.core.utils import logger
from openserver.core.utils.cost import completion_price_calculator
from openserver.server.app import app
from openserver.server.utils import llm_result_to_str, num_tokens_from_string


class CompletionsRequest:
    def __init__(self, request):
        try:
            self.model: str = request.get_json().get("model", "gpt-3.5-turbo")
            self.stream: bool = request.get_json().get("stream", False)
            self.api_key: str = request.get_json().get("api_key")
            self.prompts: List[str] | str = request.get_json().get("prompt")
            self.n_gpu_layers: int = request.get_json().get("n_gpu_layers", 99)
            self.temperature: float = request.get_json().get("temperature", 0.4)
            self.max_tokens: int = request.get_json().get("max_tokens", 1000)
            self.top_p: int = request.get_json().get("top_p", 1)
            self.cache: bool = request.get_json().get("cache", False)
            self.n_ctx: int = request.get_json().get("n_ctx", 8196)
        except Exception as e:
            return jsonify({'reason': "request data error", 'error': str(e)}), 500


@app.route("/completions", methods=["POST"])
def completions():
    try:
        request_data = CompletionsRequest(request)

        configs = CompletionConfig(with_envs=True)
        provider = configs.get_completion_providers(request_data.model)

        logger.info(provider)

        modelPath = provider.args.get("model_path")
        if isinstance(modelPath, str) == False:
            modelPath = None
        completion_input = LLmInputInterface(
            api_key=request_data.api_key or provider.args.get("api_key"),
            model=provider.key or provider.name if modelPath is None else modelPath,
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

        completionProvider = LLMFactory.get_model(
            input=completion_input, provider_name=provider.provider)

        if isinstance(request_data.prompts, str):
            request_data.prompts = [request_data.prompts]
        response = completionProvider.compelete(
            prompts=request_data.prompts)
        response_str = llm_result_to_str(response)

        completion_id = "".join(random.choices(
            string.ascii_letters + string.digits, k=28))
        completion_timestamp = int(time.time())

        if not request_data.stream:
            inp_token = num_tokens_from_string("".join(request_data.prompts))
            out_token = num_tokens_from_string(response_str)

            res = {
                "id": f"cmpl-{completion_id}",
                "object": "text_completion",
                "created": completion_timestamp,
                "model": provider.name,
                "choices": [
                    {
                        "index": 0,
                        "text": response_str,
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": inp_token,
                    "completion_tokens": out_token,
                    "total_tokens": inp_token + out_token,
                    "cost": "{:.6f}".format(completion_price_calculator(provider.cost.input, provider.cost.output, inp_token, out_token))
                },
            }
            return res

        def streaming():
            for chunk in response:
                completion_data = {
                    "id": f"cmpl-{completion_id}",
                    "object": "text_completion.chunk",
                    "created": completion_timestamp,
                    "model": provider.name,
                    "choices": [
                        {
                            "index": 0,
                            "text": chunk,
                            "finish_reason": None,
                        }
                    ],
                }

                content = json.dumps(completion_data, separators=(",", ":"))
                yield f"data: {content}"

                time.sleep(0.1)

            end_completion_data = {
                "id": f"cmpl-{completion_id}",
                "object": "text_completion.chunk",
                "created": completion_timestamp,
                "model": provider.name,
                "choices": [
                    {
                        "index": 0,
                        "text": "",
                        "finish_reason": "stop",
                    }
                ],
            }

            content = json.dumps(end_completion_data, separators=(",", ":"))
            yield f"data: {content}"

        # type: ignore
        return app.response_class(streaming(), mimetype="text/event-stream")
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/completions", methods=["GET"])
def get_completion_models():
    try:
        configs = CompletionConfig()
        for provider in configs.completion_providers.providers:
            provider.api_key = ""
            provider.args = dict(filter(lambda item: item[0] not in [
                'api_key', 'api_key_name'], provider.args.items()))
        return configs.completion_providers.model_dump()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
