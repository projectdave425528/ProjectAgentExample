"""CLI 入口點 — WhatsApp 交易分析 pipeline。

Usage:
    python -m src.main analyze --input <folder> --output <file> \
        --mode <ocr|ai_vision> [--config <path>] [--verbose]
"""
import json
import logging
import sys
from pathlib import Path

import click

from src.parser.text_parser import parse_chat_file
from src.builder.record_builder import build_records, records_to_json
from src.exporter.excel_exporter import export_to_excel
from src.config import load_config

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@click.group()
def cli():
    """WhatsApp 交易分析工具。"""


@cli.command()
@click.option("--input", "input_path", required=True, help="輸入資料夾路徑")
@click.option("--output", "output_path", required=True, help="輸出 Excel 文件路徑")
@click.option("--mode", required=True, type=click.Choice(["ocr", "ai_vision"]), help="分析模式")
@click.option("--config", "config_path", default=None, help="配置文件路徑")
@click.option("--verbose", is_flag=True, default=False, help="顯示詳細日誌")
def analyze(input_path, output_path, mode, config_path, verbose):
    """分析 WhatsApp 聊天記錄及付款截圖。"""
    _setup_logging(verbose)
    error = _validate_input(input_path, mode)
    if error:
        click.echo(error, err=True)
        sys.exit(1)

    txt_files, image_files = _scan_files(Path(input_path))
    exit_code = _check_files(txt_files, image_files)
    if exit_code:
        sys.exit(exit_code)

    config = load_config(config_path)
    messages = _parse_all_txt(txt_files)
    image_results = _analyze_images(image_files, config)
    records = build_records(messages, image_results)

    _save_intermediate(records, output_path)
    export_to_excel(records, output_path)
    click.echo(f"完成：已匯出 {len(records)} 筆交易記錄到 {output_path}")


def _setup_logging(verbose: bool) -> None:
    """設置 logging level。"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def _validate_input(input_path: str, mode: str) -> str | None:
    """驗證輸入路徑和模式。"""
    if not Path(input_path).exists():
        return "錯誤：輸入路徑不存在"
    if mode == "ai_vision":
        return "AI Vision 模式尚未實現"
    return None


def _scan_files(folder: Path) -> tuple[list[Path], list[Path]]:
    """掃描資料夾中的 .txt 和圖片文件。"""
    txt_files = sorted(folder.glob("*.txt"))
    image_files = []
    for ext in IMAGE_EXTENSIONS:
        image_files.extend(folder.glob(f"*{ext}"))
    return txt_files, sorted(image_files)


def _check_files(txt_files: list, image_files: list) -> int | None:
    """檢查文件組合是否有效，返回 exit code 或 None。"""
    if image_files and not txt_files:
        click.echo("警告：未找到 .txt 文件，無法進行文字分析", err=True)
        return 1
    return None


def _parse_all_txt(txt_files: list[Path]) -> list:
    """解析所有 .txt 文件。"""
    messages = []
    for txt_file in txt_files:
        click.echo(f"解析文件：{txt_file.name}")
        parsed = parse_chat_file(str(txt_file))
        messages.extend(parsed)
    click.echo(f"共解析 {len(messages)} 條訊息")
    return messages


def _analyze_images(image_files: list[Path], config) -> list:
    """分析所有圖片文件。"""
    if not image_files:
        return []
    return _run_ocr_analysis(image_files, config)


def _run_ocr_analysis(image_files: list[Path], config) -> list:
    """執行 OCR 分析。"""
    try:
        from src.analyzer.ocr_analyzer import OcrAnalyzer
    except ImportError:
        click.echo("錯誤：Tesseract 未安裝，請先安裝 pytesseract 及 Tesseract OCR")
        sys.exit(1)

    analyzer = OcrAnalyzer()
    results = []
    for img in image_files:
        click.echo(f"分析圖片：{img.name}")
        try:
            result = analyzer.analyze(str(img), config)
            results.append(result)
        except Exception as e:
            _handle_ocr_error(e, img)
    click.echo(f"共分析 {len(results)} 張圖片")
    return results


def _handle_ocr_error(error: Exception, img_path: Path) -> None:
    """處理 OCR 分析錯誤。"""
    error_msg = str(error).lower()
    if "tesseract" in error_msg:
        click.echo("錯誤：Tesseract 未安裝，請先安裝 Tesseract OCR 引擎", err=True)
        sys.exit(1)
    logger.warning("圖片分析失敗 %s: %s", img_path.name, error)


def _save_intermediate(records: list, output_path: str) -> None:
    """保存中間結果 JSON 到 intermediate/ 子目錄。"""
    output_dir = Path(output_path).parent
    intermediate_dir = output_dir / "intermediate"
    intermediate_dir.mkdir(parents=True, exist_ok=True)

    json_path = intermediate_dir / "records.json"
    json_str = records_to_json(records)
    json_path.write_text(json_str, encoding="utf-8")
    click.echo(f"中間結果已保存：{json_path}")


if __name__ == "__main__":
    cli()
