from typing import Any, Dict, List, cast

from .base import BaseLlmModel, LLmInputInterface

from langchain.llms import OpenAI
from langchain.schema.output import LLMResult
from langchain.callbacks.base import Callbacks, BaseCallbackManager


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
            callback_manager=cast(BaseCallbackManager, input.callback_manager),
            metadata=input.metadata,
        )  # type: ignore

    def compelete(self, prompts: List[str], callbacks: Callbacks | List[Callbacks] = None, metadata: Dict[str, Any] | None = None) -> LLMResult:
        result: LLMResult = self.client.generate(prompts=prompts, callbacks=callbacks, metadata=metadata)
        return result

    async def acompelete(self, prompts: List[str], callbacks: Callbacks | List[Callbacks] = None, metadata: Dict[str, Any] | None = None):
        result = await self.client.agenerate(prompts=prompts, metadata=metadata, callbacks=callbacks)
        return result

