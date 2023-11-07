import random
from pydantic import BaseModel
from typing import Any, Dict, List

from sam.core.utils import logger
from .config import init_config


class ConfigVectorDB(BaseModel):
    embedding: str
    vectordb: str


class VectorDBConfig:

    def __init__(self, with_envs: bool = False):
        configs = init_config("configs/vectordb_config.yaml", with_envs)
        self.configs = configs
        self.embeddings: Dict[str, Any] = configs.get_configs().get(
            "embeddings")  or {}
        self.vectordbs: Dict[str, Any] = configs.get_configs().get(
            "vectordbs") or {}
        self.filter_unavailable()

    def get_embeddings(self, model: str):
        filtered_list = list(
            filter(lambda x: model in x["models"], self.embeddings.values()))
        if len(filtered_list) < 1:
          raise ValueError(f"{model} not founded in list of embeddings")
        filtered_names = list(map(lambda x: x['name'], filtered_list))
        embedding = self.pick_random_item(filtered_names)
        return embedding

    def get_vectordb(self, db: str):
        filtered_list = list(
            filter(lambda x: x == db, self.vectordbs.keys()))
        if len(filtered_list) < 1:
          raise ValueError(f"{db} not founded in list of vectordbs")
        return db

    def filter_unavailable(self):
        self.embeddings = dict(
            filter(lambda x: x[1]["available"] is True, self.embeddings.items()))
        self.vectordbs = dict(
            filter(lambda x: x[1]["available"] is True, self.vectordbs.items()))


    def pick_random_item(self, lst: List[str]):
        return random.choice(lst)
