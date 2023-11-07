from enum import Enum
from pathlib import Path
from typing import Any, Dict, List
from abc import ABC, abstractmethod

from langchain.globals import set_llm_cache
from gptcache import Cache
from gptcache.adapter.api import init_similar_cache
from langchain.cache import GPTCache
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager, Callbacks
from langchain.cache import InMemoryCache
from llama_cpp import LlamaGrammar

set_llm_cache(InMemoryCache())

class BaseLlmModel(ABC):

    @abstractmethod
    def compelete(self, prompts: List[str]):
        pass

    @abstractmethod
    async def acompelete(self, prompts: List[str], callbacks: Callbacks | List[Callbacks] = None, metadata: Dict[str, Any] | None = None):
        pass


class LLmInputInterface:
    def __init__(self, model: str, api_key: str | None = None, stop: List[str] = ["### Humen:", "### Instruction:", "### Assistant:", "\nQuestion:"], max_tokens=4196, repeat_penalty=0.2,
                 responses: List[str] | None = None, top_k=30, top_p=0.95, streaming: bool = False, temperature=0.2, cache=True, verbose=True, max_retries=10, n_ctx: int = 2048, f16_kv=True,
                 n_gpu_layers: int = 50, n_threads=4, metadata: Dict[str, Any] | None = None, callback_manager: Callbacks | List[Callbacks] | BaseCallbackManager = CallbackManager(handlers=[StreamingStdOutCallbackHandler()]),
                 grammer: str | LlamaGrammar | None = None, grammer_path: str | Path | None = None, model_kwargs = {}):
        self.api_key: str | None = api_key
        self.model_name: str = model
        self.model_kwargs: Dict[str, Any] = model_kwargs
        self.stop: List[str] = stop
        self.max_tokens: int = max_tokens
        self.repeat_penalty: float = repeat_penalty
        self.top_k: int = top_k
        self.top_p: float = top_p
        self.temperature: float = temperature
        self.cache: bool = cache
        self.verbose: bool = verbose
        self.max_retries: int = max_retries
        self.responses: List[str] | None = responses
        self.stream: bool = streaming
        self.n_ctx: int = n_ctx
        self.f16_kv: bool = f16_kv
        self.n_gpu_layers: int = n_gpu_layers
        self.n_threads: int = n_threads
        self.grammer: str | LlamaGrammar | None = grammer
        self.grammer_path: str | Path | None = grammer_path
        self.callback_manager: Callbacks | List[Callbacks] | BaseCallbackManager | None = callback_manager
        self.metadata = metadata



class LLMType(Enum):
    AI21 = "ai21"
    COHERE = "cohere"
    FAKE = "fake"
    FIREWORKS = "fireworks"
    FREE = "free"
    LLAMACPP = "llamacpp"
    OPENAI = "openai"
    PALM = "palm"
    
    
    @classmethod
    def get_type(cls, type: str):
        type_enum_value = None
        for enum_value in LLMType:
            if type == enum_value.value:
                type_enum_value=enum_value
                break
        return type_enum_value or cls.FREE