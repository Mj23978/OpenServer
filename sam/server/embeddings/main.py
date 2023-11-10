
from flask import jsonify, request

from sam.core.config.vector_config import VectorDBConfig
from sam.core.utils import logger
from sam.core.vector_store.vector_factory import VectorFactory
from sam.server.app import app
from sam.server.utils import num_tokens_from_string


@app.route("/embeddings", methods=["POST"])
def embeddings():
    try:
        input_text_list = request.get_json().get("input")
        model = request.get_json().get("model", "bge-small")
        api_key = request.get_json().get("api_key", None)

        configs = VectorDBConfig(with_envs=False)
        provider = configs.get_embeddings(model)

        logger.info(provider)

        embeddingProvider = VectorFactory.get_embeddings(
            type=provider, model=model, api_key=api_key)
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


@app.route("/embeddings", methods=["GET"])
def get_embeddings_models():
    try:
        configs = VectorDBConfig()
        return configs.embeddings
    except Exception as e:
        return jsonify({'error': str(e)}), 500
