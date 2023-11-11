from typing import Any, Dict, List

from .base import BaseLlmModel, LLmInputInterface

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema.output import LLMResult
from langchain.callbacks.base import Callbacks
from langchain.schema import BaseMessage


class OpenAIModel(BaseLlmModel):
    def __init__(self, input: LLmInputInterface) -> None:
        self.client = OpenAI(
            openai_api_key=input.api_key,
            model=input.model_name if input.model_name else "gpt-3.5-turbo",
            batch_size=input.top_k,
            top_p=input.top_p,
            temperature=input.temperature,
            max_tokens=input.max_tokens,
            frequency_penalty=input.repeat_penalty,
            max_retries=input.max_retries,
            cache=input.cache,
            streaming=input.stream,
            verbose=input.verbose,
            callbacks=input.callbacks,
            metadata=input.metadata,
        )  # type: ignore

    def compelete(self, prompts: List[str], callbacks: Callbacks = None, metadata: Dict[str, Any] | None = None) -> LLMResult:
        result: LLMResult = self.client.generate(
            prompts=prompts, callbacks=callbacks, metadata=metadata)
        return result

    async def acompelete(self, prompts: List[str], callbacks: Callbacks = None, metadata: Dict[str, Any] | None = None):
        result = await self.client.agenerate(prompts=prompts, metadata=metadata, callbacks=callbacks)
        return result


class ChatOpenAIModel(BaseLlmModel):
    def __init__(self, input: LLmInputInterface) -> None:
        self.client = ChatOpenAI(
            openai_api_key=input.api_key,
            model=input.model_name if input.model_name else "gpt-3.5-turbo",
            temperature=input.temperature,
            max_tokens=input.max_tokens,
            max_retries=input.max_retries,
            cache=input.cache,
            streaming=input.stream,
            verbose=input.verbose,
            callbacks=input.callbacks,
            metadata=input.metadata,
        )  # type: ignore

    def compelete(self, prompts: List[List[BaseMessage]], callbacks: Callbacks = None, metadata: Dict[str, Any] | None = None) -> LLMResult:
        result: LLMResult = self.client.generate(
            messages=prompts, callbacks=callbacks, metadata=metadata)
        return result

    async def acompelete(self, prompts: List[List[BaseMessage]], callbacks: Callbacks = None, metadata: Dict[str, Any] | None = None) -> LLMResult:
        result: LLMResult = await self.client.agenerate(messages=prompts, callbacks=callbacks, metadata=metadata)
        return result
