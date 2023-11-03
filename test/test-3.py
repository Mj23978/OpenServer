from llama_cpp import Llama, LlamaGrammar

grammar = LlamaGrammar.from_file("D:/AI/SamoCoder/test/json_arr.gbnf")

llm = Llama(
    model_path="D:/AI/llama.cpp/models/dolphin-2.1-mistral-7b.Q5_K_M.gguf",
    chat_format="mistral",
    n_gpu_layers=99,
)


output = llm(
  "Create a Json Object from this output: Mark => Age: 22; John => Age: 45; Beth => Age: 34, Gender: Female",
  grammar=grammar,
  max_tokens=-1,
)

print(f"{output['choices'][0]['text']} \n\n")


# from sam.core.config.llm_config import LLMConfig

# print(LLMConfig().get_providers_for_model("gpt-3.5-turbo-16k", functions=True))
