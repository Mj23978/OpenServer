from .ai21 import AI21Model
from .fireworks import FireworksModel
from .palm import GooglePalmModel
from .base import LLmInputInterface, LLMType
from .cohere import CohereModel
from .openai import OpenAIModel
from .llama_cpp import LlamaCppModel
from .gf4 import G4FModel
from .fake import FakeModel


class LLMFactory:

    @classmethod
    def get_model(cls, input: LLmInputInterface, provider_name: LLMType | str = 'free'):
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

        else:
            return G4FModel(input)
