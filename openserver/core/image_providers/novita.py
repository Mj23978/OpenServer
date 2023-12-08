import os
import time
from typing import Any, List
import requests

from novita_client import NovitaClient, Txt2ImgRequest, save_image, Img2ImgRequest, UpscaleRequest

from ..utils import image_to_base64
from .base import BaseImageModel, ImageInputInterface


class NovitaImageModel(BaseImageModel):

    client: NovitaClient | None = None

    def txt2img(self, input: ImageInputInterface):
        input.api_key = input.api_key or os.getenv("NOVITA_API_KEY")
        width, height = input.size.split('x')

        if self.client is None:
            self.client = NovitaClient(input.api_key)
        progress = self.client.sync_txt2img(
            request=Txt2ImgRequest(
                prompt=input.prompt,
                negative_prompt=input.negative_prompt or "",
                model_name=input.model_name,
                sampler_name=input.sampler_name,
                batch_size=input.n,
                n_iter=1,
                steps=input.steps,
                cfg_scale=input.cfg,
                seed=input.seed,
                height=int(width),
                width=int(height)
            ),
            download_images=True if input.response_format == "b64_json" else False
        )
        if progress.data is not None:
            if progress.data.imgs_bytes is not None:
                if input.download_path is not None:
                    for i, img_bytes in enumerate(progress.data.imgs_bytes):
                        if progress.data.imgs is not None:
                            save_image(
                                img_bytes, input.download_path.format(image=progress.data.imgs[i].split("/")[-1]))
                return progress.data.imgs_bytes
            else:
                return progress.data.imgs

    def img2img(self, input: ImageInputInterface, images: List[str]):
        input.api_key = input.api_key or os.getenv("NOVITA_API_KEY")
        width, height = input.size.split('x')

        if self.client is None:
            self.client = NovitaClient(input.api_key)
        progress = self.client.sync_img2img(
            request=Img2ImgRequest(
                prompt=input.prompt,
                negative_prompt=input.negative_prompt or "",
                model_name=input.model_name,
                sampler_name=input.sampler_name,
                batch_size=input.n,
                n_iter=1,
                steps=input.steps,
                cfg_scale=input.cfg,
                seed=input.seed,
                height=int(width),
                width=int(height),
                init_images=[image_to_base64(img) for img in images]
            ),
            download_images=False if input.download_path is None else True
        )
        if progress.data is not None:
            if progress.data.imgs_bytes is not None:
                for i, img_bytes in enumerate(progress.data.imgs_bytes):
                    if progress.data.imgs is not None:
                        save_image(
                            img_bytes, f'{progress.data.imgs[i].split("/")[-1]}')
            return progress.data.imgs

    def search_models(self, attribute: str, value: Any, api_key: str | None = None):
        api_key = api_key or os.getenv("NOVITA_API_KEY")

        if self.client is None:
            self.client = NovitaClient(api_key)
        models = self.client.models()
        return [model for model in models if self.filter_models(model, attribute, value)]

    def all_models(self, api_key: str | None = None):
        api_key = api_key or os.getenv("NOVITA_API_KEY")

        if self.client is None:
            self.client = NovitaClient(api_key)
        models = self.client.models()
        return models
        
    def filter_models(self, model: Any, attribute: str, value: Any) -> bool:    
        if attribute in ["name", "sd_name", "base_model", "civitai_tags", "download_name"]:
            field = getattr(model, attribute)
            if field is None:
                return False
            return field.find(value) != -1
        if attribute in ["civitai_version_id", "download_status"]:
            field = getattr(model, attribute)
            if field is None:
                return False
            return field == value
        return False
    
    def get_image_task_id(self, task_id: str, api_key: str | None = None):
        api_key = api_key or os.getenv("NOVITA_API_KEY")
        return retry_request(task_id, api_key)

    def upscale_image(self, image_path: str, api_key: str | None = None):
        api_key = api_key or os.getenv("NOVITA_API_KEY")

        if self.client is None:
            self.client = NovitaClient(api_key)
        progress = self.client.upscale(request=UpscaleRequest(
            image=image_to_base64(image_path)
        ))

        if progress.data is not None:
            return self.get_image_task_id(progress.data.task_id, api_key)


def retry_request(task_id, api_key):
    delay = 1  # initial delay
    max_delay = 4  # maximum delay
    url = f"https://api.novita.ai/v2/progress?task_id={task_id}"
    headers = {
        'X-Omni-Key': api_key
    }

    while delay <= max_delay:
        time.sleep(delay)
        progress_response = requests.get(url, headers=headers).json()

        if progress_response["data"] is None or progress_response["data"]['status'] == 1 and progress_response["data"]['progress'] < 1:
            delay *= 2  # double the delay
        else:
            return progress_response["data"]["imgs"]

    # If we've made it here, we've failed all attempts
    raise Exception(
        "Failed to get a successful response after multiple attempts")
