"""Tests for CLI entry point (src/main.py)."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from src.main import (
    _check_files,
    _scan_files,
    _validate_input,
    analyze,
    cli,
)


@pytest.fixture
def runner():
    """Create a CliRunner instance."""
    return CliRunner()


@pytest.fixture
def input_folder_with_txt(tmp_path):
    """Create a temp folder with a .txt chat file."""
    chat_file = tmp_path / "chat.txt"
    chat_file.write_text(
        "1/1/2024, 10:00 - Alice: 你好\n"
        "1/1/2024, 10:01 - Bob: 收到\n",
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture
def input_folder_with_images(tmp_path):
    """Create a temp folder with image files only (no .txt)."""
    (tmp_path / "receipt.jpg").write_bytes(b"\xff\xd8\xff")
    (tmp_path / "payment.png").write_bytes(b"\x89PNG")
    return tmp_path


@pytest.fixture
def input_folder_mixed(tmp_path):
    """Create a temp folder with both .txt and images."""
    chat_file = tmp_path / "chat.txt"
    chat_file.write_text(
        "1/1/2024, 10:00 - Alice: 你好\n",
        encoding="utf-8",
    )
    (tmp_path / "receipt.jpg").write_bytes(b"\xff\xd8\xff")
    return tmp_path


# --- Unit Tests: _validate_input ---


class TestValidateInput:
    """Tests for _validate_input function."""

    def test_returns_error_when_path_not_exists(self, tmp_path):
        """Non-existent path returns error message."""
        result = _validate_input(str(tmp_path / "nonexist"), "ocr")
        assert result == "錯誤：輸入路徑不存在"

    def test_returns_error_for_ai_vision_mode(self, tmp_path):
        """ai_vision mode returns not-implemented error."""
        result = _validate_input(str(tmp_path), "ai_vision")
        assert result == "AI Vision 模式尚未實現"

    def test_returns_none_for_valid_input(self, tmp_path):
        """Valid path + ocr mode returns None."""
        result = _validate_input(str(tmp_path), "ocr")
        assert result is None


# --- Unit Tests: _scan_files ---


class TestScanFiles:
    """Tests for _scan_files function."""

    def test_finds_txt_files(self, input_folder_with_txt):
        """Detects .txt files in folder."""
        txt_files, image_files = _scan_files(input_folder_with_txt)
        assert len(txt_files) == 1
        assert txt_files[0].suffix == ".txt"
        assert len(image_files) == 0

    def test_finds_image_files(self, input_folder_with_images):
        """Detects image files in folder."""
        txt_files, image_files = _scan_files(input_folder_with_images)
        assert len(txt_files) == 0
        assert len(image_files) == 2

    def test_finds_both(self, input_folder_mixed):
        """Detects both .txt and image files."""
        txt_files, image_files = _scan_files(input_folder_mixed)
        assert len(txt_files) == 1
        assert len(image_files) == 1

    def test_empty_folder(self, tmp_path):
        """Empty folder returns empty lists."""
        txt_files, image_files = _scan_files(tmp_path)
        assert txt_files == []
        assert image_files == []


# --- Unit Tests: _check_files ---


class TestCheckFiles:
    """Tests for _check_files function."""

    def test_images_without_txt_returns_exit_code(self):
        """Images present but no .txt returns exit code 1."""
        result = _check_files([], [Path("img.jpg")])
        assert result == 1

    def test_txt_without_images_returns_none(self):
        """Only .txt files is valid (no exit code)."""
        result = _check_files([Path("chat.txt")], [])
        assert result is None

    def test_both_present_returns_none(self):
        """Both .txt and images is valid."""
        result = _check_files([Path("chat.txt")], [Path("img.jpg")])
        assert result is None


# --- CLI Integration Tests: Happy Path ---


class TestCliHappyPath:
    """CLI happy path tests using CliRunner."""

    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_analyze_txt_only_success(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
        """Analyze with .txt only completes successfully."""
        mock_config.return_value = MagicMock()
        mock_parse.return_value = [MagicMock()]
        mock_build.return_value = []
        mock_export.return_value = None

        output_file = str(tmp_path / "output" / "result.xlsx")
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        result = runner.invoke(cli, [
            "analyze",
            "--input", str(input_folder_with_txt),
            "--output", output_file,
            "--mode", "ocr",
        ])

        assert result.exit_code == 0
        assert "完成" in result.output
        mock_parse.assert_called_once()
        mock_build.assert_called_once()
        mock_export.assert_called_once()

    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_analyze_saves_intermediate_json(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
        """Analyze saves intermediate JSON to intermediate/ dir."""
        mock_config.return_value = MagicMock()
        mock_parse.return_value = []
        mock_build.return_value = []
        mock_export.return_value = None

        output_dir = tmp_path / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = str(output_dir / "result.xlsx")

        result = runner.invoke(cli, [
            "analyze",
            "--input", str(input_folder_with_txt),
            "--output", output_file,
            "--mode", "ocr",
        ])

        assert result.exit_code == 0
        intermediate_path = output_dir / "intermediate" / "records.json"
        assert intermediate_path.exists()

    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_verbose_flag_accepted(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
        """--verbose flag is accepted without error."""
        mock_config.return_value = MagicMock()
        mock_parse.return_value = []
        mock_build.return_value = []
        mock_export.return_value = None

        output_dir = tmp_path / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = str(output_dir / "result.xlsx")

        result = runner.invoke(cli, [
            "analyze",
            "--input", str(input_folder_with_txt),
            "--output", output_file,
            "--mode", "ocr",
            "--verbose",
        ])

        assert result.exit_code == 0


# --- CLI Error Path Tests ---


class TestCliErrorPath:
    """CLI error path tests."""

    def test_input_not_exists(self, runner, tmp_path):
        """Non-existent --input returns exit code 1 with Chinese error."""
        result = runner.invoke(cli, [
            "analyze",
            "--input", str(tmp_path / "nonexist"),
            "--output", str(tmp_path / "out.xlsx"),
            "--mode", "ocr",
        ])

        assert result.exit_code == 1
        assert "錯誤：輸入路徑不存在" in result.output

    def test_ai_vision_mode_not_implemented(self, runner, tmp_path):
        """--mode ai_vision returns exit code 1."""
        result = runner.invoke(cli, [
            "analyze",
            "--input", str(tmp_path),
            "--output", str(tmp_path / "out.xlsx"),
            "--mode", "ai_vision",
        ])

        assert result.exit_code == 1
        assert "AI Vision 模式尚未實現" in result.output

    def test_images_without_txt_exits(
        self, runner, input_folder_with_images, tmp_path,
    ):
        """Images without .txt returns exit code 1 with warning."""
        result = runner.invoke(cli, [
            "analyze",
            "--input", str(input_folder_with_images),
            "--output", str(tmp_path / "out.xlsx"),
            "--mode", "ocr",
        ])

        assert result.exit_code == 1
        assert "警告：未找到 .txt 文件" in result.output


# --- CLI Edge Case Tests ---


class TestCliEdgeCases:
    """CLI edge case tests."""

    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_txt_without_images_runs_normally(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
        """Input with .txt but no images runs text-only analysis."""
        mock_config.return_value = MagicMock()
        mock_parse.return_value = [MagicMock()]
        mock_build.return_value = []
        mock_export.return_value = None

        output_dir = tmp_path / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = str(output_dir / "result.xlsx")

        result = runner.invoke(cli, [
            "analyze",
            "--input", str(input_folder_with_txt),
            "--output", output_file,
            "--mode", "ocr",
        ])

        assert result.exit_code == 0
        # build_records called with empty image_results
        mock_build.assert_called_once()
        # Second positional arg should be empty list
        assert mock_build.call_args[0][1] == []

    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_config_option_passed_to_load_config(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
        """--config option is passed to load_config."""
        mock_config.return_value = MagicMock()
        mock_parse.return_value = []
        mock_build.return_value = []
        mock_export.return_value = None

        output_dir = tmp_path / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = str(output_dir / "result.xlsx")
        config_file = str(tmp_path / "custom.yaml")

        result = runner.invoke(cli, [
            "analyze",
            "--input", str(input_folder_with_txt),
            "--output", output_file,
            "--mode", "ocr",
            "--config", config_file,
        ])

        assert result.exit_code == 0
        mock_config.assert_called_once_with(config_file)

    @patch("src.main.load_config")
    def test_tesseract_import_error_handling(
        self, mock_config, runner, input_folder_mixed, tmp_path,
    ):
        """When OcrAnalyzer import fails, shows Tesseract error."""
        mock_config.return_value = MagicMock()

        output_file = str(tmp_path / "out.xlsx")

        # Patch the lazy import inside _run_ocr_analysis
        with patch("src.main.parse_chat_file", return_value=[MagicMock()]):
            with patch(
                "builtins.__import__",
                side_effect=_make_import_raiser("src.analyzer.ocr_analyzer"),
            ):
                result = runner.invoke(cli, [
                    "analyze",
                    "--input", str(input_folder_mixed),
                    "--output", output_file,
                    "--mode", "ocr",
                ])

        assert result.exit_code == 1
        assert "Tesseract" in result.output


def _make_import_raiser(blocked_module: str):
    """Create an __import__ side_effect that blocks a specific module."""
    import builtins
    real_import = builtins.__import__

    def _custom_import(name, *args, **kwargs):
        if name == blocked_module:
            raise ImportError(f"No module named '{blocked_module}'")
        return real_import(name, *args, **kwargs)

    return _custom_import


# --- Integration Test: Full Pipeline (mocked external deps) ---


class TestCliIntegration:
    """Integration test verifying full pipeline data flow."""

    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_full_pipeline_data_flow(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, tmp_path,
    ):
        """Full pipeline: scan → parse → build → export."""
        # Setup: folder with .txt and image
        chat_file = tmp_path / "input" / "chat.txt"
        chat_file.parent.mkdir(parents=True)
        chat_file.write_text(
            "1/1/2024, 10:00 - Alice: 你好\n",
            encoding="utf-8",
        )

        output_dir = tmp_path / "output"
        output_dir.mkdir(parents=True)
        output_file = str(output_dir / "result.xlsx")

        # Mock returns
        mock_msg = MagicMock()
        mock_config.return_value = MagicMock()
        mock_parse.return_value = [mock_msg]
        mock_build.return_value = []
        mock_export.return_value = None

        result = runner.invoke(cli, [
            "analyze",
            "--input", str(tmp_path / "input"),
            "--output", output_file,
            "--mode", "ocr",
        ])

        # Verify pipeline order
        assert result.exit_code == 0
        mock_parse.assert_called_once_with(str(chat_file))
        mock_build.assert_called_once_with([mock_msg], [])
        mock_export.assert_called_once_with([], output_file)

        # Verify intermediate JSON saved
        json_path = output_dir / "intermediate" / "records.json"
        assert json_path.exists()
        content = json.loads(json_path.read_text(encoding="utf-8"))
        assert content == []
