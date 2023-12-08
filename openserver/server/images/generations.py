
import time
from flask import jsonify, request
import validators
from openserver.core.config.image_config import ImageConfig

from openserver.core.image_providers.base import ImageInputInterface
from openserver.core.image_providers.image_model_factory import ImageFactory
from openserver.core.utils import logger
from openserver.server.app import app


@app.route("/images/generations", methods=["POST"])
def image_generations():
    try:
        data = request.get_json()
        image_input = ImageInputInterface(
            prompt=data.get("prompt"),
            model=data.get("model"),
            api_key=data.get("api_key", None),
            n=data.get("n", 1),
            quality=data.get("quality", "standard"),
            cfg=data.get("cfg", 6.5),
            size=data.get("size", "1024x1024"),
            response_format=data.get("response_format", "url"),
            style=data.get("style"),
            model_kwargs=data.get("model_kwargs", {}),
            steps=data.get("steps", 25),
            negative_prompt=data.get("negative_prompt"),
            sampler_name=data.get("sampler_name", "Euler a"),
            seed=data.get("seed", 43),
            download_path=data.get("download_path", False)
        )

        configs = ImageConfig(with_envs=False)
        provider = configs.get_image_providers(image_input.model_name)

        logger.info(provider)

        image_provider = ImageFactory.get_txt2txt_model(provider.provider)
        
        image_input.api_key = image_input.api_key or provider.args.get("api_key")
        image_input.model_name = provider.key or image_input.model_name
        
        images = image_provider.txt2img(image_input)
        if images is None:
            raise ValueError("Response is None")

        res = []
        for image in images:
            if validators.url(image):
                res.append({"url": image})
            else:
                res.append({"b64_json": str(image)})

        completion_timestamp = int(time.time())

        return jsonify({
            "created": completion_timestamp,
            "data": res,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/images/generations", methods=["GET"])
def get_image_models():
    try:
        configs = ImageConfig()
        for provider in configs.image_models.providers:
            provider.api_key = ""
            provider.args = dict(filter(lambda item: item[0] not in [
                                            'api_key', 'api_key_name'], provider.args.items()))
        return jsonify(configs.image_models.model_dump())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
