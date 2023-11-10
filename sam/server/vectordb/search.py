
from flask import jsonify, request

from sam.core.config.vector_config import VectorDBConfig
from sam.core.utils import logger
from sam.core.vector_store.vector_factory import VectorFactory
from sam.server.app import app
from sam.server.utils import num_tokens_from_string


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

        embeddingProvider = VectorFactory.get_embeddings(
            type=embeddings, model=model, api_key=embeddings_api_key)
        vectordbProvider = VectorFactory.get_vector_storage(
            type=vectordb, api_key=db_api_key, embedding_model=embeddingProvider, index_name=index_name)

        inp_token = num_tokens_from_string("".join(input_text))

        res = vectordbProvider.similarity_search(query=input_text, top_k=top_k)
        resp = list(map(lambda x: {"text": x.page_content, "id": x.metadata.get(
            "id"), "distance": x.metadata.get("_distance")}, res))

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
