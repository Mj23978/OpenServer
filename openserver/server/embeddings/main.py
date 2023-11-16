
from flask import jsonify, request

from openserver.core.config.vector_config import VectorDBConfig
from openserver.core.utils import logger
from openserver.core.vector_store.vector_factory import VectorFactory
from openserver.server.app import app
from openserver.server.utils import num_tokens_from_string


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
            type=provider.name, model=provider.name, api_key=api_key or provider.args.get("api_key"))
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
        return jsonify(configs.embeddings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
