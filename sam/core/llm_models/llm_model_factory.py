from .ai21 import AI21Model
from .fireworks import FireworksModel
from .palm import GooglePalmModel
from .base import LLmInputInterface
from .cohere import CohereModel
from .openai import OpenAIModel
from .llama_cpp import LlamaCppModel
from .gf4 import G4FModel
from .fake import FakeModel


def build_model_factory(input: LLmInputInterface, provider_name: str = 'free'):
    if provider_name.lower() == 'openai':  # type: ignore
        return OpenAIModel(input)
    elif provider_name.lower() == 'cohere':
        return CohereModel(input)
    elif provider_name.lower() == 'llamacpp':
        return LlamaCppModel(input)
    elif provider_name.lower() == 'fake':
        return FakeModel(input)
    elif provider_name.lower() == 'ai21':
        return AI21Model(input)
    elif provider_name.lower() == 'fireworks':
        return FireworksModel(input)
    elif provider_name.lower() == 'palm':
        return GooglePalmModel(input)
    else:
        return G4FModel(input)
