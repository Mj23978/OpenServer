import re


def extract_text(text):
    pattern = r'<<(.*?)>>(.*?)<</\1>>'
    matches = re.findall(pattern, text, re.DOTALL)
    return {tag: content for tag, content in matches}


text = """
<<SYS>> Your objective is to create input in JSON format based on the provided functions schema. <</SYS>>
<<HUMAN>>

Create a JSON array containing only the inputs for the functions only, name and arguments.

example output:
{{
  "name": "get_current_weather",
  "arguments": "{{ \"location\": \"Boston, MA\"}}"
}}

functions : {functions}

Only answer with the specified JSON format, no other text

{prompt}
<</HUMAN>>
"""

print(extract_text(text))
