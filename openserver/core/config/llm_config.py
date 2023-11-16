
from .config import init_config
from .base import BaseConfig, ConfigProvidersIn


class LLMConfig(BaseConfig):

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/llm_config.yaml", with_envs)
        self.configs = configs
        self.completion_providers: ConfigProvidersIn = self.parse(configs.get_configs().get(
            "completion_providers") or {})
        self.chat_providers: ConfigProvidersIn = self.parse(configs.get_configs().get(
            "chat_providers") or {})

    def get_completion_providers(self, model: str):
        providers = self.completion_providers.find_model(
            self.completion_providers.providers, model)
        provider = self.completion_providers.choose_model(providers, model)
        return provider

    def get_chat_providers(self, model: str, functions: bool):
        providers = self.functions_available(functions)
        providers = self.chat_providers.find_model(providers, model)
        provider = self.chat_providers.choose_model(providers, model)
        return provider

    def functions_available(self, functions: bool):
        if functions is True:
            return list(filter(lambda x: x.args.get("functions") is True, self.chat_providers.providers))
        return self.chat_providers.providers
