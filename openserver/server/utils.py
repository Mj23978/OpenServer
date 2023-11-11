import tiktoken
from langchain.schema.output import LLMResult


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def llm_result_to_str(response: LLMResult):
    final_result = ""

    for generation in response.generations:
        for item in generation:
            final_result += item.text
    return final_result
