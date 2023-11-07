from enum import Enum
from abc import ABC, abstractmethod
from typing import List

from langchain.embeddings.base import Embeddings


class BaseEmbedding(ABC):
    
    client: Embeddings

    @abstractmethod
    def get_embeddings(self, text: List[str]) -> List[List[float]]:
        pass

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        pass


class EmbeddingsType(Enum):
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"
    PALM = "palm"
    GRADIENT = "gradient"
    
    
    @classmethod
    def get_type(cls, type: str):
        type_enum_value = None
        for enum_value in EmbeddingsType:
            if type == enum_value.value:
                type_enum_value=enum_value
                break
        return type_enum_value or cls.HUGGINGFACE