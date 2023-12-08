
from .config import init_config
from .base import BaseConfig, ConfigProvidersIn


class CompletionConfig(BaseConfig):

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/completion_config.yaml", with_envs)
        self.configs = configs
        self.completion_providers: ConfigProvidersIn = self.parse(configs.get_configs().get(
            "completion_providers") or {})

    def get_completion_providers(self, model: str):
        providers = self.completion_providers.find_model(
            self.completion_providers.providers, model)
        provider = self.completion_providers.choose_model(providers, model)
        return provider