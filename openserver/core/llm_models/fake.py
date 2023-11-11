from typing import Any, Dict, List

from .base import BaseChat, BaseLlmModel, LLmInputInterface

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import FakeListLLM
from langchain.chat_models import FakeListChatModel
from langchain.schema.output import LLMResult
from langchain.schema import BaseMessage
from langchain.callbacks.base import Callbacks


class FakeModel(BaseLlmModel):
    def __init__(self, input: LLmInputInterface) -> None:
        self.client = FakeListLLM(
            responses=input.responses if input.responses else [],
            cache=input.cache,
            verbose=input.verbose,
            callbacks=CallbackManager(
                handlers=[StreamingStdOutCallbackHandler()]),
        )  # type: ignore

    def compelete(self, prompts: List[str], callbacks: Callbacks | List[Callbacks] = None, metadata: Dict[str, Any] | None = None) -> LLMResult:
        result: LLMResult = self.client.generate(prompts=prompts)
        return result

    async def acompelete(self, prompts: List[str], callbacks: Callbacks | List[Callbacks] = None, metadata: Dict[str, Any] | None = None):
        result = await self.client.agenerate(prompts=prompts, metadata=metadata, callbacks=callbacks)
        return result


class FakeChatModel(BaseChat):
    def __init__(self, input: LLmInputInterface) -> None:
        self.client = FakeListChatModel(
            responses=input.responses if input.responses else [],
            cache=input.cache,
            verbose=input.verbose,
            callbacks=CallbackManager(
                handlers=[StreamingStdOutCallbackHandler()]),
        )  # type: ignore

    def compelete(self, prompts: List[List[BaseMessage]], callbacks: Callbacks = None, metadata: Dict[str, Any] | None = None) -> LLMResult:
        result: LLMResult = self.client.generate(
            messages=prompts, callbacks=callbacks, metadata=metadata)
        return result

    async def acompelete(self, prompts: List[List[BaseMessage]], callbacks: Callbacks = None, metadata: Dict[str, Any] | None = None) -> LLMResult:
        result: LLMResult = await self.client.agenerate(messages=prompts, callbacks=callbacks, metadata=metadata)
        return result
