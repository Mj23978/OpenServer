import time
from local_llm_function_calling import Generator

start_time = time.time()

# Define a function and models
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                    "maxLength": 20,
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]

# Initialize the generator with the Hugging Face model and our functions
generator = Generator.hf(functions, "microsoft/phi-1_5")

# Generate text using a prompt
function_call = generator.generate("What is the weather like today in Brooklyn?")

end_time = time.time()

execution_time = end_time - start_time

print(f"The first function took {execution_time} seconds to execute.")
    
print(function_call)

# Generate text using a prompt
function_call = generator.generate("What is the weather like today in Mashhad?")

end_time2 = time.time()

execution_time = end_time2 - end_time

print(f"The function took {execution_time} seconds to execute.")
    
print(function_call)