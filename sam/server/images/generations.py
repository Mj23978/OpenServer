
import time
from flask import jsonify, request
import validators
from sam.core.config.image_config import ImageConfig

from sam.core.image_providers.base import ImageInputInterface
from sam.core.image_providers.image_model_factory import ImageFactory
from sam.core.utils import logger
from sam.server.app import app


@app.route("/images/generations", methods=["POST"])
def image_generations():
    try:
        data = request.get_json()
        image_input = ImageInputInterface(
            prompt=data.get("prompt"),
            model=data.get("model"),
            api_key=data.get("api_key"),
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
        provider, model = configs.get_image_providers(image_input.model_name)

        logger.info(provider)

        image_provider = ImageFactory.get_txt2txt_model(provider)

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
        return configs.image_models
    except Exception as e:
        return jsonify({'error': str(e)}), 500
