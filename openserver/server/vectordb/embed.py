
from flask import jsonify, request

from openserver.core.config.vector_config import VectorDBConfig
from openserver.core.utils import logger
from openserver.core.vector_store.vector_factory import VectorFactory
from openserver.server.app import app
from openserver.server.utils import num_tokens_from_string


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

        embeddingProvider = VectorFactory.get_embeddings(
            type=embeddings.provider, model=embeddings.name, api_key=embeddings_api_key or embeddings.args.get("api_key"))
        vectordbProvider = VectorFactory.get_vector_storage(
            type=vectordb, api_key=db_api_key, embedding_model=embeddingProvider, index_name=index_name)

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
