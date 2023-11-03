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

    def wrap_prompt_template(self, type = "function_call", **kwargs):
        prompt_template = ""
        ROOT_DIR: str = os.path.dirname(Path(__file__).parent.parent.parent)
        prompt_path = self.prompts[type]["file"]
        prompt_file = ROOT_DIR + "/" + prompt_path

        if os.path.exists(prompt_file):
            with open(prompt_file, "r") as file:
              prompt_template = file.read()
        return prompt_template.format(**kwargs)
