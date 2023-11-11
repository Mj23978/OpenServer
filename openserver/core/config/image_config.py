import random
from typing import Any, Dict, List

from .config import init_config


class ImageConfig:

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/image_config.yaml", with_envs)
        self.configs = configs
        self.image_models: Dict[str, Any] = configs.get_configs().get(
            "image_models")  # type: ignore
        self.filter_unavailable()

    def get_image_providers(self, model: str, fallback: str = "together"):

        providers = self.image_models

        filtered_list = list(
            filter(lambda x: model in x["models"], providers.values()))
        filtered_names = list(map(lambda x: x['name'], filtered_list))
        provider = self.pick_random_item(filtered_names, fallback)

        provider_models = providers[provider]["models"]
        if model not in provider_models:
            model = provider_models[0]

        return provider, model

    def filter_unavailable(self):
        self.image_models = dict(
            filter(lambda x: x[1]["available"] is True, self.image_models.items()))

    def pick_random_item(self, lst: List[str], fallback: str):
        if lst:
            return random.choice(lst)
        else:
            return fallback
