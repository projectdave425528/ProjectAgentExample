"""Configuration loader supporting .env and config.yaml."""
import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from src.models.config import AppConfig

logger = logging.getLogger(__name__)


def _load_yaml(yaml_path: Path) -> dict:
    """Load configuration from a YAML file.

    Returns empty dict if file does not exist.
    """
    if not yaml_path.exists():
        logger.warning(
            "配置文件 %s 唔存在，使用預設值", yaml_path
        )
        return {}
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def _load_env_overrides() -> dict:
    """Load environment variable overrides.

    Maps env vars to AppConfig fields.
    """
    overrides = {}
    env_mapping = {
        "ANALYSIS_MODE": "analysis_mode",
        "AI_VISION_API_KEY": "ai_vision_api_key",
        "TESSERACT_PATH": "tesseract_path",
        "OUTPUT_DIR": "output_dir",
        "CONFIDENCE_THRESHOLD": "confidence_threshold",
    }
    for env_key, config_key in env_mapping.items():
        value = os.environ.get(env_key)
        if value is not None:
            if config_key == "confidence_threshold":
                overrides[config_key] = float(value)
            else:
                overrides[config_key] = value
    return overrides


def load_config(yaml_path: str | None = None) -> AppConfig:
    """Load AppConfig from .env + config.yaml.

    Priority: env vars > yaml > defaults.
    """
    load_dotenv()
    config_path = Path(yaml_path) if yaml_path else Path("config.yaml")
    yaml_data = _load_yaml(config_path)
    env_overrides = _load_env_overrides()
    merged = {**yaml_data, **env_overrides}
    return AppConfig(**merged)
