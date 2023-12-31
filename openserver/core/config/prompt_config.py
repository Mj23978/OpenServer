import os
import re
from typing import Any, Dict
from anyio import Path

from langchain.schema import (
    BaseMessage
)

from ..utils import base_messages_to_default
from .config import init_config


class PromptConfig:

    def __init__(self):
        configs = init_config("configs/prompts_config.yaml")
        self.configs = configs
        self.prompts: Dict[str, Any] = configs.get_configs().get(
            "prompts")  # type: ignore

    def prompt_template(self, type="function_call", **kwargs):
        prompt_template = ""
        if self.prompts.get(type) == None:
            raise ValueError(f"There is no prompt template name : {type}")
        if self.prompts[type].get("content") == None:
            self.add_prompt_to_config()
        prompt_template = self.prompts[type]["content"]
        return prompt_template

    def add_prompt_to_config(self):
        ROOT_DIR: str = os.path.dirname(Path(__file__).parent.parent.parent)
        for prompt in self.prompts:
            prompt_path = self.prompts[prompt]["file"]
            prompt_file = ROOT_DIR + "/" + prompt_path

            if os.path.exists(prompt_file):
                with open(prompt_file, "r") as file:
                    self.prompts[prompt]["content"] = file.read()

    def extract_text(self, text: str, **kwargs):
        pattern = r'<<(.*?)>>(.*?)<</\1>>'
        matches = re.findall(pattern, text, re.DOTALL)
        messages = [BaseMessage(type=tag, content=content.format(
            **kwargs)) for tag, content in matches]
        return base_messages_to_default(messages)
