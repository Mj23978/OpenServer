
from .config import init_config
from .base import BaseConfig, ConfigProvidersIn


class ChatConfig(BaseConfig):

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/chat_config.yaml", with_envs)
        self.configs = configs
        self.chat_providers: ConfigProvidersIn = self.parse(configs.get_configs().get(
            "chat_providers") or {})

    def get_chat_providers(self, model: str, functions: bool):
        providers = self.functions_available(functions)
        providers = self.chat_providers.find_model(providers, model)
        provider = self.chat_providers.choose_model(providers, model)
        return provider

    def functions_available(self, functions: bool):
        if functions is True:
            return list(filter(lambda x: x.args.get("functions") is True, self.chat_providers.providers))
        return self.chat_providers.providers
