import base64
import requests
import os
import time
from typing import List
import requests

from sam.core.utils.image import base64_to_image, image_to_base64

from .base import BaseImageModel, ImageInputInterface


class SegmindImageModel(BaseImageModel):

    def txt2img(self, input: ImageInputInterface):
        input.api_key = input.api_key or os.getenv("SEGMIND_API_KEY")
        width, height = input.size.split('x')

        url = f"https://api.segmind.com/v1/{input.model_name}"
        data = {
            "prompt": input.prompt,
            "negative_prompt": input.negative_prompt,
            "samples": input.n,
            "scheduler": input.sampler_name,
            "num_inference_steps": input.steps,
            "guidance_scale": input.cfg,
            "seed": input.seed,
            "img_width": width,
            "img_height": height,
            "base64": True if input.response_format == "b64_json" else False
        }

        response = requests.post(url, json=data, headers={'x-api-key': input.api_key or ""})
        if response.content is not None:
            image = base64.b64encode(response.content).decode('utf-8')
            if input.download_path is not None:
              base64_to_image(image, input.download_path.format(image=f"output-{time.time()}"))
            return [image]
