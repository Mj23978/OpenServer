import os
from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pathlib import Path
import yaml

from ..utils.utils import logger


class Config(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra fields

    @classmethod
    def load_config(cls, config_file: str, with_envs = False) -> dict:
        # If config file exists, read it
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config_data = yaml.safe_load(file)
            if config_data is None:
                config_data = {}
        else:
            # If config file doesn't exist, prompt for credentials and create new file
            logger.info("\033[91m\033[1m"
        + "\nConfig file not found. Enter required keys and values."
        + "\033[0m\033[0m")
            config_data = {}
            with open(config_file, "w") as file:
                yaml.dump(config_data, file, default_flow_style=False)

        if with_envs is True:
            # Merge environment variables and config data
            env_vars = dict(os.environ)
            config_data = {**config_data, **env_vars}

        return config_data

    def __init__(self, config_file: str, with_envs = False, **kwargs):
        config_data = self.load_config(config_file, with_envs)
        super().__init__(**config_data, **kwargs)

    def get_config(self, key: str, default: Optional[str] = None) -> str | None:
        return self.model_dump().get(key, default)

    def get_configs(self) -> Dict[str, Any]:
        return self.model_dump()


def init_config(config_file: str, with_envs = False) -> Config:
    ROOT_DIR: str = os.path.dirname(Path(__file__).parent.parent.parent)
    _config_instance = Config(config_file=ROOT_DIR + "/" + config_file, with_envs=with_envs)
    return _config_instance

configs = init_config(config_file="configs/configs.yaml", with_envs=True)
def get_config(key: str, default: Optional[str] = None) -> str | None:
    return configs.get_config(key=key, default=default)
