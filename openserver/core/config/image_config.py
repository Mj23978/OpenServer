from .config import init_config
from .base import BaseConfig, ConfigProvidersIn


class ImageConfig(BaseConfig):

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/image_config.yaml", with_envs)
        self.configs = configs
        self.image_models: ConfigProvidersIn = self.parse(configs.get_configs().get(
            "image_models") or {})

    def get_image_providers(self, model: str):
        providers = self.image_models.find_model(
            self.image_models.providers, model)
        provider = self.image_models.choose_model(providers, model)
        return provider
