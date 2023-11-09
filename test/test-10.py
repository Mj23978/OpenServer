import together

together.api_key = "4d8d395b7b48314846f176eb221b72900d07e097252691d83aaa357e093bb0a3"

model_list = together.Models.list()

print(f"{len(model_list)} models available")

# print the first 10 models on the menu
model_list = list(
    filter(lambda x: x.get('display_type') == "image", model_list))
# model_list = list(
#     filter(lambda x: x["name"].lower().find("codellama") != -1, model_list))
model_names = [{"name": model_dict['name'],
                "type": model_dict.get("display_type")} for model_dict in model_list]
print(model_names)


# from sam.core.llm_models.together import ChatTogetherLLM, TogetherLLM
# from langchain.schema.messages import (
#     AIMessage,
#     BaseMessage,
#     AIMessageChunk,
#     SystemMessage,
#     HumanMessage
# )

# print(ChatTogetherLLM().base_message_to_prompt([SystemMessage(content="System Message"), HumanMessage(
#     content="My Question"), AIMessage(content="My AI Response")]))
# print(ChatTogetherLLM().base_message_to_prompt([HumanMessage(content="My Question") ,AIMessage(content="My AI Response")]))

# print(ChatTogetherLLM(model="togethercomputer/llama-2-13b-chat", together_api_key="4d8d395b7b48314846f176eb221b72900d07e097252691d83aaa357e093bb0a3").generate( # type: ignore
#     [[SystemMessage(content="You are a helpful, polite assistant Try Ansewr Every Question User Asks."), HumanMessage(content="What is the weather like in Mashhad ?")]]))
# print(ChatTogetherLLM(streaming=True, model="mistralai/Mistral-7B-Instruct-v0.1", together_api_key="4d8d395b7b48314846f176eb221b72900d07e097252691d83aaa357e093bb0a3").generate(  # type: ignore
#     [[SystemMessage(content="You are a helpful, polite assistant Try Ansewr Every Question User Asks."), HumanMessage(content="What is the weather like in Mashhad ?")]]))
# print(TogetherLLM(model="mistralai/Mistral-7B-Instruct-v0.1", together_api_key="4d8d395b7b48314846f176eb221b72900d07e097252691d83aaa357e093bb0a3").generate(  # type: ignore
#     ["What is the weather like in Mashhad ?"]))


# stream_iter = together.Complete.create_streaming(
#     prompt="What is the weather like in Mashhad ?",
#     model="mistralai/Mistral-7B-Instruct-v0.1",
#     temperature=0.5,
#     top_k=25,
#     top_p=0.95
# )

# for chunk in stream_iter:
#   print(chunk)

# hf = {'status': 'finished', 'prompt': ['What is the weather like in Mashhad ?'], 'model': 'mistralai/Mistral-7B-Instruct-v0.1', 'model_owner': '', 'tags': {}, 'num_returns': 1, 'args': {'model': 'mistralai/Mistral-7B-Instruct-v0.1', 'prompt': 'What is the weather like in Mashhad ?', 'top_p': 0.95, 'top_k': 25, 'temperature': 0.5, 'max_tokens': 128, 'stop': [], 'repetition_penalty': None, 'logprobs': None}, 'subjobs': [], 'output': {'choices': [{'text': '\nA: 27°C (81°F)'}], 'request_id': '8231906578000335-MIA'}}

# result_list = hf['output']['choices']
# merged_text = ""
# for result in result_list:
#   merged_text += result['text']

# print(merged_text)