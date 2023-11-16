from pydantic import BaseModel
from typing import Any, Dict

from .config import init_config
from .base import BaseConfig, ConfigProvidersIn


class VectorDBConfig(BaseConfig):

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/vectordb_config.yaml", with_envs)
        self.configs = configs
        self.embeddings: ConfigProvidersIn = self.parse(configs.get_configs().get(
            "embeddings") or {})
        self.vectordbs: Dict[str, Any] = configs.get_configs().get(
            "vectordbs") or {}
        self.filter_unavailable()

    def get_embeddings(self, model: str):
        providers = self.embeddings.find_model(
            self.embeddings.providers, model)
        provider = self.embeddings.choose_model(providers, model)
        return provider

    def get_vectordb(self, db: str):
        filtered_list = list(
            filter(lambda x: x == db, self.vectordbs.keys()))
        if len(filtered_list) < 1:
            raise ValueError(f"{db} not founded in list of vectordbs")
        return db

    def filter_unavailable(self):
        self.vectordbs = dict(
            filter(lambda x: x[1]["available"] is True, self.vectordbs.items()))
