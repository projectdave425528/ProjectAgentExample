"""Abstract base class for image analyzers."""
from abc import ABC, abstractmethod
from src.models.config import AppConfig
from src.models.image_result import ImageAnalysisResult


class ImageAnalyzerBase(ABC):
    @abstractmethod
    def analyze(self, image_path: str, config: AppConfig) -> ImageAnalysisResult:
        ...
