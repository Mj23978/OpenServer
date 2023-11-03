from langchain.llms import HuggingFaceTextGenInference

llm = HuggingFaceTextGenInference(
    inference_server_url="https://huggingface.co/spaces/HuggingFaceH4/zephyr-chat/",
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
)

print(llm("What did foo say about bar?"))