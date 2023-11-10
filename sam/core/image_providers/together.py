from typing import List
import together

from sam.core.image_providers.base import BaseImageModel, ImageInputInterface


class TogetherImageModel(BaseImageModel):

    def txt2img(self, input: ImageInputInterface):
        width, height = input.size.split('x')
        response = together.Image.create(
            prompt=input.prompt,
            steps=input.steps,
            model=input.model_name,
            results=input.n,
            negative_prompt=input.quality,
            height=int(height),
            width=int(width),
        )
        res: List[str] = []
        if isinstance(response, dict):
            for image in response["output"]["choices"]:
              res.append(image["image_base64"])
        return res
