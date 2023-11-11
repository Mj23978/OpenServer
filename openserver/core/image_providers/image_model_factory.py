from .segmind import SegmindImageModel
from .novita import NovitaImageModel
from .base import ImageType
from .openai import OpenAIImageModel
from .together import TogetherImageModel


class ImageFactory:

    @classmethod
    def get_txt2txt_model(cls, provider_name: ImageType | str = 'novita'):
        if isinstance(provider_name, str):
            provider_name = ImageType.get_type(provider_name.lower())

        if provider_name == ImageType.OPENAI:
            return OpenAIImageModel()

        elif provider_name == ImageType.NOVITA:
            return NovitaImageModel()

        elif provider_name == ImageType.TOGETHER:
            return TogetherImageModel()

        elif provider_name == ImageType.SEGMIND:
            return SegmindImageModel()

        else:
            return NovitaImageModel()
