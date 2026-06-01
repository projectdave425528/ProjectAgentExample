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
    return CliRunner()


@pytest.fixture
def input_folder_with_txt(tmp_path):
    chat_file = tmp_path / "chat.txt"
    chat_file.write_text(
        "1/1/2024, 10:00 - Alice: 你好\n"
        "1/1/2024, 10:01 - Bob: 收到\n",
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture
def input_folder_with_images(tmp_path):
    (tmp_path / "receipt.jpg").write_bytes(b"\xff\xd8\xff")
    (tmp_path / "payment.png").write_bytes(b"\x89PNG")
    return tmp_path


@pytest.fixture
def input_folder_mixed(tmp_path):
    chat_file = tmp_path / "chat.txt"
    chat_file.write_text(
        "1/1/2024, 10:00 - Alice: 你好\n",
        encoding="utf-8",
    )
    (tmp_path / "receipt.jpg").write_bytes(b"\xff\xd8\xff")
    return tmp_path


class TestValidateInput:
    def test_returns_error_when_path_not_exists(self, tmp_path):
        result = _validate_input(str(tmp_path / "nonexist"), "ocr")
        assert result == "錯誤：輸入路徑不存在"

    def test_returns_error_for_ai_vision_mode(self, tmp_path):
        result = _validate_input(str(tmp_path), "ai_vision")
        assert result == "AI Vision 模式尚未實現"

    def test_returns_none_for_valid_input(self, tmp_path):
        result = _validate_input(str(tmp_path), "ocr")
        assert result is None


class TestScanFiles:
    def test_finds_txt_files(self, input_folder_with_txt):
        txt_files, image_files = _scan_files(input_folder_with_txt)
        assert len(txt_files) == 1
        assert len(image_files) == 0

    def test_finds_image_files(self, input_folder_with_images):
        txt_files, image_files = _scan_files(input_folder_with_images)
        assert len(txt_files) == 0
        assert len(image_files) == 2

    def test_empty_folder(self, tmp_path):
        txt_files, image_files = _scan_files(tmp_path)
        assert txt_files == []
        assert image_files == []


class TestCheckFiles:
    def test_images_without_txt_returns_exit_code(self):
        result = _check_files([], [Path("img.jpg")])
        assert result == 1

    def test_txt_without_images_returns_none(self):
        result = _check_files([Path("chat.txt")], [])
        assert result is None


class TestCliHappyPath:
    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_analyze_txt_only_success(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
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
        assert "完成" in result.output

    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_analyze_saves_intermediate_json(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
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


class TestCliErrorPath:
    def test_input_not_exists(self, runner, tmp_path):
        result = runner.invoke(cli, [
            "analyze",
            "--input", str(tmp_path / "nonexist"),
            "--output", str(tmp_path / "out.xlsx"),
            "--mode", "ocr",
        ])
        assert result.exit_code == 1
        assert "錯誤：輸入路徑不存在" in result.output

    def test_ai_vision_mode_not_implemented(self, runner, tmp_path):
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
        result = runner.invoke(cli, [
            "analyze",
            "--input", str(input_folder_with_images),
            "--output", str(tmp_path / "out.xlsx"),
            "--mode", "ocr",
        ])
        assert result.exit_code == 1
        assert "警告：未找到 .txt 文件" in result.output


class TestCliEdgeCases:
    @patch("src.main.export_to_excel")
    @patch("src.main.build_records")
    @patch("src.main.parse_chat_file")
    @patch("src.main.load_config")
    def test_txt_without_images_runs_normally(
        self, mock_config, mock_parse, mock_build, mock_export,
        runner, input_folder_with_txt, tmp_path,
    ):
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
        mock_build.assert_called_once()
        assert mock_build.call_args[0][1] == []
