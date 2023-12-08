import random
from typing import Any, Dict, List

from pydantic import BaseModel

from .config import get_config


class BaseConfigError(Exception):
    pass

class InvalidConfigError(BaseConfigError):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Cost(BaseModel):
    input: float
    output: float

class ConfigModelOut(BaseModel):
    provider: str
    name: str
    key: str | None = None
    cost: Cost
    args: Dict[str, Any] = {}


class ConfigModelIn(BaseModel):
    name: str
    key: str | None = None
    cost: Cost
    args: Dict[str, Any] = {}

class ConfigProviderIn(BaseModel):
    name: str
    provider: str
    api_key: str | None = None
    available: bool = True
    models: List[ConfigModelIn]
    args: Dict[str, Any] = {}

class ConfigProvidersIn(BaseModel):
    providers: List[ConfigProviderIn]
    args: Dict[str, Any] | None = None
    
    def find_model(self, providers: List[ConfigProviderIn], search: str):
        res: List[ConfigProviderIn] = []
        if len(providers) == 0:
            providers = self.providers
        for provider in providers:
            for model in provider.models:
                if model.name == search:
                    res.append(provider)
        return res
    
    def choose_model(self, providers: List[ConfigProviderIn], model: str):
        rand = False
        if len(providers) == 0:
            rand = True
            providers = self.providers
        provider = random.choice(providers)
        models = list(filter(lambda x: x.name == model, provider.models))
        if rand == True or len(models) == 0:
            mode = random.choice(provider.models)
            return ConfigModelOut(name=mode.name, key=mode.key, provider=provider.provider, cost=mode.cost, args={**provider.args, **mode.args})
        return ConfigModelOut(name=models[0].name, key=models[0].key, provider=provider.provider, cost=models[0].cost, args={**provider.args, **models[0].args})


class BaseConfig:

    @classmethod
    def parse(cls, providers: Dict[str, Any], filter_unavailable = True):
        config_providers: List[ConfigProviderIn] = []
        for name, provider in providers.items():
            if isinstance(provider, dict):
                if provider.get("api_key_name") is not None and isinstance(provider["api_key_name"], str):
                    provider["api_key_name"] = get_config(provider["api_key_name"])
                config_provider = ConfigProviderIn(
                    name = provider.get("name") or name,
                    provider = provider.get("provider") or provider.get("name") or name,
                    api_key = provider.get("api_key_name"),
                    available = provider.get("available") or True,
                    models = cls.parse_model(provider),
                    args=dict(filter(lambda item: item[0] not in ['name', 'models', 'available'], provider.items()))
                )
                if filter_unavailable == True and provider.get("available") is not None and provider["available"] == False:
                    pass
                else:
                    config_providers.append(config_provider)                    
            else:
                raise InvalidConfigError(provider, f"Config provider {provider} must be a Dict.")
        config_model = ConfigProvidersIn(
            providers=config_providers,
        )
        return config_model

    @classmethod
    def parse_model(cls, provider: Dict[str, Any]):
        models = provider["models"]
        config_models: List[ConfigModelIn] = []
        if isinstance(models, list):
            for model in models:
                if isinstance(model, str):
                    config_models.append(
                        ConfigModelIn(
                            name=model, 
                            cost=Cost(input=0.001, output=0.001),
                        )
                    )
                else:
                  raise InvalidConfigError(provider, f"Config models List {models} must be string: {model}.")
            return config_models
        if isinstance(models, dict):
            for key, value in models.items():
                if isinstance(value, dict):
                    cost = value.get("cost")
                    if cost is None or isinstance(cost, dict) == False:
                        cost = {"input": 0.001, "output": 0.001}
                    config_models.append(
                        ConfigModelIn(
                            name=value.get("name") or key,
                            key=value.get("key"),
                            cost=Cost(input=cost["input"], output=cost["output"]),
                            args=dict(filter(lambda item: item[0] not in ['name', 'key', 'cost'], value.items()))
                        )
                    )
                else:
                  raise InvalidConfigError(
                      provider, f"Config models {models} must be Dict: {value}.")
            return config_models
        else:
          raise InvalidConfigError(provider, f"Config models {models} must be a List or Dict.")