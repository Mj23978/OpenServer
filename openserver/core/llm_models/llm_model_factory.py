from .together import ChatTogetherModel, TogetherModel
from .ai21 import AI21Model
from .fireworks import ChatFireworksModel, FireworksModel
from .palm import ChatGooglePalmModel, GooglePalmModel
from .base import LLmInputInterface, LLMType
from .cohere import ChatCohereModel, CohereModel
from .openai import ChatOpenAIModel, OpenAIModel
from .llama_cpp import LlamaCppModel
from .fake import FakeChatModel, FakeModel


class LLMFactory:

    @classmethod
    def get_model(cls, input: LLmInputInterface, provider_name: LLMType | str = 'together'):
        if isinstance(provider_name, str):
            provider_name = LLMType.get_type(provider_name.lower())

        if provider_name == LLMType.OPENAI:
            return OpenAIModel(input)

        elif provider_name == LLMType.COHERE:
            return CohereModel(input)

        elif provider_name == LLMType.LLAMACPP:
            return LlamaCppModel(input)

        elif provider_name == LLMType.FAKE:
            return FakeModel(input)

        elif provider_name == LLMType.AI21:
            return AI21Model(input)

        elif provider_name == LLMType.FIREWORKS:
            return FireworksModel(input)

        elif provider_name == LLMType.PALM:
            return GooglePalmModel(input)

        elif provider_name == LLMType.TOGETHER:
            return TogetherModel(input)

        else:
            return TogetherModel(input)

    @classmethod
    def get_chat_model(cls, input: LLmInputInterface, provider_name: LLMType | str = 'together'):
        if isinstance(provider_name, str):
            provider_name = LLMType.get_type(provider_name.lower())

        if provider_name == LLMType.OPENAI:
            return ChatOpenAIModel(input)

        elif provider_name == LLMType.PALM:
            return ChatGooglePalmModel(input)

        elif provider_name == LLMType.COHERE:
            return ChatCohereModel(input)

        elif provider_name == LLMType.FAKE:
            return FakeChatModel(input)

        elif provider_name == LLMType.FIREWORKS:
            return ChatFireworksModel(input)

        else:
            return ChatTogetherModel(input)

