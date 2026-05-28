"""Abstract base class for image analyzers."""
from abc import ABC, abstractmethod

from src.models.config import AppConfig
from src.models.image_result import ImageAnalysisResult


class ImageAnalyzerBase(ABC):
    """Abstract base class defining the interface for image analyzers.

    Subclasses must implement the `analyze` method to provide
    specific analysis logic (OCR, AI Vision, etc.).
    """

    @abstractmethod
    def analyze(
        self, image_path: str, config: AppConfig
    ) -> ImageAnalysisResult:
        """Analyze a payment screenshot image.

        Args:
            image_path: Path to the image file.
            config: Application configuration.

        Returns:
            ImageAnalysisResult with extracted payment info,
            or an error result if analysis fails.
        """
        ...
