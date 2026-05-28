"""Unit tests for config loader.

Covers: Happy Path, Error Path, Edge Cases.
"""
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config import load_config, _load_yaml, _load_env_overrides
from src.models.config import AppConfig


class TestLoadConfigHappyPath:
    """Happy path tests for config loading."""

    def test_load_from_valid_yaml(self, tmp_path):
        """Load config from a valid YAML file."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text(
            'analysis_mode: "ai_vision"\n'
            "confidence_threshold: 0.8\n"
            'output_dir: "./results"\n'
            'language: "eng"\n',
            encoding="utf-8",
        )
        config = load_config(str(yaml_file))
        assert config.analysis_mode == "ai_vision"
        assert config.confidence_threshold == 0.8
        assert config.output_dir == "./results"
        assert config.language == "eng"

    def test_env_overrides_yaml(self, tmp_path):
        """Environment variables override YAML values."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text(
            'analysis_mode: "ocr"\n'
            "confidence_threshold: 0.7\n",
            encoding="utf-8",
        )
        env_vars = {
            "ANALYSIS_MODE": "ai_vision",
            "CONFIDENCE_THRESHOLD": "0.9",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            config = load_config(str(yaml_file))
        assert config.analysis_mode == "ai_vision"
        assert config.confidence_threshold == 0.9

    def test_load_defaults_when_no_file(self, tmp_path):
        """Use defaults when YAML file does not exist."""
        non_existent = tmp_path / "missing.yaml"
        config = load_config(str(non_existent))
        assert config.analysis_mode == "ocr"
        assert config.confidence_threshold == 0.7
        assert config.output_dir == "./output"

    def test_api_key_from_env(self, tmp_path):
        """API key loaded from environment variable."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text("", encoding="utf-8")
        env_vars = {"AI_VISION_API_KEY": "sk-test-123"}
        with patch.dict(os.environ, env_vars, clear=False):
            config = load_config(str(yaml_file))
        assert config.ai_vision_api_key == "sk-test-123"


class TestLoadConfigErrorPath:
    """Error path tests for config loading."""

    def test_nonexistent_yaml_uses_defaults(self, tmp_path):
        """Non-existent YAML path falls back to defaults."""
        config = load_config(str(tmp_path / "nope.yaml"))
        assert isinstance(config, AppConfig)
        assert config.analysis_mode == "ocr"

    def test_invalid_yaml_content_uses_defaults(self, tmp_path):
        """YAML with non-dict content uses defaults."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text("just a string", encoding="utf-8")
        config = load_config(str(yaml_file))
        assert isinstance(config, AppConfig)
        assert config.analysis_mode == "ocr"

    def test_empty_yaml_uses_defaults(self, tmp_path):
        """Empty YAML file uses defaults."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text("", encoding="utf-8")
        config = load_config(str(yaml_file))
        assert isinstance(config, AppConfig)


class TestLoadConfigEdgeCases:
    """Edge case tests for config loading."""

    def test_tesseract_path_none_from_yaml(self, tmp_path):
        """tesseract_path: null in YAML results in None."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text(
            "tesseract_path: null\n", encoding="utf-8"
        )
        config = load_config(str(yaml_file))
        assert config.tesseract_path is None

    def test_partial_yaml_merges_with_defaults(self, tmp_path):
        """Partial YAML only overrides specified fields."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text(
            "confidence_threshold: 0.5\n", encoding="utf-8"
        )
        config = load_config(str(yaml_file))
        assert config.confidence_threshold == 0.5
        assert config.analysis_mode == "ocr"  # default
        assert config.language == "chi_tra+eng"  # default

    def test_env_with_empty_string_not_override(self, tmp_path):
        """Env var set to empty string still overrides."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text(
            'output_dir: "./original"\n', encoding="utf-8"
        )
        env_vars = {"OUTPUT_DIR": ""}
        with patch.dict(os.environ, env_vars, clear=False):
            config = load_config(str(yaml_file))
        assert config.output_dir == ""


class TestLoadYamlHelper:
    """Tests for _load_yaml helper function."""

    def test_returns_empty_dict_for_missing_file(self, tmp_path):
        """Returns empty dict when file doesn't exist."""
        result = _load_yaml(tmp_path / "missing.yaml")
        assert result == {}

    def test_returns_dict_for_valid_yaml(self, tmp_path):
        """Returns parsed dict for valid YAML."""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(
            "key: value\n", encoding="utf-8"
        )
        result = _load_yaml(yaml_file)
        assert result == {"key": "value"}


class TestLoadEnvOverrides:
    """Tests for _load_env_overrides helper function."""

    def test_returns_empty_when_no_env_vars(self):
        """Returns empty dict when no relevant env vars set."""
        env_to_clear = [
            "ANALYSIS_MODE", "AI_VISION_API_KEY",
            "TESSERACT_PATH", "OUTPUT_DIR",
            "CONFIDENCE_THRESHOLD",
        ]
        clean_env = {k: v for k, v in os.environ.items()
                     if k not in env_to_clear}
        with patch.dict(os.environ, clean_env, clear=True):
            result = _load_env_overrides()
        assert result == {}

    def test_converts_threshold_to_float(self):
        """CONFIDENCE_THRESHOLD env var converted to float."""
        env_vars = {"CONFIDENCE_THRESHOLD": "0.85"}
        with patch.dict(os.environ, env_vars, clear=False):
            result = _load_env_overrides()
        assert result["confidence_threshold"] == 0.85
