from typing import Any, Dict, List

from pydantic import BaseModel
from .config import init_config
import random


class ConfigLLMModel(BaseModel):
    provider: str
    model: str
    modelPath: str | None


class LLMConfig:

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/llm_config.yaml", with_envs)
        self.configs = configs
        self.providers: Dict[str, Any] = configs.get_configs().get(
            "providers")  # type: ignore
        self.filter_unavailable()

    def get_providers_for_model(self, model: str, functions: bool, fallback: str = "llamacpp"):
        providers = self.functions_available(functions)

        filtered_list = list(
            filter(lambda x: model in x["models"], providers.values()))
        filtered_names = list(map(lambda x: x['name'], filtered_list))
        provider = self.pick_random_item(filtered_names, fallback)

        provider_models = providers[provider]["models"]
        if model not in provider_models:
            model = provider_models[0]
        model_path = None
        if "models_path" in providers[provider]:
            index = providers[provider]["models"].index(model)
            model_path = providers[provider]["models_path"][index]

        return ConfigLLMModel(provider=provider, model=model, modelPath=model_path)

    def filter_unavailable(self):
        self.providers = dict(
            filter(lambda x: x[1]["available"] is True, self.providers.items()))

    def functions_available(self, functions: bool):
        if functions is True:
            return dict(filter(lambda x: x[1]["functions"] is True, self.providers.items()))
        return self.providers

    def pick_random_item(self, lst: List[str], fallback: str):
        if lst:
            return random.choice(lst)
        else:
            return fallback
