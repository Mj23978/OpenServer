from enum import Enum
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class BaseImageModel(ABC):

    @abstractmethod
    def txt2img(self, prompt: str):
        pass


class ImageInputInterface:
    def __init__(self, prompt: str, model: str, api_key: str | None = None, n: int = 1, quality: str = "standard", cfg: float = 6.5,
                 size: str = "1024x1024", response_format="url", style: str | None = None, model_kwargs={},
                 steps: int = 25, negative_prompt: str | None = None, sampler_name: str = "Euler a", seed=-1, download_path: str | None = None):
        self.prompt: str = prompt
        self.api_key: str | None = api_key
        self.model_name: str = model
        self.model_kwargs: Dict[str, Any] = model_kwargs
        self.n: int = n
        self.quality: str = quality
        self.size: str = size
        self.response_format: str = response_format
        self.cfg: float = cfg
        self.steps: int = steps
        self.style: str | None = style
        self.negative_prompt: str | None = negative_prompt
        self.sampler_name: str = sampler_name
        self.seed = seed
        self.download_path = download_path

    def to_dict(self):
        return vars(self)


class UpscaleImageInterface:
    def __init__(self, image: str, resize_mode: int = 1, upscaling_resize_w: int = 1024, upscaling_resize_h: int = 1024, 
        upscaling_crop: bool = True, upscaler_1: str = "R-ESRGAN 4x+", upscaler_2: str = "", extras_upscaler_2_visibility: float = 0.5, 
        gfpgan_visibility: float = 0.5, codeformer_visibility: float = 0.5, codeformer_weight: float = 0.5):
        self.image: str = image
        self.resize_mode: int = resize_mode
        self.upscaling_resize_w: int = upscaling_resize_w
        self.upscaling_resize_h: int = upscaling_resize_h
        self.upscaling_crop: bool = upscaling_crop
        self.upscaler_1: str = upscaler_1
        self.upscaler_2: str = upscaler_2
        self.extras_upscaler_2_visibility: float = extras_upscaler_2_visibility
        self.gfpgan_visibility: float = gfpgan_visibility
        self.codeformer_visibility: float = codeformer_visibility
        self.codeformer_weight: float = codeformer_weight

    def to_dict(self):
        return vars(self)


class FilterModelsInterface:
    id: int
    name: str | None = None
    sd_name: str | None = None
    base_model: str | None = None
    source: str | None = None
    civitai_nsfw: bool | None = None
    civitai_rating: int | None = None
    civitai_rating_count: int | None = None
    civitai_tags: str | None = None
    civitai_update_at: str | None = None
    civitai_version_id: int | None = None
    download_name: str | None = None
    download_status: int | None = None

class ImageType(Enum):
    FIREWORKS = "fireworks"
    OPENAI = "openai"
    TOGETHER = "together"
    NOVITA = "novita"
    SEGMIND = "segmind"

    @classmethod
    def get_type(cls, type: str):
        type_enum_value = None
        for enum_value in ImageType:
            if type == enum_value.value:
                type_enum_value = enum_value
                break
        return type_enum_value or cls.TOGETHER
