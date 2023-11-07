import os
from typing import Any, Dict
from anyio import Path

from pydantic import BaseModel
from .config import init_config
from sam.core.utils import logger


class PromptConfigModel(BaseModel):
    provider: str
    model: str
    modelPath: str | None

class PromptConfig:

    def __init__(self):
        configs = init_config("configs/prompts_config.yaml")
        self.configs = configs
        self.prompts: Dict[str, Any] = configs.get_configs().get(
            "prompts")  # type: ignore

    def prompt_template(self, type = "function_call", **kwargs):
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
