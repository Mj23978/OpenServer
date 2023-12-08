import re
from typing import Any, Callable
import json


def parse_partial_json(s: str, *, strict: bool = False) -> Any:
    try:
        return json.loads(s, strict=strict)
    except json.JSONDecodeError:
        pass

    new_s = ""
    stack = []
    is_inside_string = False
    escaped = False

    # Process each character in the string one at a time.
    for char in s:
        if is_inside_string:
            if char == '"' and not escaped:
                is_inside_string = False
            elif char == "\n" and not escaped:
                # Replace the newline character with the escape sequence.
                char = "\\n"
            elif char == "\\":
                escaped = not escaped
            else:
                escaped = False
        else:
            if char == '"':
                is_inside_string = True
                escaped = False
            elif char == "{":
                stack.append("}")
            elif char == "[":
                stack.append("]")
            elif char == "}" or char == "]":
                if stack and stack[-1] == char:
                    stack.pop()
                else:
                    # Mismatched closing character; the input is malformed.
                    return None

        new_s += char

    if is_inside_string:
        new_s += '"'

    for closing_char in reversed(stack):
        new_s += closing_char
    try:
        return json.loads(new_s, strict=strict)
    except json.JSONDecodeError:
        return None




def extract_json(text: str, parser: Callable[[str], Any] = json.loads):
    start_braces = text.find('{')
    end_braces = text.rfind('}')
    start_brackets = text.find('[')
    end_brackets = text.rfind(']')

    diff = text[start_brackets+1:start_braces].replace("\n", "").strip()
    if start_brackets != -1 and start_brackets < start_braces and diff == "":
      if end_brackets != -1:
        json_text = text[start_brackets:end_brackets+1]
        try:
            return parser(json_text)
        except json.JSONDecodeError:
            pass

    if start_braces != -1 and end_braces != -1:
        json_text = text[start_braces:end_braces+1]
        try:
            return parser(json_text)
        except json.JSONDecodeError:
            pass
    return None


def parse_json_markdown(json_string: str, *, parser: Callable[[str], Any] = json.loads) -> dict:
    match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)
    json_str = match.group(2) if match else json_string
    json_str = json_str.strip()
    # replace escaped newlines with actual newlines
    json_str = re.sub(r'\\n', r'\n', json_str)
    # replace escaped tabs with actual tabs
    json_str = re.sub(r'\\t', r'\t', json_str)
    # replace escaped quotes with actual quotes
    json_str = re.sub(r'\\"', r'"', json_str)
    parsed = parser(json_str)
    return parsed


def extract_json_from_string(text: str):
    json_str = parse_json_markdown(text, parser=parse_partial_json)
    if json_str is None:
      json_str = extract_json(text, parser=parse_partial_json)
    if  isinstance(json_str, list) and len(json_str) > 0:
        json_str = json_str[0]
    return json_str
