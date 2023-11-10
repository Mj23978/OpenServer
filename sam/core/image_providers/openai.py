from typing import List
import openai

from sam.core.image_providers.base import BaseImageModel, ImageInputInterface


class OpenAIImageModel(BaseImageModel):

    def txt2img(self, input: ImageInputInterface):
        response = openai.Image.create(
            prompt=input.prompt,
            api_key=input.api_key,
            model=input.model_name,
            n=input.n,
            quality=input.quality,
            size=input.size,
            response_format=input.response_format,
        )
        res: List[str] = []
        if isinstance(response, dict):
            for image in response["data"]:
              if image.get('url') is not None:
                res.append(image["url"])
              if image.get('b64_json') is not None:
                res.append(image["b64_json"])
        return res
