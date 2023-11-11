
from flask import jsonify

from openserver.core.config.vector_config import VectorDBConfig
from openserver.server.app import app


@app.route("/vectordb", methods=["GET"])
def get_vector_dbs():
    try:
        configs = VectorDBConfig()
        return configs.vectordbs
    except Exception as e:
        return jsonify({'error': str(e)}), 500
