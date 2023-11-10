
from flask import jsonify, request

from sam.core.config import PromptConfig
from sam.server.app import app


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
        return {"content": configs.prompt_template(type=name)}
    except Exception as e:
        return jsonify({'error': str(e)}), 500
