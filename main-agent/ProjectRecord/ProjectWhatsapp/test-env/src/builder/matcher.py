"""Image-to-message matching logic.

Matches ImageAnalysisResult to ParsedMessage via attachment filenames.
Uses case-insensitive comparison. Logs warnings for unmatched items.
"""
import logging
from pydantic import BaseModel, Field

from src.models.message import ParsedMessage
from src.models.image_result import ImageAnalysisResult

logger = logging.getLogger(__name__)


class MatchedPair(BaseModel):
    """A matched pair of message and image analysis result."""

    message: ParsedMessage = Field(
        ..., description="配對到嘅訊息"
    )
    image_result: ImageAnalysisResult = Field(
        ..., description="配對到嘅圖片分析結果"
    )
    needs_review: bool = Field(
        default=False,
        description="是否需要人工確認",
    )


class MatchResult(BaseModel):
    """Result of the image-to-message matching process."""

    matched_pairs: list[MatchedPair] = Field(
        default_factory=list,
        description="成功配對嘅列表",
    )
    unmatched_images: list[ImageAnalysisResult] = Field(
        default_factory=list,
        description="未能配對到訊息嘅圖片",
    )
    unmatched_attachments: list[str] = Field(
        default_factory=list,
        description="未能配對到圖片嘅附件文件名",
    )


def _build_attachment_index(
    messages: list[ParsedMessage],
) -> dict[str, ParsedMessage]:
    """Build a case-insensitive filename -> first message index.

    Only the first occurrence of each filename is kept.
    """
    index: dict[str, ParsedMessage] = {}
    for message in messages:
        for attachment in message.attachments:
            key = attachment.lower()
            if key not in index:
                index[key] = message
    return index


def _determine_needs_review(
    image_result: ImageAnalysisResult,
) -> bool:
    """Determine if a matched pair needs manual review."""
    return image_result.error is not None or image_result.needs_review


def match_images_to_messages(
    messages: list[ParsedMessage],
    image_results: list[ImageAnalysisResult],
) -> MatchResult:
    """Match image analysis results to messages by attachment filename.

    Matching rules:
    - Case-insensitive filename comparison
    - First occurrence of a filename in messages wins
    - Images with errors are still matched but flagged needs_review
    - Unmatched items are collected for reporting

    Args:
        messages: Parsed WhatsApp messages with attachments.
        image_results: Results from image analysis.

    Returns:
        MatchResult with matched pairs and unmatched items.
    """
    attachment_index = _build_attachment_index(messages)
    matched_pairs: list[MatchedPair] = []
    unmatched_images: list[ImageAnalysisResult] = []
    matched_keys: set[str] = set()

    for image_result in image_results:
        key = image_result.filename.lower()
        message = attachment_index.get(key)

        if message is not None:
            pair = MatchedPair(
                message=message,
                image_result=image_result,
                needs_review=_determine_needs_review(image_result),
            )
            matched_pairs.append(pair)
            matched_keys.add(key)
        else:
            logger.warning(
                "Image '%s' has no matching message attachment",
                image_result.filename,
            )
            unmatched_images.append(image_result)

    unmatched_attachments = _collect_unmatched_attachments(
        attachment_index, matched_keys
    )

    return MatchResult(
        matched_pairs=matched_pairs,
        unmatched_images=unmatched_images,
        unmatched_attachments=unmatched_attachments,
    )


def _collect_unmatched_attachments(
    attachment_index: dict[str, ParsedMessage],
    matched_keys: set[str],
) -> list[str]:
    """Collect attachment filenames that were not matched."""
    unmatched: list[str] = []
    for key in attachment_index:
        if key not in matched_keys:
            # Retrieve original-case filename from the message
            message = attachment_index[key]
            for att in message.attachments:
                if att.lower() == key:
                    unmatched.append(att)
                    break
    if unmatched:
        logger.warning(
            "Attachments without matching images: %s",
            unmatched,
        )
    return unmatched
