"""OCR-based image analyzer using Tesseract + Pillow."""
import os
from decimal import Decimal
from pathlib import Path

from src.analyzer.base import ImageAnalyzerBase
from src.analyzer.amount_extractor import AmountExtractor
from src.analyzer.payment_detector import PaymentDetector
from src.models.config import AppConfig
from src.models.image_result import ImageAnalysisResult

_SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Module-level instances for convenience
_amount_extractor = AmountExtractor()
_payment_detector = PaymentDetector()


def extract_amounts(text: str) -> list[Decimal]:
    """Convenience function wrapping AmountExtractor."""
    result = _amount_extractor.extract(text)
    return [result] if result is not None else []


def detect_payment_method(text: str) -> str:
    """Convenience function wrapping PaymentDetector."""
    result = _payment_detector.detect(text)
    return result if result is not None else "unknown"


class OcrAnalyzer(ImageAnalyzerBase):
    """Image analyzer using Tesseract OCR.

    Reads image with Pillow, extracts text with pytesseract,
    then detects amounts and payment methods from the text.
    """

    def analyze(
        self, image_path: str, config: AppConfig
    ) -> ImageAnalysisResult:
        """Analyze image using Tesseract OCR.

        Returns error result on failure (never raises).
        """
        filename = Path(image_path).name

        error = self._validate_file(image_path)
        if error:
            return self._error_result(filename, error)

        raw_text = self._extract_text(image_path, config)
        if raw_text is None:
            return self._error_result(
                filename, "Tesseract OCR 執行失敗"
            )

        return self._build_result(filename, raw_text)

    def _validate_file(self, image_path: str) -> str | None:
        """Validate image file exists and has supported format."""
        if not os.path.isfile(image_path):
            return "無法讀取文件"

        ext = Path(image_path).suffix.lower()
        if ext not in _SUPPORTED_EXTENSIONS:
            return f"唔支援嘅圖片格式: {ext}"

        return None

    def _extract_text(
        self, image_path: str, config: AppConfig
    ) -> str | None:
        """Extract text from image using pytesseract."""
        try:
            from PIL import Image
            import pytesseract

            if config.tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = (
                    config.tesseract_path
                )

            image = Image.open(image_path)
            text = pytesseract.image_to_string(
                image, lang=config.language
            )
            return text
        except Exception:
            return None

    def _build_result(
        self, filename: str, raw_text: str
    ) -> ImageAnalysisResult:
        """Build analysis result from extracted text."""
        amounts = extract_amounts(raw_text)
        payment = detect_payment_method(raw_text)
        confidence = self._calculate_confidence(
            raw_text, amounts, payment
        )

        return ImageAnalysisResult(
            filename=filename,
            analysis_mode="ocr",
            payment_method=payment if payment != "unknown" else None,
            amount=amounts[0] if amounts else None,
            confidence=confidence,
            raw_text=raw_text,
            needs_review=confidence < 0.5,
        )

    def _calculate_confidence(
        self,
        raw_text: str,
        amounts: list[Decimal],
        payment: str,
    ) -> float:
        """Calculate confidence score based on extraction quality."""
        if not raw_text.strip():
            return 0.0

        score = 0.3  # Base score for having text
        if amounts:
            score += 0.35
        if payment != "unknown":
            score += 0.35

        return min(score, 1.0)

    def _error_result(
        self, filename: str, error_msg: str
    ) -> ImageAnalysisResult:
        """Create an error result (no exception raised)."""
        return ImageAnalysisResult(
            filename=filename,
            analysis_mode="ocr",
            confidence=0.0,
            needs_review=True,
            error=error_msg,
        )
